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

items = open("input/items.txt", "r").readlines()
classes = open("input/classes.txt", "r").readlines()
skills = open("input/skills.txt", "r").readlines()
nicknames = open("input/nicknames.txt", "r").readlines()
email_domains = open("input/email_domains.txt", "r").readlines()


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
            cursor.execute(
                'INSERT INTO \"item\" VALUES (default, \'{}\', \'{}\') ON CONFLICT DO NOTHING'
                    .format(element, description))
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
            cursor.execute(
                'INSERT INTO \"class_of_person\" VALUES (default, \'{}\', \'{}\') ON CONFLICT DO NOTHING'
                    .format(element, description))
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
            equiped = False
            cursor.execute('SELECT id FROM class_of_person WHERE name=\'{}\''.format(element.split()[0]))
            class_of_person_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO skill VALUES (default, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'
                           'ON CONFLICT DO NOTHING'.format(element,
                                                           description,
                                                           cost,
                                                           equiped,
                                                           class_of_person_id))


def generate_user_data(amount):
    global user_data_ids
    for i in range(int(amount)):
        nickname = random.choice(nicknames)
        nickname = nickname.replace("\n", "")
        password = random_string(random.randint(10, 16))
        email_domain = random.choice(email_domains)
        email_domain = email_domain.replace("\n", "")
        email = random_string(random.randint(10, 20)) + email_domain
        cursor.execute('INSERT INTO user_data VALUES (default, \'{}\', \'{}\', \'{}\') ON CONFLICT DO NOTHING'
                       .format(email,
                               password,
                               nickname[:20]))
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

        if i % 10 != 0:
            user_id = random.choice(user_data_ids)
            is_enemy = False
            cursor.execute(
                'INSERT INTO person VALUES (default, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
                    class_of_person_id,
                    health,
                    experience,
                    user_id[0],
                    update_date,
                    is_enemy))
        else:
            cursor.execute(
                'INSERT INTO person (id, class_of_person_id, health, experience, update_date, is_enemy) '
                'VALUES (default, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(
                    class_of_person_id,
                    health,
                    experience,
                    update_date,
                    is_enemy))

    cursor.execute('SELECT id FROM person')
    person_ids = cursor.fetchall()
    generate_inventory_person()


def generate_inventory_person():
    global inventory_person_ids
    cursor.execute('SELECT person_id FROM inventory_person')
    person_id_in_inventory_person = cursor.fetchall()

    for element in person_ids:
        if element not in person_id_in_inventory_person:
            person_id = element[0]
            inventory_size = 5 * random.randint(2, 8)
            cursor.execute('INSERT INTO inventory_person VALUES (default, \'{}\', \'{}\')'.format(person_id,
                                                                                                  inventory_size))
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
        result = random.choice(('win', 'loose', 'draw'))  # ?????

        cursor.execute('INSERT INTO meetup VALUES (default, \'{}\', \'{}\', \'{}\', \'{}\')'.format(person_id[0],
                                                                                                    result,
                                                                                                    meetup_date[0][0],
                                                                                                    enemy_id[0]))


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

        if sum(element[0] for element in all_amount) < inventory_person_tuple[2]:
            cursor.execute('SELECT item_id FROM inventory_person_items WHERE inventory_person_id=\'{}\''
                           .format(inventory_person_id[0]))
            item_id_in_inventory_person_items = cursor.fetchall()

            cursor.execute('SELECT update_date FROM person WHERE id=\'{}\''.format(inventory_person_tuple[1]))
            person_update_date = cursor.fetchone()

            cursor.execute('SELECT * FROM inventory_person_items WHERE inventory_person_id=\'{}\' AND item_id=\'{}\''.
                           format(inventory_person_id[0], item_id[0]))
            current_item = cursor.fetchone()

            is_deleted = False

            if item_id_in_inventory_person_items and item_id in item_id_in_inventory_person_items and current_item \
                    and not bool(current_item[3]):
                amount_item = int(current_item[4]) + 1
                update_date = random_date(current_item[5], today)

                cursor.execute('UPDATE inventory_person_items SET amount=\'{}\', update_date=\'{}\' '
                               'WHERE inventory_person_id=\'{}\' AND item_id=\'{}\''.format(amount_item,
                                                                                            update_date,
                                                                                            inventory_person_id[0],
                                                                                            item_id[0]))
            else:
                add_date = person_update_date[0]
                amount_item = 1
                update_date = add_date

                cursor.execute(
                    'INSERT INTO inventory_person_items VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'
                    .format(inventory_person_id[0],
                            item_id[0],
                            add_date,
                            is_deleted,
                            amount_item,
                            update_date))


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
    args.add_argument('--use', action="store", dest="user_data")
    args.add_argument('--per', action="store", dest="persons")
    args.add_argument('--inv', action="store", dest="inventory_person_items")
    args.add_argument('--mee', action="store", dest="meetup")
    arguments = args.parse_args()

    generate_data(arguments)

    connection.commit()
    cursor.close()
    connection.close()
