# Online Commerce

## Overview of Project

### Team Members

Jin Yang Chen (development engineer)
Omer Yurekli (team lead)

Omer Yurekli

Arona Gaye

Omar Tall (general developer)

Salamun Nuhin

Abraham Chang

### Description of Tests

Utilised the `pytest` framework for testing, focusing on unit testing the cart functionality, and database retrieval logic. Tests related to the business logic of `category`, `product` and `supplier` have also been included.

### Notable implementation details

Clear segregation of concerns among `services`, `models` and `routes`. `routes` are purely responsible for rendering the HTML templates, offloading all business logic to the corresponding service in `services`. All data structures are centrally managed in the `models` module.

## Quick Start

### Install Poetry

Please follow the official [installation guide](https://python-poetry.org/docs/#installation) to install Poetry.

### Install dependencies

It is recommended to use Python virtual environment, so you don't pollute your system Python environment.

```bash
# Install dependencies
poetry install
```

### Mac/Linux

```bash
# Activate Python virtual environment
eval "$(poetry env activate)"
```

### Windows/Powershell

```bash
# Activate Python Virtual Environment
& .venv\Scripts\Activate.ps1
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

# To verify that the app is running, go to the /status endpoint
```

## Development

### Add dependencies

If you want to add a new dependency, please use `poetry add` command.

For example, to add `python-dotenv` dependency, run:

```bash
poetry add python-dotenv
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
```

## Database Modifications
