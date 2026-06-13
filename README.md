# Command-Line Project Management Tool

This tool allows you to create projects, assign users to projects, track tasks, and mark them as complete. Data is persisted locally in a JSON database.

---

## Features

- **User Management**: Add new users and list all users.
- **Project Tracking**: Create new projects and assign users.
- **Task Management**: Add tasks to projects and track completion status.
- **Local Persistence**: Automatic loading and saving using a local JSON database.
- **CLI Interface**: Easy-to-use command-line interface powered by `argparse`.

---

## Installation & Setup

### 1. Clone or Navigate to the Project Directory

```bash
git clone https://github.com/darrel124568/summative_lab_m4.git
```

### 2. Install Required Dependencies

This project relies on:

- `colorama` for colorized terminal output
- `email-validator` for email verification
- `pytest` for automated testing

Install them with:

```bash
pip install colorama
pip install email-validator
pip install pytest
```

---

## Usage Guide

The tool uses subcommands (`users` and `projects`) along with specific actions.

### User Commands

#### Add a User

```bash
python main.py users add --name "Alice"
```

#### List All Users

```bash
python main.py users all
```

#### View a User's Projects

```bash
python main.py users projects --name "Alice"
```

---

### Project Commands

#### Add a Project

```bash
python main.py projects add --title "Alpha"
```

#### List All Projects

```bash
python main.py projects all
```

#### Link a User to a Project

```bash
python main.py projects add-user --title "Alpha"
```

#### Add a Task to a Project

```bash
python main.py projects add-task --title "Alpha"
```

#### View Project Tasks

```bash
python main.py projects tasks --title "Alpha"
```

#### Mark a Task as Complete

```bash
python main.py projects complete-task --title "Alpha"
```

---

## Running Tests

Automated testing is configured using `pytest`. 

To execute the test suite:

```bash
python -m pytest tests/test_functionality.py
```
