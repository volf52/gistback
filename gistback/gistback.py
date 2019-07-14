import json
import os
import sys
from hashlib import md5
from pathlib import Path
from typing import Tuple

from .gitAuth import create_initial_commit


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

    def get_api_token(self) -> str:
        api_token = input("Enter you api token -> ").strip()
        return api_token

    def write_config(self):
        self.file.write_text(json.dumps(self.config))

    def read_config(self):
        self.config = json.loads(self.file.read_text())

    def initialize(self):
        if not self.dir.exists():
            Path.mkdir(self.dir)

        if not self.file.exists():
            Path.touch(self.file)

        api_token = self.get_api_token()
        commitId = create_initial_commit(api_token)
        self.config["apiToken"] = api_token
        self.config["commitId"] = commitId
        self.config["fileList"] = []
        self.write_config()
        return self.config

    def add(self, file_path: Path):
        self.read_config()
        file_list = self.config.get("fileList", [])
        file_hash = md5(file_path.read_bytes()).hexdigest()
        self.logger(f"Hash of the added file is {file_hash}")
        file_list.append(
            {
                "filePath": str(file_path.absolute()),
                "md5sum": file_hash,
                "name": file_path.stem + file_path.suffix,
            }
        )
        self.config["fileList"] = file_list
        self.write_config()

    def list_files(self):
        file_list = self.config.get("fileList", [])
        for i, f in enumerate(file_list):
            f_path = Path(f.get("filePath"))
            f_hash = f.get("md5sum", "")
            self.logger(f"{i}\t{str(f_path)}\t{f_hash}")

    def remove_file(self, idx: int):
        file_list = self.config.get("fileList", [])
        if idx < len(file_list) and idx >= 0:
            removed = file_list.pop(idx)
            self.write_config()
            f_path = str(Path(removed.get("filePath", "")))
            self.logger(f"Removed {f_path}")

    def calculate_diff(self):
        file_list = self.config.get("fileList", [])
        diff_list = []
        for i, f in enumerate(file_list):
            name = f.get("name", "")
            old_hash = f.get("md5sum")
            new_hash = md5(Path(f.get("filePath")).read_bytes()).hexdigest()
            if old_hash != new_hash:
                diff_list.append((i, name, old_hash, new_hash, f))
        return diff_list

    def diff(self):
        diff_list = self.calculate_diff()
        for f in diff_list:
            i, name, old_hash, new_hash, _ = f

            self.logger(f"{i}\t{name}\t{old_hash}\t{new_hash}")

    def run_backup(self):
        diff_list = self.calculate_diff()
        self.logger(f"Running backup for {len(diff_list)} files.")

    def __repr__(self):
        return "<Gistback %r>" % self.home


if __name__ == "__main__":
    from click import echo

    gb = Gistback(echo)
    print(gb.initialize())
    pass