# Databases Project 3 - Connecting Boston: Local Activity Group Web App

## Overview

This project delivers a lightweight, real-world web application that helps Boston residents find and participate in local activity groups. It solves the problem of scattered or inaccessible group listings by offering a centralized, intuitive platform where users can join activities, register for events, and leave feedback.

Organizers benefit from tools that help them manage sessions, track membership, and gather insights from reviews. The backend is built in Flask with a normalized SQLite database and a user-friendly HTML/CSS/Jinja2 frontend.

Key capabilities:
- Discover and filter groups by interest, cost, frequency, and age group
- Register for events and track participation
- Leave reviews (feature in progress)
- Enable organizers to manage groups, schedule events, and oversee engagement

---

## Team Members and Roles

- **Jin Yang Chen** – Development Engineer
- **Omer Yurekli** – Backend Testing & Development Engineer
- **Salamun Nuhin** – Testing & Development Engineer
- **Omar Tall** – General Developer
- **Arona Gaye** – General Developer
- **Abraham Chang** – Documentation

---

## Quick Start: Deployment Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/databases-CSCI3354/project1-online-commerce.git
cd project1-online-commerce/P3
```

### 2. Create and Activate a Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # for Linux/macOS
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
```bash
cp .env.example .env
```

### 5. Run the Application
```bash
flask run
```

---

## Testing

We use `pytest` for all unit and integration tests.
Run:
```bash
python -m pytest
```

Linting:
```bash
make lint
```

Test layout:
```
tests/
├── routes/            # HTTP route tests
├── services/          # Logic-level tests
├── integration_test.py
└── conftest.py
```

---

## E-R Diagram and Schema Summary

### Entities and Attributes
- **Users**: `id (PK)`, `username`, `email`, `hashed_password`
- **Groups**: `id (PK)`, `name`, `description`, `category`, `cost`
- **Events**: `id (PK)`, `group_id (FK)`, `title`, `date`, `location`
- **Registrations**: `id (PK)`, `user_id (FK)`, `event_id (FK)`, `status`
- **Reviews** (in dev): `id (PK)`, `user_id (FK)`, `group_id (FK)`, `star_rating`, `comment`

### Design Notes:
- One user can join multiple groups
- Events can have sessions and prerequisites
- Form-based UI enables DB interaction
- Authenticated users can only modify their own data

---

## Features

-  Secure login system using Flask-Login and Flask-Bcrypt
-  MVC design and reusable route logic
-  Flash messaging and form validation for UX
-  Role-based access and cookie session handling
-  Strong test coverage and automated linting

---

## Not Fully Implemented Yet
- Session handling
- Waitlists and notifications
- Direct event registration via site interface

---

## Lessons Learned

- Securing authentication while keeping the app minimal is tricky
- Early ER design simplifies future schema expansions
- Linting and automation tools streamlined development and debugging

---

## Presentation Materials

The full project slide deck is available in the `/presentation` folder of the repo. It includes:
- Problem background
- E-R diagram
- Schema breakdown
- Application flow
- Demo examples
