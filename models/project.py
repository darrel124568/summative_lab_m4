from models.db import DatabaseContext

class Project:
    def __init__(self, title: str, due_date: str, tasks: list = None, users: list = None):
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
    def add_project_to_database(title: str, due_date: str) -> bool:
        data = DatabaseContext.load()
        if any(p["title"].lower() == title.lower() for p in data["projects"]):
            print(f"❌ Project '{title}' already exists.")
            return False

        new_project = Project(title, due_date)
        data["projects"].append(new_project.to_dict())
        DatabaseContext.save(data)
        print(f"✅ Project '{title}' created.")
        return True

    @staticmethod
    def link_user_and_project(username: str, project_title: str):
        data = DatabaseContext.load()
        
        # Target instances
        user_node = next((u for u in data["users"] if u["name"].lower() == username.lower()), None)
        project_node = next((p for p in data["projects"] if p["title"].lower() == project_title.lower()), None)

        if not project_node:
            print(f"❌ Project '{project_title}' not found.")
            return

        # Implicit User Creation if missing
        if not user_node:
            print(f"⚠️ User '{username}' missing from records. Creating entry...")
            email = input(f"Enter email for {username}: ")
            user_node = {"name": username, "email": email, "projects": []}
            data["users"].append(user_node)

        # Append relations safely preventing duplication
        if username not in project_node["users"]:
            project_node["users"].append(username)
        if project_title not in user_node["projects"]:
            user_node["projects"].append(project_title)

        DatabaseContext.save(data)
        print(f"🔗 Linked User '{username}' with Project '{project_title}'.")