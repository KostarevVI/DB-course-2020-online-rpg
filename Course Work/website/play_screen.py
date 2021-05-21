import random as rand
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from website.models import *
import json
from .__name__ import db
from sqlalchemy import *
from flask_login import login_user, login_required, logout_user, current_user


current_person = None
inventory_of_person_1 = None
inventory_of_person_2 = None
items_in_inventory_1 = None
items_in_inventory_2 = None
inventories_of_person = None

play_screen = Blueprint('play_screen', __name__)


@play_screen.route('/play-person', methods=['POST'])
@login_required
def play_person():
    global current_user
    global current_person
    person = json.loads(request.data)
    play_person_id = person['playPersonId']
    current_person = Person.query.filter_by(id=play_person_id).first()
    print(current_person.id)
    return jsonify({})


@play_screen.route('/play', methods=['GET', 'POST'])
@login_required
def play_menu():
    global current_user
    global current_person
    global inventories_of_person

    if request.method == 'POST':
        opponent_nick = request.form.get('nickname')
        battle_inv = request.form.get('battleInventorySelect')

        cur_amount = db.session.query(func.sum(InventoryPersonItems.amount)).filter(
            InventoryPersonItems.inventory_person_id == battle_inv).first()
        # print(opponent_nick)
        # print(battle_inv)
        print(db.session.query(Person).join(UserDatum, Person.user_id == UserDatum.id).filter(
            UserDatum.nickname == opponent_nick).first() is None)

        if cur_amount[0] is None or cur_amount[0] < InventoryPerson.query.filter_by(id=battle_inv).first().inventory_size:
            enemy = None
            if opponent_nick == '':
                while enemy is None or opponent_nick == current_user.nickname:
                    opponent_nick = db.session.query(UserDatum.nickname).order_by(func.random()).first().nickname
                    enemy = db.session.query(Person.id).join(UserDatum, UserDatum.id == Person.user_id). \
                        filter(UserDatum.nickname == opponent_nick).order_by(func.random()).first()
            elif db.session.query(Person).join(UserDatum, Person.user_id == UserDatum.id).filter(UserDatum.nickname == opponent_nick).first() is None:
                flash('This User don\'t have Persons to Battle', category='error')
                return render_template("play_screen.html", user=current_user, person=current_person,
                           inventories_of_person=inventories_of_person)
            else:
                while enemy is None:
                    enemy = db.session.query(Person.id).join(UserDatum, UserDatum.id == Person.user_id). \
                        filter(UserDatum.nickname == opponent_nick).order_by(func.random()).first()

            # print(opponent_nick.nickname)

            battle_result = rand.randint(0, 2)
            print(enemy)
            print(enemy.id)
            if battle_result == 0:
                item_from_enemy = \
                    db.session.query(InventoryPersonItems.item_id, InventoryPersonItems.inventory_person_id).\
                        join(InventoryPerson, InventoryPerson.id == InventoryPersonItems.inventory_person_id).\
                        filter(and_(InventoryPerson.person_id == enemy.id, InventoryPersonItems.is_deleted == False)).\
                        order_by(func.random()).first()
                if item_from_enemy is None:
                    current_user.experience += 10
                    flash('You have won the Battle! Gained: 10 exp', category='success')
                else:
                    my_item = db.session.query(InventoryPersonItems).\
                        join(InventoryPerson, InventoryPerson.id == InventoryPersonItems.inventory_person_id).\
                        filter(and_(InventoryPerson.person_id == current_person.id, InventoryPersonItems.item_id == item_from_enemy.item_id)).first()
                    if my_item is not None:
                        my_item.amount += 1
                    else:
                        new_my_item = InventoryPersonItems(item_id=item_from_enemy.item_id, inventory_person_id=battle_inv,
                                                           add_date=text('now()'), is_deleted=False, amount=1,
                                                           update_date=text('now()'))
                        db.session.add(new_my_item)
                    new_meetup = Meetup(person_id=current_person.id, result='win', meetup_date=text('now()'),
                                    enemy_id=enemy.id)
                    db.session.add(new_meetup)
                    flash('You have won the Battle! Gained: '+
                          Item.query.filter_by(id=item_from_enemy.item_id).first().name + ' from ' + opponent_nick, category='success')
            elif battle_result == 1:
                flash('It\'s a Draw.', category='info')
                new_meetup = Meetup(person_id=current_person.id, result='draw', meetup_date=text('now()'),
                                    enemy_id=enemy.id)
                db.session.add(new_meetup)
            else:
                flash('You have lost the Battle :(', category='error')
                new_meetup = Meetup(person_id=current_person.id, result='loose', meetup_date=text('now()'),
                                    enemy_id=enemy.id)
                db.session.add(new_meetup)

            db.session.commit()
        else:
            flash('You can\'t go on Battle with full Inventory. Free this or choose another.', category='error')

    if inventories_of_person is None:
        inventories_of_person = InventoryPerson.query.filter_by(person_id=current_person.id).all()

    print(current_person.id)

    return render_template("play_screen.html", user=current_user, person=current_person,
                           inventories_of_person=inventories_of_person)


@play_screen.route('/stats', methods=['GET'])
@login_required
def stats():
    global current_person
    global current_user
    person_with_class_name = Person.query.filter_by(id=current_person.id).join(ClassOfPerson).first()
    inventories_amount = InventoryPerson.query.filter_by(person_id=current_person.id).count()
    items = db.session.query(InventoryPersonItems.amount).join(InventoryPerson).join(Person). \
        filter(Person.id == current_person.id).all()
    items_amount = 0
    for el in items:
        items_amount += el[0]
    skills_unlocked = PersonSkill.query.filter(PersonSkill.person_id == current_person.id,
                                               PersonSkill.equiped == True).count()
    meetups_p_attack = db.session.query(Meetup, UserDatum.nickname).join(Person, Person.id == Meetup.enemy_id). \
        join(UserDatum, Person.user_id == UserDatum.id).filter(Meetup.person_id == current_person.id). \
        order_by(Meetup.meetup_date.desc()).all()
    meetups_p_defence = db.session.query(Meetup, UserDatum.nickname).join(Person, Person.id == Meetup.person_id). \
        join(UserDatum, Person.user_id == UserDatum.id).filter(Meetup.enemy_id == current_person.id). \
        order_by(Meetup.meetup_date.desc()).all()
    return render_template("stats.html", user=current_user, person=person_with_class_name,
                           meetups_p_defence=meetups_p_defence, meetups_p_attack=meetups_p_attack,
                           inventories_amount=inventories_amount, items_amount=items_amount,
                           skills_unlocked=skills_unlocked)


@play_screen.route('/change-person', methods=['GET', 'POST'])
@login_required
def change_person():
    global current_person
    global inventory_of_person_1
    global items_in_inventory_1
    global inventory_of_person_2
    global items_in_inventory_2
    global inventories_of_person
    current_person = None
    inventory_of_person_1 = None
    items_in_inventory_1 = None
    inventory_of_person_2 = None
    items_in_inventory_2 = None
    inventories_of_person = None
    return redirect(url_for('game_menu.select_person'))


@play_screen.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    global inventory_of_person_1
    global inventory_of_person_2
    global items_in_inventory_1
    global items_in_inventory_2
    global inventories_of_person
    global current_person
    global current_user

    if request.method == 'POST':
        need_to_transfer = request.form.getlist('checkTransfer')  # row_itemId_inventoryId
        amount_to_transfer = request.form.getlist('selectTransfer')
        sec_inventory_cur_amount = request.form.get('transferBtn')

        if need_to_transfer != []:
            need_to_transfer_list = []
            for element in need_to_transfer:
                need_to_transfer_list.append(element.split('_'))

            sum_amount = 0
            for k in need_to_transfer_list:
                sum_amount += int(amount_to_transfer[int(k[0])])
            if sum_amount + int(sec_inventory_cur_amount) <= inventory_of_person_2.inventory_size:

                for trans_item in need_to_transfer_list:
                    item_amount = amount_to_transfer[int(trans_item[0])]
                    update_item = InventoryPersonItems.query.filter_by(item_id=trans_item[1],
                                                                       inventory_person_id=inventory_of_person_2.id,
                                                                       is_deleted=False).first()
                    if update_item:
                        update_item.amount += int(item_amount)
                        update_item.update_date = text('now()')
                    else:
                        inventory_person_item = InventoryPersonItems(item_id=trans_item[1],
                                                                     inventory_person_id=inventory_of_person_2.id,
                                                                     add_date=text('now()'),
                                                                     is_deleted=False,
                                                                     amount=item_amount,
                                                                     update_date=text('now()'))
                        try:
                            db.session.add(inventory_person_item)
                        except:
                            return 'Some error while insert'

                    cur_item = InventoryPersonItems.query.filter_by(item_id=trans_item[1],
                                                                    inventory_person_id=inventory_of_person_1.id,
                                                                    is_deleted=False).first()
                    if cur_item.amount > int(item_amount):
                        cur_item.amount -= int(item_amount)
                        cur_item.update_date = text('now()')
                    else:
                        cur_item.amount = 0
                        cur_item.is_deleted = True
                        cur_item.update_date = text('now()')

                    db.session.commit()

            else:
                flash('Too many items to transfer. Select less or second inventory is full.', category='error')

        print(need_to_transfer)
        print(amount_to_transfer)

    print('PersonId: ' + str(current_person.id))
    if inventories_of_person is None:
        inventories_of_person = InventoryPerson.query.filter_by(person_id=current_person.id).all()

    if inventory_of_person_1 is None:
        inventory_of_person_1 = InventoryPerson.query.filter_by(person_id=current_person.id).first()
    print('InvPer1: ' + str(inventory_of_person_1))

    items_in_inventory_1 = InventoryPersonItems.query.filter_by(inventory_person_id=inventory_of_person_1.id,
                                                                is_deleted=False).join(Item).all()

    if inventory_of_person_2 is not None:
        items_in_inventory_2 = InventoryPersonItems.query.filter_by(inventory_person_id=inventory_of_person_2.id,
                                                                    is_deleted=False).join(Item).all()
        print(inventory_of_person_2)

    return render_template("inventory.html", user=current_user, inventories_of_person=inventories_of_person,
                           inventory_of_person_1=inventory_of_person_1, items_in_inventory_1=items_in_inventory_1,
                           inventory_of_person_2=inventory_of_person_2, items_in_inventory_2=items_in_inventory_2,
                           person=current_person)


@play_screen.route('/inventory-select', methods=['POST'])
@login_required
def inventory_select():
    global inventory_of_person_1
    global inventory_of_person_2
    global items_in_inventory_1
    global items_in_inventory_2
    inventory_params = json.loads(request.data)
    per_inv_1 = inventory_params['perInv1']
    per_inv_2 = inventory_params['perInv2']
    inventory_of_person_1 = InventoryPerson.query.filter_by(id=per_inv_1).first()
    items_in_inventory_1 = InventoryPersonItems.query.filter_by(inventory_person_id=inventory_of_person_1.id,
                                                                is_deleted=False).all()

    inventory_of_person_2 = InventoryPerson.query.filter_by(id=per_inv_2).first()
    items_in_inventory_2 = InventoryPersonItems.query.filter_by(inventory_person_id=inventory_of_person_2.id,
                                                                is_deleted=False).join(Item).all()

    return jsonify({})


@play_screen.route('/shop', methods=['GET', 'POST'])
@login_required
def shop():
    global current_person
    if request.method == 'POST':
        if current_person.experience >= 30:
            print(current_person.experience)
            current_person = db.session.query(Person).filter_by(id=current_person.id).first()
            current_person.experience -= 30
            print(current_person.experience)
            db.session.commit()
            #   cur_id = current_person.id
            # current_person = db.session.expunge_all().query(Person).filter_by(id=cur_id).first()
            print(current_person.experience)
            new_inv = InventoryPerson(person_id=current_person.id, inventory_size=rand.randrange(10, 40, 5))
            db.session.add(new_inv)
            db.session.commit()
        else:
            flash('You have <30 exp', category='error')

    return render_template("shop.html", user=current_user, person=current_person,
                           inventories_of_person=inventories_of_person)


def logout_clear():
    global current_person
    global inventory_of_person_1
    global items_in_inventory_1
    global inventory_of_person_2
    global items_in_inventory_2
    global inventories_of_person
    current_person = None
    inventory_of_person_1 = None
    items_in_inventory_1 = None
    inventory_of_person_2 = None
    items_in_inventory_2 = None
    inventories_of_person = None
    print('clear!')
