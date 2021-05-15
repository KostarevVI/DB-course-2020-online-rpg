from random import Random
import psycopg2


class DBFunctions():

    def __init__(self):
        self.connection = None

    def connect_to_database(self):
        self.connection = psycopg2.connect(dbname='database_for_game_big',
                                           user='postgres',
                                           password='6559',
                                           host='localhost')
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    def get_data_for_request(self, nickname, battle_result, id_of_person, class_of_person, item_date):
        self.cursor.execute("SELECT nickname FROM user_data;")
        result = self.cursor.fetchall()
        for i in range(0, len(result)):
            nickname.append(result[i][0])

        self.cursor.execute("SELECT result FROM meetup;")
        result = self.cursor.fetchall()
        for i in range(0, len(result)):
            battle_result.append(result[i][0])

        self.cursor.execute("SELECT id FROM person;")
        result = self.cursor.fetchall()
        for i in range(0, len(result)):
            id_of_person.append(result[i][0])

        self.cursor.execute("SELECT name FROM class_of_person;")
        result = self.cursor.fetchall()
        for i in range(0, len(result)):
            class_of_person.append(result[i][0])

        self.cursor.execute("SELECT add_date FROM inventory_person_items;")
        result = self.cursor.fetchall()
        for i in range(0, len(result)):
            item_date.append(result[i][0])

    def execute_random_query_and_get_time(self, const_and_data):
        random = Random().randint(1, 5)

        # Запрос 1
        # Вывести информацию обо всех персонажах юзера не активных на протяжении года
        # на которо нападали больше чем нападал сам персонаж (параметр – никнейм)
        query_1 = "SELECT DISTINCT p.id, cap.name AS class FROM person p " \
                  "INNER JOIN class_of_person cap ON p.class_of_person_id = cap.id " \
                  "INNER JOIN user_data ud ON p.user_id = ud.id " \
                  "INNER JOIN meetup m on p.id = m.person_id OR p.id = m.enemy_id " \
                  "WHERE ud.nickname = %(nickname)s " \
                  "AND p.update_date <= now() - '1 year'::interval " \
                  "GROUP BY p.id, cap.name, m.person_id, m.enemy_id " \
                  "HAVING count(m.enemy_id = p.id OR NULL) != 0 " \
                  "AND count(m.person_id = p.id OR NULL)/count(m.enemy_id = p.id OR NULL) < 1;"

        # Запрос 2
        # Вывести ники юзеров-лидеров и кол-во требуемых результатов (победа/поражение/ничья) в инициированных
        # сражениях за последний год (параметр – тип результата сражения)
        query_2 = "SELECT ud.nickname, count(m.*) AS results FROM user_data ud " \
                  "INNER JOIN person p ON ud.id = p.user_id " \
                  "INNER JOIN meetup m ON p.id = m.person_id " \
                  "AND m.result = %(battle_result)s " \
                  "AND m.meetup_date >= now() - '1 year'::interval " \
                  "AND m.meetup_date < now() " \
                  "GROUP BY ud.nickname " \
                  "ORDER BY results DESC;"

        # Запрос 3
        # Вывести и стакнуть артефакты из всех инвентарей персонажа (параметр – id персонажа)
        query_3 = "SELECT i.name, SUM(amount) FROM inventory_person_items ipi " \
                  "INNER JOIN item i on i.id = ipi.item_id " \
                  "INNER JOIN inventory_person ip on ipi.inventory_person_id = ip.id " \
                  "INNER JOIN person p on ip.person_id = p.id " \
                  "WHERE p.id = %(id_of_person)s " \
                  "GROUP BY i.name;"

        # Запрос 4
        # Вывести персонажей определённого класса которые прошли всю игру
        # (вкачали оба скилла, макс жизней, получили редкий айтем) (параметр – имя класса)
        query_4 = "SELECT ps.person_id FROM person_skill ps " \
                  "INNER JOIN skill s ON ps.skill_id = s.id " \
                  "INNER JOIN class_of_person cop on s.class_of_person_id = cop.id " \
                  "INNER JOIN person p ON ps.person_id = p.id " \
                  "INNER JOIN inventory_person ip ON p.id = ip.person_id " \
                  "INNER JOIN inventory_person_items ipi on ip.id = ipi.inventory_person_id " \
                  "WHERE cop.name = %(class_of_person)s AND health = 300 AND ipi.item_id = 11 " \
                  "GROUP BY ps.person_id HAVING count(equiped=true OR NULL)=2;"

        # Запрос 5
        # Вывести рейтинг игроков (ники) по полученным за определённый месяц редким артефактам
        # для всех персонажей (параметр – даты)
        query_5 = "SELECT ud.nickname, sum(ipi.amount) FROM inventory_person_items ipi " \
                  "INNER JOIN inventory_person ip on ip.id = ipi.inventory_person_id " \
                  "INNER JOIN person p on p.id = ip.person_id " \
                  "INNER JOIN user_data ud on p.user_id = ud.id " \
                  "WHERE ipi.update_date < %(item_date)s + '1 year'::interval " \
                  "AND ipi.update_date >= %(item_date)s " \
                  "AND ipi.add_date < %(item_date)s + '1 year'::interval " \
                  "AND ipi.add_date >= %(item_date)s " \
                  "AND ipi.item_id = 11 " \
                  "GROUP BY ud.nickname " \
                  "ORDER BY sum(ipi.amount) DESC;"

        queries = (query_1, query_2, query_3, query_4, query_5)

        if random == 1:
            nickname = const_and_data.nickname[Random().randint(0, (len(const_and_data.nickname) - 1))]
            self.cursor.execute("EXPLAIN ANALYZE " + queries[random - 1], {"nickname": nickname})

        if random == 2:
            battle_result = const_and_data.battle_result[Random().randint(0, len(const_and_data.battle_result) - 1)]
            self.cursor.execute("EXPLAIN ANALYZE " + queries[random - 1], {"battle_result": battle_result})

        if random == 3:
            id_of_person = const_and_data.id_of_person[Random().randint(0, len(const_and_data.id_of_person) - 1)]
            self.cursor.execute("EXPLAIN ANALYZE " + queries[random - 1], {"id_of_person": id_of_person})

        if random == 4:
            class_of_person = const_and_data.class_of_person[Random().randint(0, (len(const_and_data.class_of_person) - 1))]
            self.cursor.execute("EXPLAIN ANALYZE " + queries[random - 1], {"class_of_person": class_of_person})

        if random == 5:
            item_date = const_and_data.item_date[Random().randint(0, (len(const_and_data.item_date) - 1))]
            self.cursor.execute("EXPLAIN ANALYZE " + queries[random - 1], {"item_date": item_date})

        res = self.cursor.fetchall()
        self.connection.commit()
        return float(res[-1][0].split(" ")[2])

    def add_indexes(self):
        self.cursor.execute("CREATE INDEX IF NOT EXISTS meetup_person_idx ON meetup(person_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS meetup_enemy_idx ON meetup(enemy_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS meetup_date_idx ON meetup(meetup_date);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS inventory_person_item_inventory_person_idx "
                            "ON inventory_person_items(inventory_person_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS inventory_person_person_idx ON inventory_person(person_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS person_skill_skill_idx ON person_skill(skill_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS person_health_idx ON person(health);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS inventory_person_items_item_addupdate_date_idx "
                            "ON inventory_person_items(item_id, add_date, update_date);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS person_user_idx ON person(user_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS person_class_idx ON person(class_of_person_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS user_nickname_idx ON user_data(nickname);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS inventory_person_item_inventory_person_idx "
                            "ON inventory_person_items(inventory_person_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS inventory_person_item_inventory_person_item_idx "
                            "ON inventory_person_items(inventory_person_id, item_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS inventory_person_item_idx ON inventory_person_items(item_id);")

    def drop_index_if_exists(self):
        self.cursor.execute("DROP INDEX IF EXISTS meetup_person_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS meetup_enemy_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS meetup_date_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS inventory_person_item_inventory_person_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS inventory_person_person_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS person_skill_skill_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS person_health_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS inventory_person_items_item_addupdate_date_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS person_user_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS person_class_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS user_nickname_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS inventory_person_item_inventory_person_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS inventory_person_item_inventory_person_item_idx;")
        self.cursor.execute("DROP INDEX IF EXISTS inventory_person_item_idx;")

    def prepare_queries(self):
        # Вывести информацию обо всех персонажах юзера не активных на протяжении года
        # на которо нападали больше чем нападал сам персонаж (параметр – никнейм)
        self.cursor.execute("PREPARE query1 (varchar(20)) AS "
                            "SELECT DISTINCT p.id, cap.name AS class FROM person p "
                            "INNER JOIN class_of_person cap ON p.class_of_person_id = cap.id "
                            "INNER JOIN user_data ud ON p.user_id = ud.id "
                            "INNER JOIN meetup m on p.id = m.person_id OR p.id = m.enemy_id "
                            "WHERE ud.nickname = $1 "
                            "AND p.update_date <= now() - '1 year'::interval "
                            "GROUP BY p.id, cap.name, m.person_id, m.enemy_id "
                            "HAVING count(m.enemy_id = p.id OR NULL) != 0 "
                            "AND count(m.person_id = p.id OR NULL)/count(m.enemy_id = p.id OR NULL) < 1;")

        # Вывести ники юзеров-лидеров и кол-во требуемых результатов (победа/поражение/ничья) в инициированных
        # сражениях за последний год (параметр – тип результата сражения)
        self.cursor.execute("PREPARE query2 AS "
                            "SELECT ud.nickname, count(m.*) AS results FROM user_data ud "
                            "INNER JOIN person p ON ud.id = p.user_id "
                            "INNER JOIN meetup m ON p.id = m.person_id "
                            "AND m.result = $1 "
                            "AND m.meetup_date >= now() - '1 year'::interval "
                            "AND m.meetup_date < now() "
                            "GROUP BY ud.nickname "
                            "ORDER BY results DESC;")

        # Вывести и стакнуть артефакты из всех инвентарей персонажа (параметр – id персонажа)
        self.cursor.execute("PREPARE query3 (bigint) AS "
                            "SELECT i.name, SUM(amount) FROM inventory_person_items ipi "
                            "INNER JOIN item i on i.id = ipi.item_id "
                            "INNER JOIN inventory_person ip on ipi.inventory_person_id = ip.id "
                            "INNER JOIN person p on ip.person_id = p.id "
                            "WHERE p.id = $1 "
                            "GROUP BY i.name;")

        # Вывести персонажей определённого класса которые прошли всю игру
        # (вкачали оба скилла, макс жизней, получили редкий айтем) (параметр – имя класса)
        self.cursor.execute("PREPARE query4 (varchar(30)) AS "
                            "SELECT ps.person_id FROM person_skill ps "
                            "INNER JOIN skill s ON ps.skill_id = s.id "
                            "INNER JOIN class_of_person cop on s.class_of_person_id = cop.id "
                            "INNER JOIN person p ON ps.person_id = p.id "
                            "INNER JOIN inventory_person ip ON p.id = ip.person_id "
                            "INNER JOIN inventory_person_items ipi on ip.id = ipi.inventory_person_id "
                            "WHERE cop.name = $1 AND health = 300 AND ipi.item_id = 11 "
                            "GROUP BY ps.person_id HAVING count(equiped=true OR NULL)=2;")

        # Вывести рейтинг игроков (ники) по полученным за определённый месяц редким артефактам
        # для всех персонажей (параметр – даты)
        self.cursor.execute("PREPARE query5 AS "
                            "SELECT ud.nickname, sum(ipi.amount) FROM inventory_person_items ipi " 
                            "INNER JOIN inventory_person ip on ip.id = ipi.inventory_person_id " 
                            "INNER JOIN person p on p.id = ip.person_id " 
                            "INNER JOIN user_data ud on p.user_id = ud.id " 
                            "WHERE ipi.update_date < $1::timestamp + '1 year'::interval " 
                            "AND ipi.update_date >= $1 " 
                            "AND ipi.add_date < $1 + '1 year'::interval " 
                            "AND ipi.add_date >= $1 " 
                            "AND ipi.item_id = 11 " 
                            "GROUP BY ud.nickname " 
                            "ORDER BY sum(ipi.amount) DESC;")

        self.connection.commit()

    def execute_random_query_with_optimisation_and_get_time(self, const_and_data):
        random = Random().randint(1, 5)

        if random == 1:
            nickname = const_and_data.nickname[Random().randint(0, (len(const_and_data.nickname) - 1))]
            self.cursor.execute("EXPLAIN ANALYZE EXECUTE query1 ('{}');".format(nickname))

        if random == 2:
            battle_result = const_and_data.battle_result[Random().randint(0, len(const_and_data.battle_result) - 1)]
            self.cursor.execute("EXPLAIN ANALYZE EXECUTE query2 ('{}');".format(battle_result))

        if random == 3:
            id_of_person = const_and_data.id_of_person[Random().randint(0, len(const_and_data.id_of_person) - 1)]
            self.cursor.execute("EXPLAIN ANALYZE EXECUTE query3 ({});".format(id_of_person))

        if random == 4:
            class_of_person = \
                const_and_data.class_of_person[Random().randint(0, (len(const_and_data.class_of_person) - 1))]
            self.cursor.execute("EXPLAIN ANALYZE EXECUTE query4 ('{}');".format(class_of_person))

        if random == 5:
            item_date = const_and_data.item_date[Random().randint(0, (len(const_and_data.item_date) - 1))]
            self.cursor.execute("EXPLAIN ANALYZE EXECUTE query5 ('{}');".format(item_date))

        res = self.cursor.fetchall()
        return float(res[-1][0].split(" ")[2])
