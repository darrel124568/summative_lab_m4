import json
from utils.utils import read

class DatabaseContext:
    FILE_NAME = "data.json"

    @classmethod
    def load(cls) -> dict:
        try:
            return read(cls.FILE_NAME)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": [], "projects": []}

    @classmethod
    def save(cls, data: dict):
        with open(cls.FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)