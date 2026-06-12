import json

class Database_manipulations:
    FILE_NAME = "data.json"

    @classmethod
    def load(cls) -> dict:
        try:
            return cls.read()
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": [], "projects": []}

    @classmethod
    def save(cls, data: dict):
        with open(cls.FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def read(cls):
        with open(cls.FILE_NAME) as f:
            return(json.load(f))