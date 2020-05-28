-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- /*
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- * USERS
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
INSERT INTO user_data(email, password, nickname)
VALUES ('vas9@gmail.com', 'qwerty123', 'Nagibator999'),
('pit3@yandex.ru', 'asdflk51sd', 'PrettyLame'),
('mark3f@mail.ru', 'wawawaw0w', 'Lamb5Wool');
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- /*
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- * CLASSES
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
INSERT INTO class_of_person(name, description) 
values ('Swordman', 'Short distance attack with sword'),
('Archer', 'Long distance attack with bow&arrows'),
('Mage', 'Mid distance attack with spells');
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- /*
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- * ITEMS
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
INSERT INTO item (name, description) 
values ('Large sword', 'Swordmans weapon'),
('Shield', 'Defence yourself'),
('Heal potion', 'Healt +100'),
('Bow', 'Archers weapon'),
('Arrow', 'My knee!'),							-- 5
('Magic staff', 'Mages weapon'),
('Firestorm spell', 'Makes firestorm'),
('Waterwall spell', 'Makes wall of water'),
('Nature spell', 'Heals persons near you'),
('Coin', 'You can trade it'), 						-- 10
('Very rare item', 'It is a very-very rare item');
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- /*
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- * ENEMY
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
INSERT INTO enemy(health, class_of_person_id, experience) 
values (200, (SELECT id FROM class_of_person WHERE name='Swordman'), 20),
(120, (SELECT id FROM class_of_person WHERE name='Archer'), 10),
(150, (SELECT id FROM class_of_person WHERE name='Mage'), 15);

INSERT INTO inventory_enemy(enemy_id, inventory_size) 
values ((SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Swordman')), 7),
((SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Archer')), 15),
((SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Mage')), 20);

ALTER TABLE inventory_enemy_items ALTER COLUMN add_date SET DEFAULT now();
ALTER TABLE inventory_enemy_items ALTER COLUMN update_date SET DEFAULT now();
INSERT INTO inventory_enemy_items (inventory_enemy_id, item_id, is_deleted, amount) 
values ((SELECT id FROM inventory_enemy WHERE enemy_id=(SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Swordman'))), (SELECT id FROM item WHERE name='Heal potion'), 'f', 1),
((SELECT id FROM inventory_enemy WHERE enemy_id=(SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Swordman'))), (SELECT id FROM item WHERE name='Coin'), 'f', 5),
((SELECT id FROM inventory_enemy WHERE enemy_id=(SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Archer'))), (SELECT id FROM item WHERE name='Arrow'), 'f', 10),
((SELECT id FROM inventory_enemy WHERE enemy_id=(SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Archer'))), (SELECT id FROM item WHERE name='Coin'), 'f', 7),
((SELECT id FROM inventory_enemy WHERE enemy_id=(SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Mage'))), (SELECT id FROM item WHERE name='Nature spell'), 'f', 2),
((SELECT id FROM inventory_enemy WHERE enemy_id=(SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Mage'))), (SELECT id FROM item WHERE name='Waterwall spell'), 'f', 2),
((SELECT id FROM inventory_enemy WHERE enemy_id=(SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Mage'))), (SELECT id FROM item WHERE name='Firestorm spell'), 'f', 2),
((SELECT id FROM inventory_enemy WHERE enemy_id=(SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Mage'))), (SELECT id FROM item WHERE name='Coin'), 'f', 10);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- /*
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- * PERSON
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
INSERT INTO person(class_of_person_id, health, experience, user_id) 
values ((SELECT id FROM class_of_person WHERE name='Swordman'), 250, 0, (SELECT id FROM user_data WHERE email='vas9@gmail.com')),
((SELECT id FROM class_of_person WHERE name='Archer'), 170, 0, (SELECT id FROM user_data WHERE email='pit3@yandex.ru')),
((SELECT id FROM class_of_person WHERE name='Mage'), 200, 0, (SELECT id FROM user_data WHERE email='mark3f@mail.ru'));

INSERT INTO inventory_person(person_id, inventory_size) 
values ((SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='vas9@gmail.com')), 40),
((SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='pit3@yandex.ru')), 40),
((SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='mark3f@mail.ru')), 40);

ALTER TABLE inventory_person_items ALTER COLUMN add_date SET DEFAULT now();
ALTER TABLE inventory_person_items ALTER COLUMN update_date SET DEFAULT now();
INSERT INTO inventory_person_items (inventory_person_id, item_id, is_deleted, amount) 
values ((SELECT id FROM inventory_person WHERE person_id=(SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='vas9@gmail.com'))), (SELECT id FROM item WHERE name='Large sword'), 'f', 1),
((SELECT id FROM inventory_person WHERE person_id=(SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='vas9@gmail.com'))), (SELECT id FROM item WHERE name='Shield'), 'f', 1),
((SELECT id FROM inventory_person WHERE person_id=(SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='vas9@gmail.com'))), (SELECT id FROM item WHERE name='Heal potion'), 'f', 3),
((SELECT id FROM inventory_person WHERE person_id=(SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='pit3@yandex.ru'))), (SELECT id FROM item WHERE name='Bow'), 'f', 1),
((SELECT id FROM inventory_person WHERE person_id=(SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='pit3@yandex.ru'))), (SELECT id FROM item WHERE name='Arrow'), 'f', 15),
((SELECT id FROM inventory_person WHERE person_id=(SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='mark3f@mail.ru'))), (SELECT id FROM item WHERE name='Magic staff'), 'f', 1),
((SELECT id FROM inventory_person WHERE person_id=(SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='mark3f@mail.ru'))), (SELECT id FROM item WHERE name='Firestorm spell'), 'f', 3),
((SELECT id FROM inventory_person WHERE person_id=(SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='mark3f@mail.ru'))), (SELECT id FROM item WHERE name='Waterwall spell'), 'f', 3),
((SELECT id FROM inventory_person WHERE person_id=(SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='mark3f@mail.ru'))), (SELECT id FROM item WHERE name='Nature spell'), 'f', 3);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- /*
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- * SKILLS
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
INSERT INTO skill (name, description, cost, equiped, class_of_person_id)
values ('Swordman skill 1', 'Damage +10', 50, 'f', (SELECT id FROM class_of_person WHERE name='Swordman')),
('Swordman skill 2', 'Damage +20', 100, 'f', (SELECT id FROM class_of_person WHERE name='Swordman')),
('Archer skill 1', 'Range +15', 50, 'f', (SELECT id FROM class_of_person WHERE name='Archer')),
('Archer skill 2', 'Range +30', 100, 'f', (SELECT id FROM class_of_person WHERE name='Archer')),
('Mage skill 1', 'Mana +20', 50, 'f', (SELECT id FROM class_of_person WHERE name='Mage')),
('Mage skill 2', 'Mana +40', 100, 'f', (SELECT id FROM class_of_person WHERE name='Mage'));
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- /*
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- * MEETUP
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
ALTER TABLE meetup ALTER COLUMN meetup_date SET DEFAULT now();
INSERT INTO meetup(person_id, enemy_id, result) 					-- result: 'l' - персонаж проиграл, 'w' - персонаж победил, 'd' - битва прервалась (ничья)
values ((SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='vas9@gmail.com')), (SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Swordman')), 'w'),
((SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='pit3@yandex.ru')), (SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Mage')), 'l'),
((SELECT id FROM person WHERE user_id=(SELECT id FROM user_data WHERE email='mark3f@mail.ru')), (SELECT id FROM enemy WHERE class_of_person_id=(SELECT id FROM class_of_person WHERE name='Archer')), 'd');

