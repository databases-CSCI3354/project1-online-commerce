CREATE TABLE IF NOT EXISTS residents (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT UNIQUE,
    interests TEXT,
    date_of_birth TEXT,
    profile_image TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resident_id INTEGER NOT NULL,
    username TEXT UNIQUE NOT NULL, 
    hashed_password TEXT NOT NULL,
    FOREIGN KEY (resident_id) REFERENCES residents(id)
);

CREATE TABLE IF NOT EXISTS activity_groups (
    name TEXT PRIMARY KEY,
    category TEXT,
    description TEXT,
    founding_date TEXT,
    website TEXT,
    email TEXT,
    phone_number TEXT,
    social_media_links TEXT, -- stored as JSON string
    is_active BOOLEAN DEFAULT 1,
    total_members INTEGER DEFAULT 0,
    event_frequency TEXT NOT NULL
        CHECK (event_frequency IN ('weekly','biweekly','monthly')),
    membership_fee INTEGER,
    open_to_public BOOLEAN,
    min_age INTEGER
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY,
    resident_id INTEGER NOT NULL,
    activity_group_name TEXT NOT NULL,
    content TEXT,
    star_rating INTEGER CHECK (star_rating BETWEEN 1 AND 5),
    review_date TEXT,
    is_verified INTEGER DEFAULT 0,
    FOREIGN KEY (resident_id) REFERENCES residents(id),
    FOREIGN KEY (activity_group_name) REFERENCES activity_groups(name)
);

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    activity_group_name TEXT NOT NULL,
    date TEXT NOT NULL,
    location_id INTEGER,
    max_participants INTEGER,
    cost INTEGER,
    registration_required INTEGER,
    registration_deadline TEXT,
    FOREIGN KEY (activity_group_name) REFERENCES activity_groups(name),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    activity_group_name TEXT NOT NULL,
    event_id INTEGER,
    date TEXT,
    attendance INTEGER,
    agenda TEXT,
    FOREIGN KEY (activity_group_name) REFERENCES activity_groups(name),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- (associative)
CREATE TABLE IF NOT EXISTS members (
    resident_id INTEGER,
    activity_group_name TEXT,
    join_date TEXT,
    role TEXT,
    PRIMARY KEY (resident_id, activity_group_name),
    FOREIGN KEY (resident_id) REFERENCES residents(id),
    FOREIGN KEY (activity_group_name) REFERENCES activity_groups(name)
);

-- (associative)
CREATE TABLE IF NOT EXISTS hosts (
    activity_group_name TEXT,
    session_id INTEGER,
    PRIMARY KEY (activity_group_name, session_id),
    FOREIGN KEY (activity_group_name) REFERENCES activity_groups(name),
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- (associative, self-referencing)
CREATE TABLE IF NOT EXISTS prerequisites (
    event_id INTEGER,
    prerequisite_event_id INTEGER,
    minimum_performance INTEGER,
    qualification_period INTEGER,
    is_waiver_allowed INTEGER,
    PRIMARY KEY (event_id, prerequisite_event_id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (prerequisite_event_id) REFERENCES events(id),
    CHECK (event_id != prerequisite_event_id)
);


-- dummy data insertions
INSERT OR IGNORE INTO residents (id, name, email, phone_number, interests, date_of_birth, profile_image)
VALUES
    (1, 'John Doe', 'john.doe@example.com', '+1 (555) 555-5555', 'Music, Art, Cooking', '1990-01-01', 'https://example.com/johndoe.jpg');

INSERT OR IGNORE INTO activity_groups (name, category, description, founding_date, website, email, phone_number, social_media_links, is_active, total_members, event_frequency, membership_fee, open_to_public, min_age)
VALUES
    ('Boston Draws', 'Arts & Crafts', 'Finding the next Picasso!', '2020-01-01', 'https://example.com/arts-and-crafts', 'info@arts-and-crafts.com', '+1 (555) 555-5555', '{"facebook": "https://facebook.com/arts-and-crafts", "instagram": "https://instagram.com/arts-and-crafts"}', 1, 0, 'weekly', 0, 1, 18),
    ('Kpop Dance', 'Dance', 'All are welcome! Not just koreans', '2020-01-01', 'https://example.com/dance', 'info@dance.com', '+1 (555) 555-5555', '{"facebook": "https://facebook.com/dance", "instagram": "https://instagram.com/dance"}', 1, 0, 'weekly', 0, 1, 18),
    ('Mus1c4lyf3', 'Music', 'We love cool music!', '2020-01-01', 'https://example.com/music', 'info@music.com', '+1 (555) 555-5555', '{"facebook": "https://facebook.com/music", "instagram": "https://instagram.com/music"}', 1, 0, 'weekly', 0, 1, 18);


INSERT OR IGNORE INTO users (id, username, hashed_password)
SELECT 
    id,
    name,
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFJWQQFXZs.5HZi' -- Default hashed password: 'password'
FROM Residents
WHERE NOT EXISTS (SELECT 1 FROM users WHERE resident_id = id);
