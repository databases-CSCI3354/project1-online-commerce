-- Table: resident
-- Stores resident information (e.g., individuals in Boston who join activity groups).
-- The resident table has unique information about each resident.
CREATE TABLE resident (
    resident_id INTEGER PRIMARY KEY,  -- Unique identifier for each resident
    name TEXT NOT NULL,  -- Full name of the resident
    email TEXT UNIQUE NOT NULL,  -- Unique email address (required)
    phone_number TEXT UNIQUE,  -- Optional phone number (must be unique)
    interests TEXT,  -- Resident's interests, potentially stored as a comma-separated list or JSON string
    date_of_birth TEXT,  -- Date of birth, stored as TEXT (YYYY-MM-DD)
    profile_image TEXT  -- Profile image URL or file path (optional)
);

-- Create an index on the resident's email for faster queries
CREATE INDEX idx_resident_email ON resident(email);

-- Table: activity_group
-- Stores information about different activity groups (e.g., sports clubs, professional networks).
CREATE TABLE activity_group (
    name TEXT PRIMARY KEY,  -- Unique name of the activity group (identifier)
    category TEXT,  -- Category of activity (e.g., sports, arts, professional)
    description TEXT,  -- Description of the activity group
    founding_date TEXT,  -- Date the activity group was founded (stored as TEXT: YYYY-MM-DD)
    website TEXT,  -- URL of the activity group's website (optional)
    email TEXT,  -- Email address for the activity group
    phone_number TEXT,  -- Phone number for the activity group
    social_media_links TEXT,  -- Stored as a JSON string, for social media links (e.g., {"facebook": "url", "twitter": "url"})
    is_active INTEGER DEFAULT 1,  -- BOOLEAN stored as INTEGER (1 = active, 0 = inactive)
    total_members INTEGER DEFAULT 0,  -- Count of members in the group, initialized to 0
    event_frequency TEXT,  -- Frequency of events (e.g., weekly, monthly)
    membership_fee INTEGER,  -- Membership fee (in USD)
    open_to_public INTEGER,  -- BOOLEAN (1 = open to public, 0 = closed)
    min_age INTEGER  -- Minimum age required to join (optional)
);

-- Table: review
-- Stores reviews written by residents for activity groups.
CREATE TABLE review (
    review_id INTEGER PRIMARY KEY,  -- Unique identifier for the review
    resident_id INTEGER NOT NULL,  -- FK to resident table (who wrote the review)
    activity_group_name TEXT NOT NULL,  -- FK to activity group table (which group was reviewed)
    content TEXT,  -- Text content of the review
    star_rating INTEGER CHECK (star_rating BETWEEN 1 AND 5),  -- Star rating (1 to 5)
    review_date TEXT,  -- Date of the review (YYYY-MM-DD)
    is_verified INTEGER DEFAULT 0,  -- BOOLEAN stored as INTEGER (1 = verified, 0 = not verified)
    FOREIGN KEY (resident_id) REFERENCES resident(resident_id),  -- Foreign key constraint to resident
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name)  -- Foreign key constraint to activity_group
);

-- Table: location
-- Stores physical locations for events.
CREATE TABLE location (
    location_id INTEGER PRIMARY KEY,  -- Unique identifier for each location
    address TEXT,  -- Street address of the location
    city TEXT,  -- City where the location is situated
    state TEXT,  -- State where the location is situated
    zip_code TEXT  -- ZIP code of the location
);

-- Table: event
-- Stores information about events hosted by activity groups.
CREATE TABLE event (
    event_id INTEGER PRIMARY KEY,  -- Unique identifier for the event
    activity_group_name TEXT NOT NULL,  -- FK to activity group (which group is hosting the event)
    date TEXT NOT NULL,  -- Date of the event (YYYY-MM-DD)
    location_id INTEGER,  -- FK to location table (where the event will be held)
    max_participants INTEGER,  -- Maximum number of participants for the event
    cost INTEGER,  -- Cost of attending the event (in USD)
    registration_required INTEGER,  -- BOOLEAN stored as INTEGER (1 = required, 0 = not required)
    registration_deadline TEXT,  -- Deadline for event registration (YYYY-MM-DD)
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name),  -- Foreign key to activity_group
    FOREIGN KEY (location_id) REFERENCES location(location_id)  -- Foreign key to location
);

-- Create an index on event date for fast querying
CREATE INDEX idx_event_date ON event(date);

-- Table: session
-- Stores session details for recurring or regular events within an activity group.
CREATE TABLE session (
    session_id INTEGER PRIMARY KEY,  -- Unique identifier for the session
    activity_group_name TEXT NOT NULL,  -- FK to activity group (which group is hosting the session)
    event_id INTEGER,  -- FK to event (which event the session is tied to)
    date TEXT,  -- Date of the session (YYYY-MM-DD)
    attendance INTEGER,  -- Number of attendees
    agenda TEXT,  -- The agenda for the session
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name),  -- Foreign key to activity_group
    FOREIGN KEY (event_id) REFERENCES event(event_id)  -- Foreign key to event
);

-- Create an index on session date for fast querying
CREATE INDEX idx_session_date ON session(date);

-- Table: member (associative)
-- Stores many-to-many relationships between residents and activity groups.
CREATE TABLE member (
    resident_id INTEGER,  -- FK to resident table (resident who joined the group)
    activity_group_name TEXT,  -- FK to activity group table (group the resident has joined)
    join_date TEXT,  -- Date the resident joined the group (YYYY-MM-DD)
    role TEXT,  -- Role of the resident in the group (e.g., member, organizer)
    PRIMARY KEY (resident_id, activity_group_name),  -- Composite primary key
    FOREIGN KEY (resident_id) REFERENCES resident(resident_id),  -- Foreign key to resident
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name)  -- Foreign key to activity_group
);

-- Table: hosts (associative)
-- Stores which sessions are hosted by which activity groups.
CREATE TABLE hosts (
    activity_group_name TEXT,  -- FK to activity group (which group is hosting the session)
    session_id INTEGER,  -- FK to session (which session is hosted)
    PRIMARY KEY (activity_group_name, session_id),  -- Composite primary key
    FOREIGN KEY (activity_group_name) REFERENCES activity_group(name),  -- Foreign key to activity_group
    FOREIGN KEY (session_id) REFERENCES session(session_id)  -- Foreign key to session
);

-- Table: prerequisite (associative, self-referencing)
-- Stores prerequisite relationships between events within an activity group.
CREATE TABLE prerequisite (
    event_id INTEGER,  -- FK to event (main event)
    prerequisite_event_id INTEGER,  -- FK to event (prerequisite event)
    minimum_performance INTEGER,  -- Minimum performance required to attend the main event
    qualification_period INTEGER,  -- Period (in days) the qualification remains valid
    is_waiver_allowed INTEGER,  -- BOOLEAN stored as INTEGER (1 = waiver allowed, 0 = no waiver)
    PRIMARY KEY (event_id, prerequisite_event_id),  -- Composite primary key
    FOREIGN KEY (event_id) REFERENCES event(event_id),  -- Foreign key to event
    FOREIGN KEY (prerequisite_event_id) REFERENCES event(event_id),  -- Foreign key to event
    CHECK (event_id != prerequisite_event_id)  -- Ensures an event cannot be its own prerequisite
);

-- Create an index on member resident_id for faster querying
CREATE INDEX idx_member_resident_id ON member(resident_id);
