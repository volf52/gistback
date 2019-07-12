import os
from pathlib import Path
from typing import Tuple
import json
from dotenv import load_dotenv


def get_default_settings() -> dict:
    return {"anc": 123}


def read_settings():
    settings_dir = Path(Path.home()) / "gistback"
    settings_file = settings_dir / "settings.json"
    if not settings_dir.exists():
        Path.mkdir(settings_dir)
    if not settings_file.exists():
        Path.touch(settings_file)
        settings_file.write_text(json.dumps(get_default_settings()))

    return json.loads(settings_file.read_text())


def read_dev_creds() -> Tuple[str, str]:
    env_path = Path(".") / ".env"
    if not env_path.exists():
        Path.touch(env_path)
    load_dotenv(verbose=True, dotenv_path=env_path)
    api_key, api_secret = os.getenv("API_KEY"), os.getenv("API_SECRET")
    if not (api_key and api_secret):
        api_key, api_secret = save_creds_to_env(env_path)
    return api_key, api_secret


def ask_for_creds() -> Tuple[str, str]:
    api_key = input("Enter you api key -> ").strip()
    api_secret = input("Enter your api secret -> ").strip()
    return (api_key, api_secret)


def save_creds_to_env(path_to_env: Path) -> Tuple[str, str]:
    api_key, api_secret = ask_for_creds()
    path_to_env.write_text(f"API_KEY={api_key}\nAPI_SECRET={api_secret}")
    return (api_key, api_secret)


if __name__ == "__main__":
    # print(read_dev_creds())
    print(type(read_settings()))
    pass
