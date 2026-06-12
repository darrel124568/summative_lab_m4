import argparse
from models.user import User
from models.project import Project
from models.task import Task
from models.db import Database_manipulations

def main():
    parser = argparse.ArgumentParser(description="A commandline project management tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Users Subparser
    user_parser = subparsers.add_parser("users")
    user_parser.add_argument("action", choices=["add", "projects", "add-project", "all"])
    user_parser.add_argument("--name", "-n", help="Name of the user")

    # Projects Subparser
    project_parser = subparsers.add_parser("projects")
    project_parser.add_argument("action", choices=["add", "all", "add-user", "users", "add-task", "tasks", "complete-task"])
    project_parser.add_argument("--title", "-t", help="Title of the project")

    args = parser.parse_args()
    #users
    if args.command == "users":
        if args.action == "add":
            email = input("Enter user email: ")
            User.add_user_to_database(args.name, email)
            
        elif args.action == "projects":
            projects = User.get_projects(args.name)
            if projects is not None:
                print(f"\nProjects managed by {args.name}:")
                for p in projects:
                    print(f" - {p}")
            else:
                print("User not found.")
                
        elif args.action == "add-project":
            project_name = input("Enter project name: ")
            Project.link_user_and_project(args.name, project_name)
        elif args.action == "all":
            data = Database_manipulations.load()
            print("\nAll Users:")
            for u in data["users"]:
                print(f" - Name: {u['name']}, email: {u["email"]}")


    #projects
    elif args.command == "projects":
        if args.action == "add":
            due_date = input("Enter the due date for the new project: ")
            Project.add_project_to_database(args.title, due_date)

        elif args.action == "all":
            data = Database_manipulations.load()
            print("\nAll Projects:")
            for p in data.get("projects", []):
                print(f" - {p['title']} (Due: {p.get('due_date')})")

        elif args.action == "tasks":
            data = Database_manipulations.load()
            project = next((p for p in data["projects"] if p["title"].lower() == args.title.lower()), None)
            if project:
                print(f"\nTasks for '{args.title}':")
                for t in project["tasks"]:
                    status = "Complete" if t["complete"] else "Pending"
                    print(f"{t['name']}  {status}")
            else:
                print("Project not found.")

        elif args.action == "users":
            data = Database_manipulations.load()
            project = next((p for p in data["projects"] if p["title"].lower() == args.title.lower()), None)
            if project:
                print(f"\nTeam Members on '{args.title}':")
                for u in project["users"]:
                    print(f" - {u}")
            else:
                print("Project not found.")

        elif args.action == "add-user":
            user_name = input("Enter the username to add: ")
            Project.link_user_and_project(user_name, args.title)

        elif args.action == "add-task":
            task_name = input("Enter the new task: ")
            description = input("add a description for the task: ")
            Task.add_task_to_project(args.title, task_name, description)

        elif args.action == "complete-task":
            task_name = input("Enter task name to complete: ")
            Task.mark_as_complete(args.title, task_name)

if __name__ == "__main__":
    main()