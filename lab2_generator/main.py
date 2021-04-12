import datetime
import psycopg2
import random
import argparse
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

'''
connection = psycopg2.connect(
    dbname=config.get("database_for_game", "dbname"),
    user=config.get("postgres", "user"),
    password=config.get("6559", "password"))
'''

connection = psycopg2.connect(dbname='database_for_game',
                              user='postgres',
                              password='6559',
                              host='localhost')

cursor = connection.cursor()

letters = 'qwertyuiopasdfghjklzxcvbnm'

today = datetime.datetime.today()

item_ids = ()
inventory_person_ids = ()
class_of_person_ids = ()
user_data_ids = ()
person_ids = ()

item_array = []
class_of_person_array = []
skill_array = []
user_data_array = []
person_array = []
inventory_person_array = []
meetup_array = []
person_skill_array = []
inventory_person_items_update_array = []
inventory_person_items_insert_array = []
inventory_person_items_update_tuple = []

items = open("input/items.txt", "r").readlines()
classes = open("input/classes.txt", "r").readlines()
skills = open("input/skills.txt", "r").readlines()
nicknames = open("input/nicknames.txt", "r").readlines()
email_domains = open("input/email_domains.txt", "r").readlines()


def add_on_update(inventory_person_id, item_id, current_item):
    amount_item = int(current_item[4]) + 1
    update_date = random_date(current_item[5], today)
    inventory_person_items_update_array.append([amount_item,
                                                update_date,
                                                inventory_person_id[0],
                                                item_id[0]])


def amount_of_insert_and_updates_for_person(inventory_person_id, insert_list, update_list):
    update_items_dictionary = {}
    insert_items = 0
    for element in update_list:
        if element[2] == inventory_person_id:
            if update_items_dictionary.get(element[3]) is not None:
                if update_items_dictionary[element[3]] < element[0]:
                    update_items_dictionary[element[3]] = element[0]
            else:
                update_items_dictionary[element[3]] = element[0]

    for element in insert_list:
        if element[0] == inventory_person_id and update_items_dictionary.get(element[1]) is None:
            insert_items += 1

    total_amount = insert_items + sum(update_items_dictionary.values())
    return total_amount


def list_to_tuple(update_list):
    list_temp = []
    for element in update_list:
        list_temp.append(tuple(element))
    return tuple(list_temp)


def random_string(length):
    rnd_str = ''
    for i in range(int(length)):
        rnd_str += random.choice(letters)
    return rnd_str


def random_date(start_date: object, end_date: object) -> object:
    date_delta = end_date - start_date
    days_delta = date_delta.days
    if days_delta == 0:
        return today
    else:
        days_random = random.randrange(days_delta)
        rnd_date = start_date + datetime.timedelta(days=days_random)
        return rnd_date


def generate_item():
    global item_ids
    cursor.execute('SELECT name FROM item')
    item_names = cursor.fetchall()
    for element in items:
        element = element.replace("\n", "")
        if element not in item_names:
            description = random_string(random.randint(5, 15))
            item_array.append((element, description))

    if item_array:
        temp_list = ','.join(['%s'] * len(item_array))
        cursor.execute(
            'INSERT INTO \"item\"(name, description) VALUES {} ON CONFLICT DO NOTHING'.format(temp_list), item_array)
    cursor.execute('SELECT id FROM item')
    item_ids = cursor.fetchall()


def generate_class_of_person():
    global class_of_person_ids
    cursor.execute('SELECT name FROM class_of_person')
    class_name = cursor.fetchall()
    for element in classes:
        element = element.replace("\n", "")
        if element not in class_name:
            description = random_string(random.randint(5, 15))
            class_of_person_array.append((element, description))

    if class_of_person_array:
        temp_list = ','.join(['%s'] * len(class_of_person_array))
        cursor.execute('INSERT INTO \"class_of_person\"(name, description) VALUES {} ON CONFLICT DO NOTHING'
                       .format(temp_list), class_of_person_array)
    cursor.execute('SELECT id FROM class_of_person')
    class_of_person_ids = cursor.fetchall()
    generate_skill()


def generate_skill():
    cursor.execute('SELECT name FROM skill')
    skill_name = cursor.fetchall()
    for index, element in enumerate(skills):
        element = element.replace("\n", "")
        if element not in skill_name:
            description = random_string(random.randint(5, 15))
            cost = 50 * (index % 2 + 1)
            cursor.execute('SELECT id FROM class_of_person WHERE name=\'{}\''.format(element.split()[0]))
            class_of_person_id = cursor.fetchone()[0]
            skill_array.append((element, description, cost, class_of_person_id))

    if skill_array:
        temp_list = ','.join(['%s'] * len(skill_array))
        cursor.execute('INSERT INTO skill(name, description, cost, class_of_person_id) VALUES {} '
                       'ON CONFLICT DO NOTHING'.format(temp_list), skill_array)


def generate_person_skill():
    cursor.execute('SELECT person_id FROM person_skill')
    person_id_in_person_skill = cursor.fetchall()

    for element in person_ids:
        if element not in person_id_in_person_skill:
            person_id = element[0]
            cursor.execute('SELECT class_of_person_id FROM person WHERE id=\'{}\''.format(person_id))
            person_class = cursor.fetchall()
            cursor.execute('SELECT id FROM skill WHERE class_of_person_id={}'.format(person_class[0][0]))
            class_skills = cursor.fetchall()
            for skill_temp in class_skills:
                skill_id = skill_temp[0]
                person_skill_array.append((person_id, skill_id, False))

    if person_skill_array:
        temp_list = ','.join(['%s'] * len(person_skill_array))
        cursor.execute('INSERT INTO person_skill VALUES {}'
                       .format(temp_list), person_skill_array)


def generate_user_data(amount):
    global user_data_ids
    for i in range(int(amount)):
        nickname = random.choice(nicknames)
        nickname = nickname.replace("\n", "")
        password = random_string(random.randint(10, 16))
        email_domain = random.choice(email_domains)
        email_domain = email_domain.replace("\n", "")
        email = random_string(random.randint(10, 20)) + email_domain
        user_data_array.append((email, password, nickname[:20]))

    if user_data_array:
        temp_list = ','.join(['%s'] * len(user_data_array))
        cursor.execute('INSERT INTO user_data(email, password, nickname) VALUES {} ON CONFLICT DO NOTHING'
                       .format(temp_list), user_data_array)
    cursor.execute('SELECT id FROM user_data')
    user_data_ids = cursor.fetchall()


def generate_person(amount):
    global person_ids
    global user_data_ids
    for i in range(int(amount)):
        class_of_person_id = random.choice(class_of_person_ids)[0]
        health = 10 * random.randint(10, 30)
        experience = 5 * random.randint(0, 19)
        update_date = random_date(today - datetime.timedelta(days=2 * 365),
                                  today)
        is_enemy = True

        cursor.execute('SELECT id FROM user_data')
        user_data_ids = cursor.fetchall()

        user_id = [None]

        if i % 10 != 0:
            user_id = random.choice(user_data_ids)
            is_enemy = False
        person_array.append((class_of_person_id, health, experience, user_id[0], update_date, is_enemy))

    if person_array:
        temp_list = ','.join(['%s'] * len(person_array))
        cursor.execute(
            'INSERT INTO person (class_of_person_id, health, experience, user_id, update_date, is_enemy) '
            'VALUES {}'.format(temp_list), person_array)

    cursor.execute('SELECT id FROM person')
    person_ids = cursor.fetchall()
    generate_inventory_person()
    generate_person_skill()


def generate_inventory_person():
    global inventory_person_ids
    cursor.execute('SELECT person_id FROM inventory_person')
    person_id_in_inventory_person = cursor.fetchall()

    for element in person_ids:
        if element not in person_id_in_inventory_person:
            person_id = element[0]
            inventory_size = 5 * random.randint(2, 8)
            inventory_person_array.append((person_id, inventory_size))

    if inventory_person_array:
        temp_list = ','.join(['%s'] * len(inventory_person_array))
        cursor.execute('INSERT INTO inventory_person(person_id, inventory_size) VALUES {}'
                       .format(temp_list), inventory_person_array)
    cursor.execute('SELECT id FROM inventory_person')
    inventory_person_ids = cursor.fetchall()


def generate_meetup(amount):
    global person_ids
    cursor.execute('SELECT id FROM person')
    person_ids = cursor.fetchall()

    for i in range(int(amount)):
        person_id = random.choice(person_ids)
        index = person_ids.index(person_id)
        person_ids_for_enemy = person_ids[:index] + person_ids[index + 1:]
        enemy_id = random.choice(person_ids_for_enemy)
        cursor.execute('SELECT update_date FROM person WHERE id=\'{}\''.format(person_id[0]))
        person_update_date = cursor.fetchall()
        cursor.execute('SELECT update_date FROM person WHERE id=\'{}\''.format(enemy_id[0]))
        enemy_update_date = cursor.fetchall()
        if person_update_date <= enemy_update_date:
            meetup_date = person_update_date
        else:
            meetup_date = enemy_update_date

        result = random.choice(('win', 'loose', 'draw'))
        meetup_array.append((person_id[0], result, meetup_date[0][0], enemy_id[0]))

    if meetup_array:
        temp_list = ','.join(['%s'] * len(meetup_array))
        cursor.execute('INSERT INTO meetup (person_id, result, meetup_date, enemy_id) VALUES {}'
                       .format(temp_list), meetup_array)


def generate_inventory_person_items(amount):
    global inventory_person_ids
    cursor.execute('SELECT id FROM inventory_person')
    inventory_person_ids = cursor.fetchall()

    for i in range(int(amount)):
        inventory_person_id = random.choice(inventory_person_ids)
        item_id = random.choice(item_ids)

        # check plenum
        cursor.execute('SELECT * FROM inventory_person WHERE id=\'{}\''.format(inventory_person_id[0]))
        inventory_person_tuple = cursor.fetchone()
        cursor.execute('SELECT amount FROM inventory_person_items WHERE inventory_person_id=\'{}\''
                       .format(inventory_person_id[0]))
        all_amount = cursor.fetchall()

        current_amount_of_items = sum(element[0] for element in all_amount) + \
            amount_of_insert_and_updates_for_person(inventory_person_id[0],
                                                    inventory_person_items_insert_array,
                                                    inventory_person_items_update_array)

        if current_amount_of_items < inventory_person_tuple[2]:
            cursor.execute('SELECT * FROM inventory_person_items WHERE inventory_person_id=\'{}\' AND item_id=\'{}\''.
                           format(inventory_person_id[0], item_id[0]))
            current_item = cursor.fetchone()

            cursor.execute('SELECT update_date FROM person WHERE id=\'{}\''.format(inventory_person_tuple[1]))
            person_update_date = cursor.fetchone()

            is_deleted = False

            if (current_item and not bool(current_item[3])) or (inventory_person_id[0],
                                                                item_id[0],
                                                                person_update_date[0],
                                                                is_deleted,
                                                                1,
                                                                person_update_date[0]) \
                    in inventory_person_items_insert_array:
                # если такой айтем уже в инвентаре игрока – апдейтим его
                if not current_item:
                    current_item = (inventory_person_id[0],
                                    item_id[0],
                                    person_update_date[0],
                                    is_deleted,
                                    1,
                                    person_update_date[0])

                if inventory_person_items_update_array:
                    flag = False
                    # перебираем все кортежи на апдейт и если наш есть – amount+1
                    for index, element in enumerate(inventory_person_items_update_array):
                        if inventory_person_id[0] == element[2] and item_id[0] == element[3]:
                            flag = True
                            inventory_person_items_update_array[index][0] += 1
                    # если кортежа на апдейт ещё нет в списке, но список не пуст – добавляем этот кортеж
                    if not flag:
                        add_on_update(inventory_person_id, item_id, current_item)
                # если список пустой – добавляем кортеж на апдейт
                else:
                    add_on_update(inventory_person_id, item_id, current_item)

            # если нету такого айтема в инвентаре у игрока – добавляем его туда
            else:
                add_date = person_update_date[0]
                amount_item = 1
                update_date = add_date
                inventory_person_items_insert_array.append((inventory_person_id[0],
                                                            item_id[0],
                                                            add_date,
                                                            is_deleted,
                                                            amount_item,
                                                            update_date))

    if inventory_person_items_insert_array:
        temp_list = ','.join(['%s'] * len(inventory_person_items_insert_array))
        cursor.execute(
            'INSERT INTO inventory_person_items VALUES {}'.format(temp_list), inventory_person_items_insert_array)

    if inventory_person_items_update_array:
        temp_list = ','.join(['%s'] * len(inventory_person_items_update_array))
        cursor.execute('UPDATE inventory_person_items AS t ' \
                       'SET amount = c.amount, update_date = c.update_date ' \
                       'FROM (VALUES {}) as c(amount, update_date, inventory_person_id, item_id) ' \
                       'WHERE c.inventory_person_id = t.inventory_person_id AND c.item_id = t.item_id'
                       .format(temp_list), list_to_tuple(inventory_person_items_update_array))


def generate_data(args):
    generate_item()
    generate_class_of_person()

    if args.user_data is not None:
        generate_user_data(arguments.user_data)

    if args.persons is not None:
        generate_person(arguments.persons)

    if args.inventory_person_items is not None:
        generate_inventory_person_items(arguments.inventory_person_items)

    if args.meetup is not None:
        generate_meetup(arguments.meetup)


if __name__ == '__main__':
    args = argparse.ArgumentParser(description="Details of data generation")
    args.add_argument('-u', action="store", dest="user_data")
    args.add_argument('-p', action="store", dest="persons")
    args.add_argument('-i', action="store", dest="inventory_person_items")
    args.add_argument('-m', action="store", dest="meetup")
    arguments = args.parse_args()

    generate_data(arguments)

    connection.commit()
    cursor.close()
    connection.close()
