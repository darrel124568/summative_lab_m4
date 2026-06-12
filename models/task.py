from models.db import DatabaseContext

class Task:
    def __init__(self, name: str, description: str = '', complete: bool = False):
        self.name = name
        self.description = description
        self.complete = complete

    def to_dict(self) -> dict:
        return {"name": self.name, "description": self.description, "complete": self.complete}

    @staticmethod
    def add_task_to_project(project_title: str, task_name: str):
        data = DatabaseContext.load()
        project = next((p for p in data["projects"] if p["title"].lower() == project_title.lower()), None)
        
        if not project:
            print(f"❌ Project '{project_title}' not found.")
            return

        if any(t["name"].lower() == task_name.lower() for t in project["tasks"]):
            print(f"⚠️ Task '{task_name}' already exists in this project.")
            return

        new_task = Task(task_name)
        project["tasks"].append(new_task.to_dict())
        DatabaseContext.save(data)
        print(f"✅ Added task '{task_name}' to '{project_title}'.")

    @staticmethod
    def mark_as_complete(project_title: str, task_name: str):
        data = DatabaseContext.load()
        project = next((p for p in data["projects"] if p["title"].lower() == project_title.lower()), None)

        if not project:
            print(f"❌ Project '{project_title}' not found.")
            return

        for task in project["tasks"]:
            if task["name"].lower() == task_name.lower():
                task["complete"] = True
                DatabaseContext.save(data)
                print(f"🎯 Task '{task_name}' marked complete!")
                return

        print(f"❌ Task '{task_name}' not found in project '{project_title}'.")