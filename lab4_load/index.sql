-- Запрос 1
CREATE INDEX IF NOT EXISTS meetup_person_idx ON meetup(person_id);
CREATE INDEX IF NOT EXISTS meetup_enemy_idx ON meetup(enemy_id);
CREATE INDEX IF NOT EXISTS person_user_idx ON person(user_id);
CREATE INDEX IF NOT EXISTS person_class_idx ON person(class_of_person_id);
CREATE INDEX IF NOT EXISTS user_nickname_idx ON user_data(nickname);


DROP INDEX IF EXISTS meetup_person_idx;
DROP INDEX IF EXISTS meetup_enemy_idx;
DROP INDEX IF EXISTS person_user_idx;
DROP INDEX IF EXISTS person_class_idx;
DROP INDEX IF EXISTS user_nickname_idx;


-- Запрос 2
CREATE INDEX IF NOT EXISTS meetup_date_idx ON meetup(meetup_date);

DROP INDEX IF EXISTS meetup_date_idx;


-- Запрос 3
CREATE INDEX IF NOT EXISTS inventory_person_item_inventory_person_idx ON inventory_person_items(inventory_person_id);
CREATE INDEX IF NOT EXISTS inventory_person_person_idx ON inventory_person(person_id);

DROP INDEX IF EXISTS inventory_person_item_inventory_person_idx;
DROP INDEX IF EXISTS inventory_person_person_idx;

-- Запрос 4
CREATE INDEX IF NOT EXISTS inventory_person_item_inventory_person_idx ON inventory_person_items(inventory_person_id);
CREATE INDEX IF NOT EXISTS inventory_person_person_idx ON inventory_person(person_id);
CREATE INDEX IF NOT EXISTS person_skill_skill_idx ON person_skill(skill_id);
CREATE INDEX IF NOT EXISTS person_health_idx ON person(health);

DROP INDEX IF EXISTS inventory_person_item_inventory_person_idx;
DROP INDEX IF EXISTS inventory_person_person_idx;
DROP INDEX IF EXISTS person_skill_skill_idx;
DROP INDEX IF EXISTS person_health_idx;


-- Запрос 5
CREATE INDEX IF NOT EXISTS inventory_person_items_item_addupdate_date_idx ON inventory_person_items(item_id, add_date, update_date);
CREATE INDEX IF NOT EXISTS inventory_person_item_inventory_person_idx ON inventory_person_items(inventory_person_id);
CREATE INDEX IF NOT EXISTS inventory_person_item_inventory_person_item_idx ON inventory_person_items(inventory_person_id, item_id);
CREATE INDEX IF NOT EXISTS inventory_person_item_idx ON inventory_person_items(item_id);

DROP INDEX IF EXISTS inventory_person_items_item_addupdate_date_idx;
DROP INDEX IF EXISTS inventory_person_item_inventory_person_idx;
DROP INDEX IF EXISTS inventory_person_item_inventory_person_item_idx;
DROP INDEX IF EXISTS inventory_person_idx;
DROP INDEX IF EXISTS inventory_person_item_idx;










