from models.db import Database_manipulations

class Project:
    def __init__(self, title, due_date, tasks: list = None, users: list = None):
        self.title = title
        self.due_date = due_date
        self.tasks = tasks if tasks is not None else []
        self.users = users if users is not None else []

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "due_date": self.due_date,
            "tasks": self.tasks,
            "users": self.users
        }

    @staticmethod
    def add_project_to_database(title, due_date):
        data = Database_manipulations.load()
        if any(p["title"].lower() == title.lower() for p in data["projects"]):
            print(f"Project '{title}' already exists.")
            return False

        new_project = Project(title, due_date)
        data["projects"].append(new_project.to_dict())
        Database_manipulations.save(data)
        print(f"Project '{title}' created.")
        return True

    @staticmethod
    def link_user_and_project(username, project_title):
        data = Database_manipulations.load()
        
        user = next((u for u in data["users"] if u["name"].lower() == username.lower()), None)
        project = next((p for p in data["projects"] if p["title"].lower() == project_title.lower()), None)

        if not project:
            print(f"{project_title} not found, creating a new instance...")
            due_date = input("Enter the due date for the new project: ")
            new_project = Project(project_title, due_date)
            Project.add_project_to_database(new_project.title, due_date)
            Project.link_user_and_project(username, project_title)
            return

        if not user:
            print(f"User '{username}' missing from records. Creating entry...")
            email = input(f"Enter email for {username}: ")
            user = {"name": username, "email": email, "projects": []}
            data["users"].append(user)

        if username not in project["users"]:
            project["users"].append(username)
        if project_title not in user["projects"]:
            user["projects"].append(project_title)

        Database_manipulations.save(data)