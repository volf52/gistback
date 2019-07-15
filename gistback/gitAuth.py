import json
from datetime import datetime

import requests

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


def update_gist(token: str, id: str, files):
    headers = {"Authorization": f"token {token}"}
    data = json.dumps(
        {
            "files": {
                "gistSettings.json": {
                    "content": json.dumps({"lastModified": str(datetime.now())})
                },
                **files,
            }
        }
    )
    r = requests.patch(f"{BASE_URL}/gists/{id}", headers=headers, data=data)

    return r.status_code == 200
