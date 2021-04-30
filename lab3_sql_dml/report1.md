# Язык SQL DML

## Цели работы:

Познакомиться с языком создания запросов управления данными SQL-DML.

## Программа работы:

1. Самостоятельное изучение SQL-DDL.
2. Создание скрипта БД в соответствии с согласованной схемой. Должны присутствовать первичные и внешние ключи, ограничения на диапазоны значений. Демонстрация скрипта преподавателю.
3. Создание скрипта, заполняющего все таблицы БД данными.
4. Выполнение SQL-запросов, изменяющих схему созданной БД по заданию преподавателя. Демонстрация их работы преподавателю.

## Ход работы:

## Создание стандартных запросов

### 1. Сделать выборку данных из одной таблицы

 - Вывод данных из таблицы **class_of_person**.

```sql
create or replace view task1_1 as SELECT * FROM class_of_person;
```

Результат запроса:  
![task1_1](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task1_1.png)

 - Вывод данных из таблицы **person**.

```sql
create or replace view task1_2 as SELECT * FROM person;
```

Результат запроса:  
![task1_2](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task1_2.png)

 - Вывод данных из таблицы **user_data**.

```sql
create or replace view task1_3 as SELECT * FROM user_data;
```

Результат запроса:  
![task1_3](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task1_3.png)

 - Вывод данных из таблицы **person_skill**.

```sql
create or replace view task1_4 as SELECT * FROM person_skill;
```

Результат запроса:  
![task1_4](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task1_4.png)

 - Вывод данных из таблицы **skill**.

```sql
create or replace view task1_5 as SELECT * FROM skill;
```

Результат запроса:  
![task1_5](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task1_5.png)

 - Вывод данных из таблицы **meetup**.

```sql
create or replace view task1_6 as SELECT * FROM meetup;
```

Результат запроса:  
![task1_6](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task1_6.png)

 - Вывод данных из таблицы **inventory_person**.

```sql
create or replace view task1_7 as SELECT * FROM inventory_person;
```

Результат запроса:  
![task1_7](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task1_7.png)

 - Вывод данных из таблицы **inventory_person_items**.

```sql
create or replace view task1_8 as SELECT * FROM inventory_person_items;
```

Результат запроса:  
![task1_8](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task1_8.png)

 - Вывод данных из таблицы **item**.

```sql
create or replace view task1_9 as SELECT * FROM item;
```

Результат запроса:  
![task1_9](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task1_9.png)

### 2. Сделать выборку данных из одной таблицы при нескольких условиях, с использованием логических операций, **LIKE**, **BETWEEN**, **IN** 

 - Вывод персонажей, чьё здоровье находится в диапазоне между 30 и 50.

```sql
create or replace view task2_1 as SELECT * FROM person WHERE health BETWEEN 150 AND 170;
```
Результат запроса:   
![task2_1](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task2_1.png)

 - Вывод информации о пользователях, чей никнейм начинаются на 'dec'.

```sql
create or replace view task2_2 as SELECT * FROM user_data WHERE nickname LIKE 'dec%';
```

Результат запроса:  
![task2_2](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task2_2.png)

 - Вывод вещей из инвентарей с id '2', '212' и '1212'.

```sql
create or replace view task2_3 as SELECT * FROM inventory_person_items WHERE inventory_person_id IN ('2', '212', '1212');
```

Результат запроса:  
![task2_3](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task2_3.png)

### 3. Создать в запросе вычисляемое поле

 - Запрос рассчитывает количество суток, прошедших между первым получением предмета и его последним получением.

```sql
create or replace view task3 as SELECT inventory_person_id, add_date, update_date, extract(epoch FROM update_date - 
add_date)/3600/24 AS delta_days FROM inventory_person_items WHERE add_date != update_date ORDER BY delta_days;
```

Результат запроса:  
![task3](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task3.png)

### 4. Сделать выборку всех данных с сортировкой по нескольким полям

 - Сортировка данных в таблице с айтемами в инвентарях персонажей по типу айтема и его количеству в инвоентаре.

```sql
create or replace view task4 as SELECT * FROM inventory_person_items ORDER BY item_id, amount;
```

Результат запроса:  
![task4](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task4.png)

### 5. Создать запрос, вычисляющий несколько совокупных характеристик таблиц

 - Вывод среднего округлённого значения очков жизней и максимального количества опыта для существующих персонажей.

```sql
create or replace view task5 as SELECT ROUND(AVG(health), 2) AS "AVG Hp", MAX(experience) AS "MAX Exp" FROM person;
```

Результат запроса:  
![task5](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task5.png)

### 6. Сделать выборку данных из связанных таблиц

 - Делаем выборку из связанных таблиц class_of_person и skill. Выводим название класса. название скилла и его стоимость. 

```sql
create or replace view task6 as SELECT 
    c.name as "Class name", s.name as "Skill name", s.cost 
FROM class_of_person c 
    INNER JOIN skill s on s.class_of_person_id = c.id;
```

Результат запроса:  
![task6_1](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task6_1.png)

 - Делаем выборку из трёх таблиц person, user_data и class_of_person. Выводим всех персонажей юзера, показывая их класс.

```sql
create or replace view task6_2 as SELECT 
    p.id, ud.nickname, c.name 
FROM 
    person p 
    INNER JOIN user_data ud ON p.user_id = ud.id
    INNER JOIN class_of_person c ON p.class_of_person_id = c.id
ORDER BY ud.nickname;
```

Результат запроса:  
![task6_2](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task6_2.png)

### 7.Создать запрос, рассчитывающий совокупную характеристику с использованием группировки, наложите ограничение на результат группировки

 - Группировка вещей в инвентарях персонажей по id самих инвентарей, рассчет количества типов вещей в инвентаре и их общего количества, где сумма общего количества вещей должна быть больше 5.

```sql
create or replace view task7 as SELECT
    inventory_person_id, COUNT(ipi.inventory_person_id), SUM(amount) 
FROM inventory_person_items ipi 
GROUP BY ipi.inventory_person_id HAVING SUM(amount)>5
ORDER BY ipi.inventory_person_id
```

Результат запроса:  
![task7](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task_7.png)

### 8. Придумать и реализовать пример использования вложенного запроса

 - Вложенный запрос, который выводит количество персонажей, класс которых 'Archer'.

```sql
create or replace view task8 as SELECT COUNT(*) 
FROM person p 
WHERE class_of_person_id = (SELECT cop.id FROM class_of_person cop WHERE cop.name = 'Archer');
```

Результат запроса:  
![task8](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task8.png)

### 9. С помощью команды **INSERT** добавить в каждую таблицу по одной записи.

 - Добавление записи в каждую из таблиц, оформленное в виде процедуры.

```sql
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
```

### 10. С помощью оператора **UPDATE** измените значения нескольких полей у всех записей, отвечающих заданному условию

 - Обновляет баллы на картах лояльности, приравнивает их к 15000, и дату последнего изменения у конкретного покупателя  с id = 9.

```sql
CREATE OR REPLACE PROCEDURE task10() LANGUAGE plpgsql AS 
$$ BEGIN
    UPDATE person SET health = 200, update_date = now() WHERE health = 170 AND user_id = 2;
END $$;
CALL task10();
```

Результат до выполнения запроса:  
![task10_before](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task10_before.png)

Результат после выполнения запроса: 
![task10_after](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task10_after.png)

### 11. С помощью оператора **DELETE** удалить запись, имеющую максимальное (минимальное) значение некоторой совокупной характеристики

 - Удаляет персонажа который больше всех участвовал в схватках.

```sql
CREATE OR REPLACE PROCEDURE task11() LANGUAGE plpgsql AS 
$$ BEGIN
DELETE FROM person WHERE id = (SELECT person_id
                                FROM (SELECT person_id, count(*) AS meetup_count 
                                      FROM meetup
                                      GROUP BY person_id
                                      ORDER BY meetup_count DESC LIMIT 1) AS most_pupular_meetup_person);
END $$;
CALL task11();
```

Результат до выполнения запроса:  
![task11_before](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task11_before.png)

Результат после выполнения запроса:  
![task11_after](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task11_after.png)

### 12. С помощью оператора **DELETE** удалить записи в главной таблице, на которые не ссылается подчиненная таблица (используя вложенный запрос)

 - Удалим ранее созданный тестовый класс на который не ссылается ни один из персонажей.

```sql
CREATE OR REPLACE PROCEDURE task12() LANGUAGE plpgsql AS 
$$ BEGIN
    DELETE FROM class_of_person cop WHERE cop.id NOT IN (SELECT DISTINCT class_of_person_id FROM person);
END $$;
CALL task12();
```

Результат до выполнения запроса:   
![task12_before](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task12_before.png)

Результат после выполнения запроса:   
![task12_after](https://gitlab.icc.spbstu.ru/kostarev.vi/DB_lab_works/-/raw/master/lab3_sql_dml/images/task12_after.png)



