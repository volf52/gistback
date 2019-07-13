import requests
from datetime import datetime
import json

BASE_URL = "https://api.github.com"


def create_initial_commit(token: str) -> str:
    headers = {"Authorization": f"token {token}"}
    initial_data = {
        "description": "Backing up critical files on gist",
        "files": {
            "gistSettings.json": {
                "content": json.dumps({"lastModified": str(datetime.now())})
            }
        },
    }
    r = requests.post(
        f"{BASE_URL}/gists", headers=headers, data=json.dumps(initial_data)
    )
    if r.status_code == 201:
        return r.json().get("id", "")
    else:
        return ""
