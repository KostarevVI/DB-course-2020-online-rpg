CREATE TABLE User_data (
id SERIAL PRIMARY KEY,
email VARCHAR(40),
password VARCHAR(16)
);

CREATE TABLE Item(
id SERIAL PRIMARY KEY,
name VARCHAR(30),
description TEXT
);

CREATE TABLE Class_of_person (
id SERIAL PRIMARY KEY,
name VARCHAR(30)
);

CREATE TABLE Person (
id SERIAL PRIMARY KEY,
class_of_person_id INTEGER REFERENCES Class_of_person(id),
health INTEGER,
experience INTEGER,
user_id INTEGER REFERENCES User_data(id)
);

CREATE TABLE Skill(
id SERIAL PRIMARY KEY,
name VARCHAR(30),
description TEXT,
cost INTEGER,
equiped BOOL,
class_of_person_id INTEGER REFERENCES Class_of_person(id)
);

CREATE TABLE Inventory_person (
id SERIAL PRIMARY KEY,
person_id INTEGER REFERENCES Person(id),
inventory_size INTEGER
);

CREATE TABLE Inventory_person_items(
inventory_person_id INTEGER REFERENCES Inventory_person(id),
item_id INTEGER REFERENCES Item(id),
add_date TIMESTAMP,
is_deleted BOOL,
amount INTEGER,
update_date TIMESTAMP
);

CREATE TABLE Enemy(
id SERIAL PRIMARY KEY,
health INTEGER,
class_of_person_id INTEGER REFERENCES Class_of_person(id),
experience INTEGER
);

CREATE TABLE Inventory_enemy_items(
inventory_enemy_id INTEGER REFERENCES Inventory_enemy(id),
item_id INTEGER REFERENCES Item(id),
add_date TIMESTAMP,
is_deleted BOOL,
amount INTEGER,
update_date TIMESTAMP
);

CREATE TABLE Inventory_enemy(
id SERIAL PRIMARY KEY,
enemy_id INTEGER REFERENCES Enemy(id),
inventory_size INTEGER
);

CREATE TABLE Meetup(
id SERIAL PRIMARY KEY,
person_id INTEGER REFERENCES Person(id),
enemy_id INTEGER REFERENCES Enemy(id),
result CHAR,
meetup_date TIMESTAMP
);

