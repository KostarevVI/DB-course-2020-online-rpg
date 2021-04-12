-------------------------------------ОБЪЕДИНЕНИЕ PERSON И ENEMY
ALTER TABLE Person ALTER COLUMN user_id SET DEFAULT NULL;
ALTER TABLE Enemy ADD COLUMN user_id INTEGER NULL DEFAULT NULL;
ALTER TABLE Person ADD is_enemy BOOLEAN NOT NULL DEFAULT 'f';
ALTER TABLE Person ALTER COLUMN is_enemy SET DEFAULT 't';
INSERT INTO Person(class_of_person_id, health, experience, user_id, update_date) 
SELECT class_of_person_id, health,experience,user_id,update_date FROM Enemy;

------------------------------------ОБЪЕДИНЕНИЕ INVENTORY_PERSON И INVENTORY_ENEMY
INSERT INTO inventory_person(inventory_size) SELECT inventory_size FROM inventory_enemy;
UPDATE inventory_person SET person_id = id;

------------------------------------ОБЪЕДИНЕНИЕ INVENTORY_PERSON_ITEMS И INVENTORY_PERSON_ENEMY
ALTER TABLE inventory_enemy_items ADD COLUMN new_id INTEGER;
UPDATE inventory_enemy_items SET new_id=inventory_enemy_id+3;
INSERT INTO inventory_person_items(inventory_person_id, item_id, add_date, is_deleted, amount, update_date) 
SELECT new_id, item_id, add_date, is_deleted, amount, update_date FROM inventory_enemy_items;

------------------------------------ИЗМЕНЕНИЕ MEETUP
ALTER TABLE meetup ADD COLUMN new_enemy_id INTEGER REFERENCES Person(id) ON DELETE SET NULL;
UPDATE meetup SET new_enemy_id=enemy_id+3;
ALTER TABLE meetup DROP COLUMN enemy_id;
ALTER TABLE meetup RENAME COLUMN new_enemy_id TO enemy_id;

------------------------------------ДОБАВЛЕНИЕ PERSON_SKILL
CREATE TABLE person_skill (
person_id INTEGER REFERENCES person(id) ON DELETE CASCADE,
skill_id INTEGER REFERENCES skill(id) ON DELETE CASCADE,
equiped BOOL NOT NULL
);

insert into person_skill VALUES (1, 1, 'f'),
								(1, 2, 'f'),
								(2, 3, 'f'),
								(2, 4, 'f'),
								(3, 5, 'f'),
								(3, 6, 'f');

------------------------------------ИЗМЕНЕНИЕ SKILL
ALTER TABLE skill DROP COLUMN equiped;

------------------------------------УДАЛЕНИЕ ЛИШНИХ ТАБЛИЦ
DROP TABLE inventory_enemy_items;
DROP TABLE inventory_enemy;
DROP TABLE enemy;
SELECT * FROM information_schema.tables 
WHERE table_schema = 'public'