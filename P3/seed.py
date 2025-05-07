import sqlite3
import os
from flask_bcrypt import Bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), 'app', 'activity.db')
bcrypt = Bcrypt()
hashed_password = bcrypt.generate_password_hash('testpass').decode('utf-8')
print(f"[DEBUG] Using hashed password for testuser: {hashed_password}")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Insert a test resident (user) with bcrypt hash
c.execute("""
INSERT OR IGNORE INTO resident (resident_id, name, email, phone_number, interests, date_of_birth, profile_image, username, hashed_password)
VALUES (1, 'Test User', 'test@example.com', '555-1234', 'music,sports', '2000-01-01', NULL, 'testuser', ?)
""", (hashed_password,))

# Always update the test user's password and username to ensure login works after reseeding
c.execute("""
UPDATE resident
SET username = 'testuser', hashed_password = ?
WHERE resident_id = 1
""", (hashed_password,))

# Insert more residents for registration testing
c.execute("""
INSERT OR IGNORE INTO resident (resident_id, name, email, phone_number, interests, date_of_birth, profile_image)
VALUES (2, 'Alice Smith', 'alice@example.com', '555-2001', 'books,travel', '1995-04-12', NULL)
""")
c.execute("""
INSERT OR IGNORE INTO resident (resident_id, name, email, phone_number, interests, date_of_birth, profile_image)
VALUES (3, 'Bob Lee', 'bob@example.com', '555-2002', 'sports,chess', '1992-08-23', NULL)
""")
c.execute("""
INSERT OR IGNORE INTO resident (resident_id, name, email, phone_number, interests, date_of_birth, profile_image)
VALUES (4, 'Carol Nguyen', 'carol@example.com', '555-2003', 'food,technology', '1988-11-30', NULL)
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

# Insert more activity groups
c.execute("""
INSERT OR IGNORE INTO activity_group (name, category, description, founding_date, website, email, phone_number, social_media_links, is_active, total_members, event_frequency, membership_fee, open_to_public, min_age)
VALUES ('Boston Book Club', 'Literature', 'A club for book lovers in Boston', '2018-03-15', 'http://bostonbookclub.com', 'books@example.com', '555-2345', '{"facebook": "@bostonbookclub"}', 1, 25, 'monthly', 10, 1, 16)
""")
c.execute("""
INSERT OR IGNORE INTO activity_group (name, category, description, founding_date, website, email, phone_number, social_media_links, is_active, total_members, event_frequency, membership_fee, open_to_public, min_age)
VALUES ('Boston Runners', 'Sports', 'Running group for all levels', '2015-06-10', 'http://bostonrunners.com', 'run@example.com', '555-3456', '{"instagram": "@bostonrunners"}', 1, 40, 'weekly', 0, 1, 18)
""")
c.execute("""
INSERT OR IGNORE INTO activity_group (name, category, description, founding_date, website, email, phone_number, social_media_links, is_active, total_members, event_frequency, membership_fee, open_to_public, min_age)
VALUES ('Boston Chess Masters', 'Games', 'For chess enthusiasts and learners', '2019-09-01', 'http://bostonchess.com', 'chess@example.com', '555-4567', '{"twitter": "@bostonchess"}', 1, 15, 'biweekly', 5, 1, 12)
""")
c.execute("""
INSERT OR IGNORE INTO activity_group (name, category, description, founding_date, website, email, phone_number, social_media_links, is_active, total_members, event_frequency, membership_fee, open_to_public, min_age)
VALUES ('Boston Foodies', 'Food', 'Exploring Boston one restaurant at a time', '2021-02-20', 'http://bostonfoodies.com', 'food@example.com', '555-5679', '{"instagram": "@bostonfoodies"}', 1, 30, 'monthly', 20, 1, 21)
""")
c.execute("""
INSERT OR IGNORE INTO activity_group (name, category, description, founding_date, website, email, phone_number, social_media_links, is_active, total_members, event_frequency, membership_fee, open_to_public, min_age)
VALUES ('Boston Coders', 'Technology', 'A group for coding enthusiasts', '2017-11-05', 'http://bostoncoders.com', 'code@example.com', '555-6789', '{"github": "bostoncoders"}', 1, 50, 'weekly', 0, 1, 16)
""")

conn.commit()
conn.close()

print('Seed data inserted!') 
