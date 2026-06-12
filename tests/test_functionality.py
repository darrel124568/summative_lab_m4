import pytest
from models.database_manipulations import Database_manipulations
from models.user import User
from models.project import Project
from models.task import Task

# FIXTURES

@pytest.fixture(autouse=True)
def mock_db_file(tmp_path, monkeypatch):
    """
    Editting the file path to a temporary database i'm making
    """
    temp_db = tmp_path / "test_data.json"
    monkeypatch.setattr(Database_manipulations, "FILE_NAME", str(temp_db))
    return temp_db


@pytest.fixture
def sample_data():
    """Make sample data for tests."""
    return {
        "users": [
            {"id": 111, "name": "Alice", "email": "alice@example.com", "projects": ["Alpha"]}
        ],
        "projects": [
            {
                "id": 222,
                "title": "Alpha",
                "due_date": "2026-12-31",
                "tasks": [{"name": "Setup", "description": "Initial configuration", "complete": False}],
                "users": ["Alice"]
            }
        ]
    }

# USER TESTS

def test_add_user_success():
    """A brand new user can be successfully added."""
    assert User.add_user_to_database("Bob", "bob@example.com") is True
    
    # Ensure persistence in the database
    data = Database_manipulations.load()
    assert len(data["users"]) == 1
    assert data["users"][0]["name"] == "Bob"
    assert data["users"][0]["email"] == "bob@example.com"


def test_add_user_duplicate():
    """Verifies no duplication of usernames"""
    User.add_user_to_database("Alice", "alice@example.com")
    assert User.add_user_to_database("alice", "alice2@example.com") is False
    #ensure the database isn't changed
    data = Database_manipulations.load()
    assert len(data["users"]) == 1


def test_get_projects_for_user(sample_data):
    """fetch projects linked to a specific user."""
    Database_manipulations.save(sample_data)
    
    projects = User.get_projects("Alice")
    assert projects == ["Alpha"]

    # Test for a non-exsiting user
    assert User.get_projects("Ghost") is None

# PROJECT TESTS

def test_add_project_success():
    """Verifies a brand new project can be successfully added."""
    assert Project.add_project_to_database("Beta", "2026-08-15") is True
    
    data = Database_manipulations.load()
    assert len(data["projects"]) == 1
    assert data["projects"][0]["title"] == "Beta"


def test_add_project_duplicate():
    """Verifies duplicate project titles are rejected."""
    Project.add_project_to_database("Alpha", "2026-12-31")
    assert Project.add_project_to_database("alpha", "2027-01-01") is False


def test_link_user_and_project_existing(sample_data):
    """Tests linking an existing user to an existing project."""
    sample_data["users"].append({"id": 333, "name": "Bob", "email": "bob@example.com", "projects": []})
    Database_manipulations.save(sample_data)

    Project.link_user_and_project("Bob", "Alpha")

    data = Database_manipulations.load()
    bob = next(u for u in data["users"] if u["name"] == "Bob")
    alpha = next(p for p in data["projects"] if p["title"] == "Alpha")

    assert "Alpha" in bob["projects"]
    assert "Bob" in alpha["users"]


def test_link_user_and_project_missing_user(sample_data, monkeypatch):
    """
    Tests linking when the user doesn't exist yet
    """
    Database_manipulations.save(sample_data)
    monkeypatch.setattr("builtins.input", lambda _: "charlie@example.com")
    
    Project.link_user_and_project("Charlie", "Alpha")
    
    data = Database_manipulations.load()
    charlie = next((u for u in data["users"] if u["name"] == "Charlie"), None)
    
    assert charlie is not None
    assert charlie["email"] == "charlie@example.com"
    assert "Alpha" in charlie["projects"]

# TASK TESTS

def test_add_task_to_project(sample_data):
    """Verifies a task can be successfully appended to a specific project."""
    Database_manipulations.save(sample_data)

    Task.add_task_to_project("Alpha", "Test_task_Name", "Sample description")

    data = Database_manipulations.load()
    project = data["projects"][0]
    
    assert len(project["tasks"]) == 2
    assert project["tasks"][1]["name"] == "Test_task_Name"


def test_mark_as_complete(sample_data):
    """Verifies a task can be set to complete is True."""
    Database_manipulations.save(sample_data)

    Task.mark_as_complete("Alpha", "Setup")

    data = Database_manipulations.load()
    task = data["projects"][0]["tasks"][0]
    
    assert task["complete"] is True