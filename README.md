# Online Commerce

## Install Poetry

Please follow the official [installation guide](https://python-poetry.org/docs/#installation) to install Poetry.

## Install dependencies

It is recommended to use Python virtual environment, so you don't pollute your system Python environment.

```bash
# Install dependencies
poetry install
```

```bash
# Activate Python virtual environment
eval "$(poetry env activate)"
```

## Add dependencies

If you want to add a new dependency, please use `poetry add` command.

For example, to add `python-dotenv` dependency, run:

```bash
poetry add python-dotenv
```

## Set up environment variables

```bash
# Create .env file (by copying from .env.example)
cp .env.example .env
```

## Style Enforcement

```bash
black . # Check Python code style
isort . # Sort Python imports
```

## Commands

```bash
# Quick Start at root directory
flask run

# To verify that the app is running, go to the /status endpoint
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
```
