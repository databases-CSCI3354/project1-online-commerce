# Databases Project 2 - Professor Aviram

## Team Members and Roles

- Jin Yang Chen: ER Diagram and Write-Up
- Salamun Nuhin: schema.txt

### Decisions made when representing the activity_group entity

Firstly, we debated whether the name of the activity group will suffice as the primary key. Although it is possible for distinct activity groups to have the same name, we could not find any examples of such cases after searching on the web for an hour. As such, we decided to set the name of the activity group as the primary key, and avoided the overhead of maintaining a separate id attribute.

Secondly, after interviewing our friends who have considered joining external activity groups, we found out that a huge concern for many is the frequency with which the activity group hosts events. Many of our interviewees do not want to join activity groups with extremely high frequency of meetups for fear of the commitment levels. Others did not want to pay the membership fee for activity groups which do not meet up frequently enough. From a user-experience standpoint, we believe that the best way to represent event_frequency is via an enum (weekly, fortnightly, monthly, quarterly), as splitting the dates too thinly via number of days makes it difficult for users to filter for their desired activity groups.

Thirdly, we discussed what is the best way to represent the social_media_links
information. Every activity group manages a different subset of social media accounts. For example, [Boston Young Professionals Association](https://bostonypa.com/) has a LinkedIn page because it is a professional community. On the other hand, more casual activity groups such as [Better Off Bowling](https://www.betteroffbowling.com/boston) will manage a more different subset of social media accounts such as X. As the type of activity groups we are looking at is extremely broad, we have good reason to believe that there might be a large proportion of social media sites which only a few activity groups have an account for. If we were to designate an attribute for every single one of these obscure social media sites (i.e. myspace_link, xiaohongshu_link, etc.), there will be many NULL values under these columns which is space-inefficient for the database. As such, we decided to represent the social_media_links attribute as a JSON object where the key is the name of the social media platform and the value is the corresponding link. If a particular activity group does not own a social media account for that platform, that key-value pair will not exist in the JSON object.

### Decisions made when representing the resident entity

We believe that the resident entity (resident of Boston) and activity_group entity have a many-to-many relationship. A resident can be a member of zero or more activity groups. An activity group can have zero or more members. It is also useful to track when the resident joined the activity group for membership fee collection purposes, as well as the role which the resident plays in the activity_group (e.g. member, exco, etc.)

A resident need not necessarily be a member of an activity group to participate in one of its events. Additionally, a resident may not necessarily be interested in all of the activity group’s events because of his unique interests. As such, we believe that a useful website will recommend to users possible events to attend or new activity groups to join semi-frequently. To do that, we need to know the user’s interests. As such, we included interests as a multivalued attribute which users can possibly select from a pool of enums when he first builds his profile on our website.

We also realised that it is redundant to include the attribute age in the resident entity, as we can easily derive it given the resident’s date of birth. Age is an important attribute to keep track of implicitly because certain events are only for mature audiences (e.g. sports bar gatherings)

### Decisions made when representing the event entity

We notice that some events are pre-requisites of others. After speaking with one of our friends who is part of the [Charles River Wheelers](https://crw.org/) club, she mentioned that some of the more demanding cross-country events require participants to have successfully completed prior events before. We therefore modelled this recursive relationship in the ER diagram, keeping note of what the minimum performance must be for the prerequisite event, how long a prerequisite event completion remains valid, as well as whether a waiver can be considered for residents who can provide alternative credentials.

### Decisions made when representing the session entity

It felt reasonable to differentiate normal, routine sessions of activity groups from their highlight events. Members of the activity group might want to check the agenda of each session before deciding whether or not to participate in a particular session. We felt that the most intuitive way to represent the session is a weak entity, whose existence is dependent on activity_group as its identifying entity. With the session number serving as the discriminator, we can uniquely identify the session via the activity group’s name
