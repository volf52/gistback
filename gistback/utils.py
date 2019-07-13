import json
import os
import sys
from pathlib import Path
from typing import Tuple

from gitAuth import create_initial_commit


class Gistback(object):
    def __init__(self, logger):
        self.dir = Path(Path.home()) / "gistback"
        self.file = self.dir / "settings.json"
        self.config = {}
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

    def initialize(self):
        if not self.dir.exists():
            Path.mkdir(self.dir)

        if not self.file.exists():
            Path.touch(self.file)

        api_token = self.get_api_token()
        commitId = create_initial_commit(api_token)
        self.config["apiToken"] = api_token
        self.config["commitId"] = commitId
        return self.config

    def __repr__(self):
        return "<Gistback %r>" % self.home


if __name__ == "__main__":
    from click import echo

    gb = Gistback(echo)
    print(gb.initialize())
    pass
