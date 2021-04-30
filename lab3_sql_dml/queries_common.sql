--1. Вывод данных из таблиц
create or replace view task1_1 as SELECT * FROM class_of_person;
create or replace view task1_2 as SELECT * FROM person;
create or replace view task1_3 as SELECT * FROM user_data;
create or replace view task1_4 as SELECT * FROM person_skill;
create or replace view task1_5 as SELECT * FROM skill;
create or replace view task1_6 as SELECT * FROM meetup;
create or replace view task1_7 as SELECT * FROM inventory_person;
create or replace view task1_8 as SELECT * FROM inventory_person_items;
create or replace view task1_9 as SELECT * FROM item;

--2. Сделать выборку данных из одной таблицы при нескольких условиях, с использованием логических операций, 
--**LIKE**, **BETWEEN**, **IN** 
create or replace view task2_1 as SELECT * FROM person WHERE health BETWEEN 150 AND 170;
create or replace view task2_2 as SELECT * FROM user_data WHERE nickname LIKE 'dec%';
create or replace view task2_3 as SELECT * FROM inventory_person_items WHERE inventory_person_id IN ('2', '212', '1212');

--3. Создать в запросе вычисляемое поле
create or replace view task3 as SELECT inventory_person_id, add_date, update_date, extract(epoch FROM update_date - 
add_date)/3600/24 AS delta_days FROM inventory_person_items WHERE add_date != update_date ORDER BY delta_days;

--4. Сделать выборку всех данных с сортировкой по нескольким полям
create or replace view task4 as SELECT * FROM inventory_person_items ORDER BY item_id, amount;

--5. Создать запрос, вычисляющий несколько совокупных характеристик таблиц
create or replace view task5 as SELECT ROUND(AVG(health), 2) AS "AVG Hp", MAX(experience) AS "MAX Exp" FROM person;

--6. Сделать выборку данных из связанных таблиц
create or replace view task6 as SELECT 
    c.name as "Class name", s.name as "Skill name", s.cost 
FROM class_of_person c 
    INNER JOIN skill s on s.class_of_person_id = c.id;

create or replace view task6_2 as SELECT 
    p.id, ud.nickname, c.name 
FROM 
    person p 
    INNER JOIN user_data ud ON p.user_id = ud.id
    INNER JOIN class_of_person c ON p.class_of_person_id = c.id
ORDER BY ud.nickname;

--7.Создать запрос, рассчитывающий совокупную характеристику с использованием группировки, 
--наложите ограничение на результат группировки
create or replace view task7 as SELECT
    inventory_person_id, COUNT(ipi.inventory_person_id), SUM(amount) 
FROM inventory_person_items ipi 
GROUP BY ipi.inventory_person_id HAVING SUM(amount)>5
ORDER BY ipi.inventory_person_id

--8. Придумать и реализовать пример использования вложенного запроса
create or replace view task8 as SELECT COUNT(*) 
FROM person p 
WHERE class_of_person_id = (SELECT cop.id FROM class_of_person cop WHERE cop.name = 'Archer');

--9. С помощью команды **INSERT** добавить в каждую таблицу по одной записи.
CREATE OR REPLACE PROCEDURE task9() LANGUAGE plpgsql AS 
$$ BEGIN
    INSERT INTO public.user_data(email, password, nickname) VALUES ('task_email@ya.ru', 'lo102olo', 'task_nickname') ON CONFLICT DO NOTHING;
    INSERT INTO public.person(class_of_person_id, health, experience, user_id, update_date, is_enemy) VALUES (1, 100, 50, 1, now(), False) ON CONFLICT DO NOTHING;
    INSERT INTO public.meetup(person_id, result, meetup_date, enemy_id) VALUES (1, 'draw', now(), 2) ON CONFLICT DO NOTHING;
    INSERT INTO public.class_of_person(name, description) VALUES ('task_class', 'aaaolo') ON CONFLICT DO NOTHING;
    INSERT INTO public.skill(name, description, cost, class_of_person_id) VALUES ('task_skill', 'ldsdaolo', 50, 6) ON CONFLICT DO NOTHING;
    INSERT INTO public.person_skill(person_id, skill_id, equiped) VALUES (1, 4, True) ON CONFLICT DO NOTHING;
    INSERT INTO public.inventory_person(person_id, inventory_size) VALUES (1, 1000) ON CONFLICT DO NOTHING;
    INSERT INTO public.item(name, description) VALUES ('test_item', 'dsdaw32') ON CONFLICT DO NOTHING;
    INSERT INTO public.inventory_person_items(inventory_person_id, item_id, add_date, is_deleted, amount, update_date) VALUES (1, 4, now(), True, 1, now()) ON CONFLICT DO NOTHING; 
END $$;
CALL task9();

--10. С помощью оператора **UPDATE** измените значения нескольких полей у всех записей, 
--отвечающих заданному условию
CREATE OR REPLACE PROCEDURE task10() LANGUAGE plpgsql AS 
$$ BEGIN
    UPDATE person SET health = 200, update_date = now() WHERE health = 170 AND user_id = 2;
END $$;
CALL task10();

--11. С помощью оператора **DELETE** удалить запись, 
--имеющую максимальное (минимальное) значение некоторой совокупной характеристики
CREATE OR REPLACE PROCEDURE task11() LANGUAGE plpgsql AS 
$$ BEGIN
DELETE FROM person WHERE id = (SELECT person_id
                                FROM (SELECT person_id, count(*) AS meetup_count 
                                      FROM meetup
                                      GROUP BY person_id
                                      ORDER BY meetup_count DESC LIMIT 1) AS most_pupular_meetup_person);
END $$;
CALL task11();

--12. С помощью оператора **DELETE** удалить записи в главной таблице, 
--на которые не ссылается подчиненная таблица (используя вложенный запрос)
CREATE OR REPLACE PROCEDURE task12() LANGUAGE plpgsql AS 
$$ BEGIN
    DELETE FROM class_of_person cop WHERE cop.id NOT IN (SELECT DISTINCT class_of_person_id FROM person);
END $$;
CALL task12();


