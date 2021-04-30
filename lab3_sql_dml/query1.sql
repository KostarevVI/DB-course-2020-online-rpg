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

SELECT * FROM person WHERE id IN (SELECT * FROM gain_rare_item_every_month)

