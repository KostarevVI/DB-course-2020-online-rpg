--DELETE FROM inventory_person_items WHERE inventory_person_id =

-- Запрос 1
WITH inventory_to_person_half_year_table AS (
	SELECT ip.person_id, item_id, MIN(add_date) AS add_date FROM inventory_person_items ipi
	INNER JOIN inventory_person ip ON ipi.inventory_person_id = ip.id
	WHERE add_date > now()::date - '6 month'::interval
	GROUP BY ip.person_id, item_id
	ORDER BY ip.person_id, item_id
), gain_rare_item_every_month AS (
	SELECT person_id FROM inventory_to_person_half_year_table
	WHERE (add_date >= (now()::date - '1 month'::interval)
		   AND add_date < now()::date)
	AND person_id IN (
		SELECT person_id FROM inventory_to_person_half_year_table
		WHERE (add_date >= (now()::date - '2 month'::interval)
			   AND add_date < (now()::date - '1 month'::interval))
		AND person_id IN (
			SELECT person_id FROM inventory_to_person_half_year_table
			WHERE (add_date >= (now()::date - '3 month'::interval)
				   AND add_date < (now()::date - '2 month'::interval))
			AND person_id IN (
					SELECT person_id FROM inventory_to_person_half_year_table
					WHERE (add_date >= (now()::date - '4 month'::interval)
						   AND add_date < (now()::date - '3 month'::interval))
					AND person_id IN (
						SELECT person_id FROM inventory_to_person_half_year_table
						WHERE (add_date >= (now()::date - '5 month'::interval)
							   AND add_date < (now()::date - '4 month'::interval))
						AND person_id IN (
								SELECT person_id FROM inventory_to_person_half_year_table
								WHERE add_date >= (now()::date - '6 month'::interval)
								AND add_date < (now()::date - '5 month'::interval)
							   )
						)
				)
		)
	)
)

--SELECT * FROM person WHERE id IN (SELECT * FROM gain_rare_item_every_month)

SELECT ip.person_id, inventory_person_id, item_id, MIN(add_date) AS add_date FROM inventory_person_items ipi
	INNER JOIN inventory_person ip ON ipi.inventory_person_id = ip.id
    WHERE ip.person_id IN (SELECT * FROM gain_rare_item_every_month)
	GROUP BY ip.person_id, inventory_person_id, item_id
	ORDER BY ip.person_id, inventory_person_id, item_id


-- Запрос 2
-- Вставка айтемов
--INSERT INTO inventory_person_items(item_id, inventory_person_id, add_date, is_deleted, amount) VALUES
--(5, 398, now()::date - '3 month'::interval - '5 day'::interval, False, 1);
-- Вставка сражений
--INSERT INTO meetup(person_id, result, meetup_date, enemy_id) VALUES
--(1234, 'win', now(), 1);

WITH person_win_meetup_count AS
(
	SELECT person_id, count(*) AS wins_count FROM
	(
		SELECT person_id FROM meetup
		WHERE meetup_date > now()::date - '1 year'::interval
		AND result = 'win'
		UNION ALL
		SELECT enemy_id FROM meetup
		WHERE meetup_date > now()::date - '1 year'::interval
		AND result = 'loose' AND enemy_id IS NOT NULL
	) AS winners
	GROUP BY person_id ORDER BY wins_count DESC
), inventory_to_person_half_year_table AS
(
	SELECT ip.person_id, SUM(amount) AS collected_items FROM inventory_person_items ipi
	INNER JOIN inventory_person ip ON ipi.inventory_person_id = ip.id
	WHERE add_date > now()::date - '1 year'::interval
	GROUP BY ip.person_id
	ORDER BY collected_items DESC
)

--SELECT * FROM person_win_meetup_count

--SELECT * FROM inventory_to_person_half_year_table

--SELECT person_id, (pwmc.wins_count::real/iphyt.collected_items::real) AS relation FROM person_win_meetup_count pwmc
--INNER JOIN inventory_to_person_half_year_table iphyt USING (person_id) ORDER BY relation DESC LIMIT 5

/*SELECT * FROM meetup
		WHERE meetup_date > now()::date - '1 year'::interval
		  AND person_id IN (SELECT person_id FROM (SELECT person_id, (pwmc.wins_count::real/iphyt.collected_items::real) AS relation FROM person_win_meetup_count pwmc
		      INNER JOIN inventory_to_person_half_year_table iphyt USING (person_id) ORDER BY relation DESC LIMIT 5) as p1)
		  AND result = 'win'
		UNION ALL
		SELECT * FROM meetup
		WHERE meetup_date > now()::date - '1 year'::interval
		  AND enemy_id IN (SELECT person_id FROM (SELECT person_id, (pwmc.wins_count::real/iphyt.collected_items::real) AS relation FROM person_win_meetup_count pwmc
		  INNER JOIN inventory_to_person_half_year_table iphyt USING (person_id) ORDER BY relation DESC LIMIT 5) as p2)
		AND result = 'loose' AND enemy_id IS NOT NULL
 */

SELECT person_id, item_id, amount FROM inventory_person_items ipi2
    INNER JOIN inventory_person ip2 ON ipi2.inventory_person_id = ip2.id
	WHERE add_date > now()::date - '1 year'::interval
	  AND ip2.person_id IN (SELECT person_id FROM (SELECT person_id, (pwmc.wins_count::real/iphyt.collected_items::real) AS relation FROM person_win_meetup_count pwmc
		  INNER JOIN inventory_to_person_half_year_table iphyt USING (person_id) ORDER BY relation DESC LIMIT 5) as p1)



SELECT i.name, amount FROM inventory_person_items ipi
                  INNER JOIN item i on i.id = ipi.item_id
                  INNER JOIN inventory_person ip on ipi.inventory_person_id = ip.id
                  INNER JOIN person p on ip.person_id = p.id AND p.id = 1