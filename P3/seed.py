import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'app', 'activity.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Insert a test resident (user)
c.execute("""
INSERT OR IGNORE INTO resident (resident_id, name, email, phone_number, interests, date_of_birth, profile_image, username, hashed_password)
VALUES (1, 'Test User', 'test@example.com', '555-1234', 'music,sports', '2000-01-01', NULL, 'testuser', '$2b$12$C6UzMDM.H6dfI/f/IKcEeOEvQ6h1uZ5l5Q5e5e5e5e5e5e5e5e5e')
""")

# Insert a test activity group
c.execute("""
INSERT OR IGNORE INTO activity_group (name, category, description, founding_date, website, email, phone_number, social_media_links, is_active, total_members, event_frequency, membership_fee, open_to_public, min_age)
VALUES ('Kpop Dance', 'Dance', 'A group for Kpop dance lovers', '2020-01-01', 'http://kpopdance.com', 'kpop@example.com', '555-5678', '{"instagram": "@kpopdance"}', 1, 10, 'weekly', 0, 1, 18)
""")

# Insert a test location
c.execute("""
INSERT OR IGNORE INTO location (location_id, address, city, state, zip_code)
VALUES (1, '123 Main St', 'Boston', 'MA', '02118')
""")

# Insert a test event
c.execute("""
INSERT OR IGNORE INTO event (event_id, activity_group_name, date, location_id, max_participants, cost, registration_required, registration_deadline)
VALUES (1, 'Kpop Dance', '2025-06-01', 1, 50, 0, 1, '2025-05-25')
""")

conn.commit()
conn.close()

print('Seed data inserted!') 
