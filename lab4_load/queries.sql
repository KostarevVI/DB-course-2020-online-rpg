-- Запрос 1
-- Вывести информацию обо всех персонажах юзера не активных на протяжении года
-- на которо нападали больше чем нападал сам персонаж (параметр – никнейм)
EXPLAIN (ANALYZE, COSTS OFF)
    SELECT DISTINCT p.id, cap.name AS class FROM person p
          INNER JOIN class_of_person cap ON p.class_of_person_id = cap.id
          INNER JOIN user_data ud ON p.user_id = ud.id
          INNER JOIN meetup m on p.id = m.person_id OR p.id = m.enemy_id
          WHERE ud.nickname = 'Lamb5Wool' --Lamb5Wool/redispel
            AND p.update_date <= now() - '1 year'::interval
          GROUP BY p.id, cap.name, m.person_id, m.enemy_id
          HAVING count(m.enemy_id = p.id OR NULL) != 0
             AND count(m.person_id = p.id OR NULL)/count(m.enemy_id = p.id OR NULL) < 1;

PREPARE query1(varchar(20)) AS SELECT DISTINCT p.id, cap.name AS class FROM person p
          INNER JOIN class_of_person cap ON p.class_of_person_id = cap.id
          INNER JOIN user_data ud ON p.user_id = ud.id
          INNER JOIN meetup m on p.id = m.person_id OR p.id = m.enemy_id
          WHERE ud.nickname = $1
            AND p.update_date <= now() - '1 year'::interval
          GROUP BY p.id, cap.name, m.person_id, m.enemy_id
          HAVING count(m.enemy_id = p.id OR NULL) != 0
             AND count(m.person_id = p.id OR NULL)/count(m.enemy_id = p.id OR NULL) < 1;

EXPLAIN ANALYZE EXECUTE query1 ('redispel');

DEALLOCATE query1;

-- Запрос 2
-- Вывести ники юзеров-лидеров и кол-во требуемых результатов (победа/поражение/ничья) в инициированных
-- сражениях за последний год (параметр – тип результата сражения)
EXPLAIN (ANALYZE, COSTS OFF) SELECT ud.nickname, count(m.*) AS results FROM user_data ud
          INNER JOIN person p ON ud.id = p.user_id
          INNER JOIN meetup m ON p.id = m.person_id
          AND m.result = 'loose'
          AND m.meetup_date >= now() - '1 year'::interval
          AND m.meetup_date < now()
          GROUP BY ud.nickname
          ORDER BY results DESC;

PREPARE query2 AS SELECT ud.nickname, count(m.*) AS results FROM user_data ud
          INNER JOIN person p ON ud.id = p.user_id
          INNER JOIN meetup m ON p.id = m.person_id
          AND m.result = $1
          AND m.meetup_date >= now() - '1 year'::interval
          AND m.meetup_date < now()
          GROUP BY ud.nickname
          ORDER BY results DESC;

EXPLAIN ANALYZE EXECUTE query2 ('loose');

DEALLOCATE query2;


-- Запрос 3
-- Вывести и стакнуть артефакты из всех инвентарей персонажа (параметр – id персонажа)
EXPLAIN (ANALYZE, COSTS OFF) SELECT i.name, SUM(amount) FROM inventory_person_items ipi
          INNER JOIN item i on i.id = ipi.item_id
          INNER JOIN inventory_person ip on ipi.inventory_person_id = ip.id
          INNER JOIN person p on ip.person_id = p.id
          WHERE p.id = 1234 --1234/120007
          GROUP BY i.name;

PREPARE query3(bigint) AS SELECT i.name, SUM(amount) FROM inventory_person_items ipi
          INNER JOIN item i on i.id = ipi.item_id
          INNER JOIN inventory_person ip on ipi.inventory_person_id = ip.id
          INNER JOIN person p on ip.person_id = p.id
          WHERE p.id = $1
          GROUP BY i.name;

EXPLAIN ANALYZE EXECUTE query3 (1234);

DEALLOCATE query3;

-- Запрос 4
-- Вывести персонажей определённого класса которые прошли всю игру
-- (вкачали оба скилла, макс жизней, получили редкий айтем) (параметр – имя класса)
EXPLAIN (ANALYZE, COSTS OFF) SELECT ps.person_id FROM person_skill ps
    INNER JOIN skill s ON ps.skill_id = s.id
    INNER JOIN class_of_person cop on s.class_of_person_id = cop.id
    INNER JOIN person p ON ps.person_id = p.id
    INNER JOIN inventory_person ip ON p.id = ip.person_id
    INNER JOIN inventory_person_items ipi on ip.id = ipi.inventory_person_id
    WHERE cop.name = 'Archer' AND health = 300 AND ipi.item_id = 11
    GROUP BY ps.person_id HAVING count(equiped=true OR NULL)=2;

PREPARE query4(varchar(30)) AS SELECT ps.person_id FROM person_skill ps
    INNER JOIN skill s ON ps.skill_id = s.id
    INNER JOIN class_of_person cop on s.class_of_person_id = cop.id
    INNER JOIN person p ON ps.person_id = p.id
    INNER JOIN inventory_person ip ON p.id = ip.person_id
    INNER JOIN inventory_person_items ipi on ip.id = ipi.inventory_person_id
    WHERE cop.name = $1 AND health = 300 AND ipi.item_id = 11
    GROUP BY ps.person_id HAVING count(equiped=true OR NULL)=2;

DEALLOCATE query4;

EXPLAIN ANALYZE EXECUTE query4 ('Archer');

-- Запрос 5
-- Вывести рейтинг игроков (ники) по полученным за определённый промежуток времени редким артефактам
-- для всех персонажей (параметр – даты)
EXPLAIN (ANALYZE, COSTS OFF) SELECT ud.nickname, sum(ipi.amount) FROM inventory_person_items ipi
    INNER JOIN inventory_person ip on ip.id = ipi.inventory_person_id
    INNER JOIN person p on p.id = ip.person_id
    INNER JOIN user_data ud on p.user_id = ud.id
    WHERE ipi.update_date < now()
      AND ipi.update_date >= now() - '12 months'::interval
      AND ipi.add_date < now()
      AND ipi.add_date >= now() - '12 months'::interval
      AND ipi.item_id = 11
    GROUP BY ud.nickname
    ORDER BY sum(ipi.amount) DESC;

SET work_mem = '500MB';

RESET work_mem;

ANALYZE;

PREPARE query5 AS SELECT ud.nickname, sum(ipi.amount) FROM inventory_person_items ipi
    INNER JOIN inventory_person ip on ip.id = ipi.inventory_person_id
    INNER JOIN person p on p.id = ip.person_id
    INNER JOIN user_data ud on p.user_id = ud.id
    WHERE ipi.update_date < $1
      AND ipi.update_date >= $1 - '12 months'::interval
      AND ipi.add_date < $1
      AND ipi.add_date >= $1 - '12 months'::interval
      AND ipi.item_id = 11
    GROUP BY ud.nickname
    ORDER BY sum(ipi.amount) DESC;

DEALLOCATE query5;

EXPLAIN ANALYZE EXECUTE query5 (now());

SELECT schemaname,tablename,indexname FROM pg_indexes;

-- делать аналайз перед expain
-- вет тулы для анализа учздшт
-- увеличить память в постгресе
-- workmem кэш/буфер сайз
-- файл конфигурации