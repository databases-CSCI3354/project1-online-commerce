DROP TABLE IF EXISTS hosts;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS prerequisite;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS activity_group;
DROP TABLE IF EXISTS resident;

-- Table: resident
CREATE TABLE resident (
    resident_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT UNIQUE,
    interests TEXT,
    date_of_birth TEXT,
    profile_image TEXT,
    username TEXT UNIQUE,
    hashed_password TEXT
);

-- Table: activity_group
CREATE TABLE activity_group (
    name TEXT PRIMARY KEY,
    category TEXT,
    description TEXT,
    founding_date TEXT,
    website TEXT,
    email TEXT,
    phone_number TEXT,
    social_media_links TEXT, -- stored as JSON string
    is_active INTEGER DEFAULT 1,
    total_members INTEGER DEFAULT 0,
    event_frequency TEXT,
    membership_fee INTEGER,
    open_to_public INTEGER,
    min_age INTEGER
);

-- Table: review
CREATE TABLE review (
    review_id INTEGER PRIMARY KEY,
    resident_id INTEGER NOT NULL,
    activity_group_name TEXT NOT NULL,
    content TEXT,
    star_rating INTEGER CHECK (star_rating BETWEEN 1 AND 5),
    review_date TEXT,
    is_verified INTEGER DEFAULT 0,
    FOREIGN KEY (resident_id) REFERENCES resident(resident_id),
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name)
);

-- Table: location
CREATE TABLE location (
    location_id INTEGER PRIMARY KEY,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
);

-- Table: event
CREATE TABLE event (
    event_id INTEGER PRIMARY KEY,
    activity_group_name TEXT NOT NULL,
    date TEXT NOT NULL,
    location_id INTEGER,
    max_participants INTEGER,
    cost INTEGER,
    registration_required INTEGER,
    registration_deadline TEXT,
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name),
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Table: session
CREATE TABLE session (
    session_id INTEGER PRIMARY KEY,
    activity_group_name TEXT NOT NULL,
    event_id INTEGER,
    date TEXT,
    attendance INTEGER,
    agenda TEXT,
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

-- Table: member (associative)
CREATE TABLE member (
    resident_id INTEGER,
    activity_group_name TEXT,
    join_date TEXT,
    role TEXT,
    PRIMARY KEY (resident_id, activity_group_name),
    FOREIGN KEY (resident_id) REFERENCES resident(resident_id),
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name)
);

-- Table: hosts (associative)
CREATE TABLE hosts (
    activity_group_name TEXT,
    session_id INTEGER,
    PRIMARY KEY (activity_group_name, session_id),
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name),
    FOREIGN KEY (session_id) REFERENCES session(session_id)
);

-- Table: prerequisite (associative, self-referencing)
CREATE TABLE prerequisite (
    event_id INTEGER,
    prerequisite_event_id INTEGER,
    minimum_performance INTEGER,
    qualification_period INTEGER,
    is_waiver_allowed INTEGER,
    PRIMARY KEY (event_id, prerequisite_event_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id),
    FOREIGN KEY (prerequisite_event_id) REFERENCES event(event_id),
    CHECK (event_id != prerequisite_event_id)
);

-- Table: registrations
CREATE TABLE registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES event(event_id),
    FOREIGN KEY (user_id) REFERENCES resident(resident_id)
);

-- Table: waitlist
CREATE TABLE waitlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    status TEXT DEFAULT 'waiting', -- 'waiting', 'notified', 'confirmed'
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES event(event_id),
    FOREIGN KEY (user_id) REFERENCES resident(resident_id)
);
