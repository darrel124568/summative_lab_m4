from models.db import Database_manipulations

class User:
    def __init__(self, name, email, projects: list = None):
        self.name = name
        self.email = email
        self.projects = projects if projects is not None else []

    def to_dict(self):
        return {"name": self.name, "email": self.email, "projects": self.projects}

    @staticmethod
    def add_user_to_database(name, email):
        data = Database_manipulations.load()
        if any(u["name"].lower() == name.lower() for u in data["users"]):
            print(f"User '{name}' already exists.")
            return False
        
        new_user = User(name, email)
        data["users"].append(new_user.to_dict())
        Database_manipulations.save(data)
        print(f"User '{name}' added successfully.")
        return True

    @staticmethod
    def get_projects(name: str) -> list:
        data = Database_manipulations.load()
        for u in data["users"]:
            if u["name"].lower() == name.lower():
                return u["projects"]
        return None