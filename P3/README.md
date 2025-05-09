# Connecting Boston: Local Activity Group Web App

## Overview

This project delivers a lightweight, real-world web application that helps Boston residents find and participate in local activity groups. It solves the problem of scattered or inaccessible group listings by offering a centralized, intuitive platform where users can join activities, register for events, and leave feedback.

Organizers benefit from tools that help them manage sessions, track membership, and gather insights from reviews. The backend is built in Flask with a normalized SQLite database and a user-friendly HTML/CSS/Jinja2 frontend.

Key capabilities:
- Discover and filter groups by interest, cost, frequency, and age group
- Register for events and track participation
- Leave reviews (feature in progress)
- Enable organizers to manage groups, schedule events, and oversee engagement

---

## Recent Feature Additions

The application now includes several important updates:

- Admin dashboard for managing events and overseeing platform activity
- User profiles for personal information and participation tracking
- Prerequisite event tracking for advanced scheduling logic
- Waitlist system with automatic notifications for full events
- Full event registration functionality within the platform
- Distinct user and admin views based on role permissions
- Notification system for registration status and waitlist movement

These enhancements improve both user experience and administrative efficiency.

---

## Team Members and Roles

- Jin Yang Chen – Development Engineer
- Omer Yurekli – Backend Testing & Development Engineer
- Salamun Nuhin – Testing & Development Engineer
- Omar Tall – General Developer
- Arona Gaye – General Developer
- Abraham Chang – Documentation

---

## Quick Start: Deployment Instructions

1. Clone the Repository
```bash
git clone https://github.com/databases-CSCI3354/project1-online-commerce.git
cd project1-online-commerce/P3
```

2. Create and Activate a Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # for Linux/macOS
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Set Up Environment Variables
```bash
cp .env.example .env
```

5. Run the Application
```bash
flask run
```

---

## Testing

The application uses `pytest` for unit and integration testing.

To run all tests:
```bash
python -m pytest
```

For linting:
```bash
make lint
```

Test directory structure:
```
tests/
├── routes/
├── services/
├── integration_test.py
└── conftest.py
```

---

## E-R Diagram and Schema Summary

The E-R diagram below shows how users, events, groups, and registrations are related.

![E-R Diagram](./er_diagram.png)

### Key Entities and Attributes
- Users: id (PK), username, email, hashed_password
- Groups: id (PK), name, description, category, cost
- Events: id (PK), group_id (FK), title, date, location
- Registrations: id (PK), user_id (FK), event_id (FK), status
- Reviews (in development): id (PK), user_id (FK), group_id (FK), star_rating, comment

### Design Considerations
- Users may join multiple groups
- Events may have prerequisites
- Secure and restricted access controls
- Updates handled through a form-based UI

---

## Features

- Secure user login and password encryption
- Clean separation of logic with MVC structure
- Form validation and responsive feedback messages
- Role-based access controls
- Notification system for users
- Automated testing and linting

---

## Known Limitations

- Partial session management implementation

---

## Lessons Learned

- Early ER design decisions reduce future complexity
- Proper use of development tools improves project quality
- Separation of concerns in routes and services aids scalability

---

## Presentation Materials

The full project slide deck is available in the repo as a pdf file. It includes:
- Problem background
- E-R diagram
- Schema breakdown
- Application flow
- Demo examples
