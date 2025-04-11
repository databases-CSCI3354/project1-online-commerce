# Databases Project 2 - Professor Aviram

## Team Members and Roles

- Jin Yang Chen: ER Diagram and Write-Up
- Salamun Nuhin: schema.txt
- Omer Yurekli: SQL code
- Omar Tall: ER Diagram and Documentation Editor
- Arona Gaye: SQL code
- Abraham Chang: Documentation

### Decisions made when representing the activity_group entity

Firstly, we debated whether the name of the activity group would suffice as the primary key. Although it is possible for distinct activity groups to share the same name, we could not find any examples of such cases after searching the web for an hour. As such, we decided to use the name of the activity group as the primary key and avoided the overhead of maintaining a separate id attribute.

Secondly, after interviewing friends who have considered joining external activity groups, we found that a major concern for many is the frequency with which the group hosts events. Some interviewees did not want to join activity groups with an overly high frequency of meetups due to the level of commitment required. Others were hesitant to pay membership fees for groups that meet too infrequently. From a user experience standpoint, we believe that the best way to represent event_frequency is via an enum (weekly, fortnightly, monthly, quarterly). Representing frequency in terms of exact days would make it harder for users to filter for suitable activity groups.

Thirdly, we discussed the best way to represent the social_media_links attribute. Each activity group manages a different subset of social media accounts. For example, the Boston Young Professionals Association has a LinkedIn page due to its professional nature. In contrast, more casual groups such as Better Off Bowling tend to use platforms like X (formerly Twitter). Given the wide variety of group types we are considering, we believe there will be many social media platforms used by only a small number of groups. If we were to designate a separate attribute for each possible platform (e.g., myspace_link, xiaohongshu_link, etc.), the result would be numerous NULL values in the database, which is inefficient. Therefore, we decided to represent social_media_links as a JSON object where the key is the name of the platform and the value is the corresponding URL. If an activity group does not have an account on a specific platform, that key-value pair simply does not exist in the JSON.

### Decisions made when representing the resident entity

We believe that the resident (a resident of Boston) and activity_group entities have a many-to-many relationship. A resident can be a member of zero or more activity groups, and a group can have zero or more members. It is also useful to track when a resident joined a group—for purposes such as membership fee collection—as well as the role the resident holds in the group (e.g., member, executive committee member).

A resident does not need to be a member of an activity group to participate in its events. Additionally, a resident may not be interested in all of a group's events due to their personal interests. Therefore, we believe a useful website should semi-regularly recommend events or new groups for users to explore. To enable this, we included interests as a multivalued attribute, which residents can select from a predefined set of enums when building their profile on the site.

We also realized that including an explicit age attribute in the resident entity is redundant, as age can be derived from the resident’s date of birth. That said, age is an important implicit attribute, as certain events may be restricted to mature audiences (e.g., gatherings at sports bars).

### Decisions made when representing the event entity

We observed that some events are prerequisites for others. One of our friends, a member of the Charles River Wheelers, mentioned that certain demanding cross-country rides require participants to have completed previous rides. We therefore modeled this as a recursive relationship in the ER diagram. We also accounted for details such as the minimum performance required in the prerequisite event, how long that completion remains valid, and whether waivers can be granted for residents who can provide equivalent credentials.

### Decisions made when representing the session entity

We felt it was useful to differentiate between regular, routine sessions and a group’s highlight events. Members may want to check the agenda of a session before deciding whether to participate. We concluded that the most intuitive way to represent a session is as a weak entity, dependent on the activity_group entity as its identifying owner. Using the session number as a discriminator, we can uniquely identify each session through the combination of the activity group’s name and the session number.


### Normalization & Functional Dependencies

Throughout our modeling process, we ensured that all entity sets and relationship sets were normalized to at least Third Normal Form (3NF). This means that:
- All non-key attributes are fully functionally dependent on the primary key (no partial dependencies),
- There are no transitive dependencies between non-key attributes.

For example, in the resident table, email and date_of_birth are only dependent on resident_id, and not on any other non-key attribute. Similarly, the event table avoids transitive dependencies by using a foreign key to the location table instead of repeating location details for each event.

We also decomposed multivalued attributes like interests into a separate table structure (e.g., resident_interests(resident_id, interest)), allowing better scalability and query performance. This approach aligns with 3NF principles and ensures data integrity. For example, we excluded derived attributes like `age`, which can be computed from `date_of_birth`, and identified `interests` as a multivalued attribute that could be refactored into a separate table if implemented fully. 

To reduce redundancy and improve query flexibility, we also extracted address details into a dedicated `location` entity, allowing multiple events to reuse the same location without duplication. 

Normalization Process in Practice:

First Normal Form (1NF) was ensured by removing repeating groups (e.g., representing multiple interests or roles through separate rows in bridge tables).
Second Normal Form (2NF) was achieved by ensuring all non-key attributes are fully dependent on the entire primary key in composite-key scenarios (e.g., resident_id, activity_group_name → role).
Third Normal Form (3NF) was achieved by removing transitive dependencies (e.g., storing location details in a location entity rather than duplicating them in event).

Some of the key functional dependencies that guided our design include:
- `resident_id → name, email, date_of_birth`
- `activity_group.name → category, description, event_frequency`
- `event_id → activity_group_name, date, location_id`
- `(resident_id, activity_group_name) → join_date, role`

Additional functional dependencies considered during modeling:
- session_number, activity_group_name → session_date, session_agenda
- event_id → prerequisite_event_id, waiver_option
- location_id → street, city, state, zipcode

These functional dependencies and normalization decisions informed both our E-R modeling and the final relational schema, helping us ensure data consistency, avoid redundancy, and maintain referential integrity across the database.

[ER Diagram Link](https://drive.google.com/file/d/1QLbSjFEI5fYJH3wG2fbt35MT0Bw4TNWx/view?usp=sharing)
