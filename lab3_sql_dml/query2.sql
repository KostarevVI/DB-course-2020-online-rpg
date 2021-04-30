--INSERT INTO inventory_person_items(item_id, inventory_person_id, add_date, is_deleted, amount) VALUES 
--(5, 398, now()::date - '3 month'::interval - '5 day'::interval, False, 1);

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

SELECT person_id, (pwmc.wins_count::real/iphyt.collected_items::real) AS relation FROM person_win_meetup_count pwmc
INNER JOIN inventory_to_person_half_year_table iphyt USING (person_id) ORDER BY relation DESC LIMIT 5

