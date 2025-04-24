# Databases Project 3 - Professor Aviram

## Overview of Project

### Team Members and Roles

## Quick Start

### Create and activate Python virtual environment

```bash
python -m venv .venv

# on macOS/Linux
source .venv/bin/activate   

# on Windows
.venv\Scripts\activate         
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up environment variables

```bash
# Create .env file (by copying from .env.example)
cp .env.example .env
```

## Commands

```bash
# Quick Start at root directory
flask run

# Run tests
pytest

# Run tests with coverage report
pytest --cov=app

# To verify that the app is running, go to the /status endpoint
```

## Development

### Add dependencies

If you want to add a new dependency, please use `pip install` command.

For example, to add `python-dotenv` dependency, run:

```bash
pip install python-dotenv
```

Before you merge your PR, make sure to freeze your current environment back into the `requirements.txt` file.

```bash
pip freeze > requirements.txt
```

## Style Enforcement

```bash
make lint # Run in the root of the directory
```

## Folder Structure

```bash
├── app/
│   ├── models/ # Data models used across the application
│   ├── routes/ # Routes handle the HTTP requests and render the appropriate templates (no business logic)
│   ├── services/ # Services handle the business logic of the application
│   ├── static/ # Static files like CSS
│   ├── templates/ # Jinja templates
│   ├── utils/ # Utility functions that are used across the entire application
│   ├── northwind.db # Built database file
│   └── run.py # Main executuable file
└── tests/ # Tests for each file are labelled with the file name
    ├── routes/ # Tests for route handlers
    ├── services/ # Tests for service layer
    ├── integration_test.py # End-to-end tests
    └── conftest.py # Test fixtures and configuration
```
