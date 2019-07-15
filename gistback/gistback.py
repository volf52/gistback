import json
import os
import sys
from hashlib import md5
from pathlib import Path
from typing import Tuple

from .gitAuth import create_initial_commit, update_gist


class Gistback(object):
    def __init__(self, logger):
        self.dir = Path(Path.home()) / "gistback"
        self.file = self.dir / "settings.json"
        self.config = {"fileList": [], "commitId": "", "apiToken": ""}
        self.verbose = False
        self.logger = logger

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            self.logger(f"  config[{key}] = {value}", file=sys.stderr)

    def __get_api_token(self) -> str:
        api_token = input("Enter you api token -> ").strip()
        return api_token

    def __write_config(self):
        self.file.write_text(json.dumps(self.config))

    def read_config(self):
        self.config = json.loads(self.file.read_text())

    def initialize(self):
        if not self.dir.exists():
            Path.mkdir(self.dir)

        if not self.file.exists():
            Path.touch(self.file)

        api_token = self.__get_api_token()
        commitId = create_initial_commit(api_token)
        self.config["apiToken"] = api_token
        self.config["commitId"] = commitId
        self.config["fileList"] = []
        self.config["newFiles"] = []
        self.config["pendingChanges"] = {"rename": [], "remove": []}
        self.__write_config()
        return self.config

    def add(self, file_path: Path, name=None):
        self.read_config()
        try:
            file_path.read_text()
        except:
            self.logger("You can only add text files for now")
            self.logger("Aborting...")
            return
        new_files = self.config.get("newFiles", [])
        file_hash = md5(file_path.read_bytes()).hexdigest()
        file_name = file_path.stem + file_path.suffix if name is None else name
        file_obj = {
            "filePath": str(file_path.absolute()),
            "md5sum": file_hash,
            "name": file_name,
        }
        new_files.append(file_obj)
        self.logger(f"Hash of the added file is {file_hash}")
        self.logger(f"{file_name} added successfully")

        # self.config["fileList"] = file_list
        self.config["newFiles"] = new_files
        self.__write_config()

    def list_files(self):
        file_list = self.config.get("fileList", [])
        for i, f in enumerate(file_list):
            f_path = Path(f.get("filePath"))
            f_hash = f.get("md5sum", "")
            self.logger(f"{i}\t{str(f_path)}\t{f_hash}")

    def list_staged(self):
        diff_list = self.__calculate_diff(self.config.get("newFiles", []), "new")
        diff_list.extend(self.__calculate_diff(self.config.get("fileList", []), "old"))
        self.__print_diff(diff_list)

    def remove_file(self, idx: int, t: str):
        file_list = self.config.get(t, [])
        if idx < len(file_list) and idx >= 0:
            removed = file_list.pop(idx)
            if t == "fileList":
                pendingRemoves = self.config.get("pendingChanges").get("remove", [])
                pendingRemoves.append(removed.get("name"))
            self.__write_config()
            f_path = str(Path(removed.get("filePath", "")))
            self.logger(f"Removed {f_path}")

    def __calculate_diff(self, file_list, t):
        diff_list = []
        for i, f in enumerate(file_list):
            name = f.get("name", "")
            fp = Path(f.get("filePath"))
            old_hash = "" if t == "new" else f.get("md5sum")
            if fp.exists():
                new_hash = md5(fp.read_bytes()).hexdigest()
            else:
                new_hash = "Deleted"
            if old_hash != new_hash:
                diff_list.append((i, name, old_hash, new_hash, f))
        return diff_list

    def diff(self):
        file_list = self.config.get("fileList", [])
        diff_list = self.__calculate_diff(file_list, "old")
        self.__print_diff(diff_list)

    def __print_diff(self, diff_list):
        for f in diff_list:
            i, name, old_hash, new_hash, _ = f

            self.logger(f"{i}\t{name}\t{old_hash}\t{new_hash}")

    def __get_removed(self):
        removed = self.config.get("pendingChanges").get("remove", [])
        return dict([(x, None) for x in removed])

    def __prepare_files(self, file_list):
        data = {}
        for (i, name, old_hash, new_hash, f) in file_list:
            f_path = Path(f.get("filePath"))
            new_data_obj = {"content": f_path.read_text() if f_path.exists() else None}
            data[f.get("name")] = new_data_obj
        return data

    def run_backup(self):
        new_files = self.config.get("newFiles", [])
        file_list = self.config.get("fileList", [])
        token = self.config.get("apiToken", False)
        commitId = self.config.get("commitId", False)
        if not (commitId and token):
            self.logger("There's a problem with the token or the commit id")
            self.logger("Aborting...")
            return
        diff_list = []
        diff_list.extend(self.__calculate_diff(new_files, "new"))
        diff_list.extend(self.__calculate_diff(file_list, "old"))
        length = len(diff_list) + len(self.config.get("pendingChanges").get("remove"))
        if length == 0:
            self.logger("Nothing to backup")
            return
        self.logger(f"Running backup for {length} files.")
        data = self.__prepare_files(diff_list)
        data.update(self.__get_removed())
        result = update_gist(token, commitId, data)
        self.logger(f"Operation was {'' if result else 'un'}successful")
        file_list.extend(new_files)
        self.config["newFiles"] = []
        self.config["fileList"] = file_list
        self.config["pendingChanges"]["remove"] = []
        self.__write_config()

    def __repr__(self):
        return "<Gistback %r>" % self.home


if __name__ == "__main__":
    from click import echo

    gb = Gistback(echo)
    print(gb.initialize())
    pass
