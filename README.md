# Online Commerce

## Install Poetry

It is recommended to use Python virtual environment, so you don't pollute your system Python environment.

```bash
# Install dependencies
poetry install
```

```bash
# Activate Python virtual environment
eval "$(poetry env activate)"
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
# Quick Start
flask --app flaskr run --debug

# Initialize database
$ flask --app flaskr init-db
```
