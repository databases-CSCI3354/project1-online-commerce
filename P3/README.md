# Databases Project 3 - Professor Aviram

## Overview of Project

### Team Members and Roles

- Jin Yang Chen: Development Engineer
- Omer Yurekli: Testing & Development Engineeer
- Salamun Nuhin: Testing & Development Engineer
- Omar Tall: General Developer
- Arona Gaye: General Developer
- Abraham Chang: Documentation

## Quick Start

### Create and activate Python virtual environment

```bash

python3 -m venv .venv

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

### Add Google Maps API Key (Optional)

To see our embedded google maps iframe, you can create a Google Maps API key on google clouds services and add that to the .env file.

## Commands

```bash
# Quick Start at root directory
flask run

# Run tests
python -m pytest
```

## Development

### Add dependencies

If you want to add a new dependency, please use `make add-<dependency>` command.

For example, to add `python-dotenv` dependency, run:

```bash
make add-python-dotenv
```

The above command will add the dependency to the `requirements.txt` file and install it in your current environment. If not, you will need to manually freeze your environment at the end.

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
│   ├── activity.db # Built database file
│   └── run.py # Main executuable file
└── tests/ # Tests for each file are labelled with the file name
    ├── routes/ # Tests for route handlers
    ├── services/ # Tests for service layer
    ├── integration_test.py # End-to-end tests
    └── conftest.py # Test fixtures and configuration
```
