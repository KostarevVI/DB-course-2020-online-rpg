CREATE TYPE meetup_result AS ENUM ('loose', 'draw', 'win'); -- 'loose' - персонаж проиграл, 'win' - персонаж победил, 'draw' - битва прервалась (ничья)

CREATE TABLE User_data (
id SERIAL PRIMARY KEY,
email VARCHAR(40) UNIQUE NOT NULL CHECK(email != ''),
password VARCHAR(16) NOT NULL CHECK(password!=''),
nickname VARCHAR(20) UNIQUE NOT NULL CHECK(nickname!='')
);

CREATE TABLE Item(
id SERIAL PRIMARY KEY,
name VARCHAR(30) UNIQUE NOT NULL CHECK(name!=''),
description TEXT NOT NULL CHECK(description!='')
);

CREATE TABLE Class_of_person (
id SERIAL PRIMARY KEY,
name VARCHAR(30) UNIQUE NOT NULL CHECK(name!=''),
description TEXT NOT NULL CHECK(description!='')
);

CREATE TABLE Person (
id SERIAL PRIMARY KEY,
class_of_person_id INTEGER REFERENCES Class_of_person(id) ON DELETE CASCADE,
health INTEGER NOT NULL,
experience INTEGER NOT NULL,
user_id INTEGER REFERENCES User_data(id) ON DELETE CASCADE,
update_date TIMESTAMP NOT NULL
);

CREATE TABLE Skill(
id SERIAL PRIMARY KEY,
name VARCHAR(30) UNIQUE NOT NULL CHECK(name!=''),
description TEXT NOT NULL CHECK(description!=''),
cost INTEGER NOT NULL,
equiped BOOL NOT NULL,
class_of_person_id INTEGER REFERENCES Class_of_person(id) ON DELETE CASCADE
);

CREATE TABLE Inventory_person (
id SERIAL PRIMARY KEY,
person_id INTEGER REFERENCES Person(id) ON DELETE CASCADE,
inventory_size INTEGER NOT NULL CHECK(inventory_size>0)
);

CREATE TABLE Inventory_person_items(
inventory_person_id INTEGER REFERENCES Inventory_person(id) ON DELETE CASCADE,
item_id INTEGER REFERENCES Item(id) ON DELETE CASCADE,
add_date TIMESTAMP NOT NULL,
is_deleted BOOL NOT NULL,
amount INTEGER NOT NULL CHECK(amount>0),
update_date TIMESTAMP NOT NULL
);

CREATE TABLE Enemy(
id SERIAL PRIMARY KEY,
health INTEGER NOT NULL,
class_of_person_id INTEGER REFERENCES Class_of_person(id) ON DELETE CASCADE,
experience INTEGER NOT NULL,
update_date TIMESTAMP NOT NULL
);

CREATE TABLE Inventory_enemy(
id SERIAL PRIMARY KEY,
enemy_id INTEGER REFERENCES Enemy(id) ON DELETE CASCADE,
inventory_size INTEGER NOT NULL CHECK(inventory_size>0)
);

CREATE TABLE Inventory_enemy_items(
inventory_enemy_id INTEGER REFERENCES Inventory_enemy(id) ON DELETE CASCADE,
item_id INTEGER REFERENCES Item(id) ON DELETE CASCADE,
add_date TIMESTAMP NOT NULL,
is_deleted BOOL NOT NULL,
amount INTEGER NOT NULL CHECK(amount>0),
update_date TIMESTAMP NOT NULL
);

CREATE TABLE Meetup(
id SERIAL PRIMARY KEY,
person_id INTEGER REFERENCES Person(id) ON DELETE CASCADE,
enemy_id INTEGER REFERENCES Enemy(id) ON DELETE SET NULL,
result meetup_result NOT NULL,
meetup_date TIMESTAMP NOT NULL
);

