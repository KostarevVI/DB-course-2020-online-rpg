from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Person, ClassOfPerson, UserDatum, Meetup, InventoryPerson
from .__name__ import db
import json
import random as rand
from sqlalchemy import *
from collections import namedtuple
from sqlalchemy.sql.expression import and_

game_menu = Blueprint('game_menu', __name__)


@game_menu.route('/', methods=['GET'])
@login_required
def select_person():
    if request.method == 'GET':
        persons_of_user = Person.query.filter(Person.user_id == current_user.id).join(ClassOfPerson) \
            .order_by(Person.id.desc()).all()
        classes_of_person = ClassOfPerson.query.all()

        return render_template("select_person.html", user=current_user, persons_of_user=persons_of_user,
                               classes_of_person=classes_of_person)

    # if request.method == 'POST':
    #     note = request.form.get('person')
    #
    #     if len(note) < 1:
    #         flash('Note is too short!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note added!', category='success')


@game_menu.route('/create-person', methods=['POST'])
@login_required
def create_person():
    person_params = json.loads(request.data)
    p_class_id = person_params['perClass']
    new_person = Person(class_of_person_id=p_class_id, health=100, experience=0, user_id=current_user.id,
                        is_enemy=False)
    db.session.add(new_person)
    db.session.commit()
    db.session.refresh(new_person)
    new_inv = InventoryPerson(person_id=new_person.id, inventory_size=rand.randrange(10, 40, 5))
    db.session.add(new_inv)
    db.session.commit()
    flash('Person added!', category='success')

    return jsonify({})


@game_menu.route('/delete-person', methods=['POST'])
@login_required
def delete_person():
    person = json.loads(request.data)
    person_id = person['personId']
    person = Person.query.get(person_id)
    if person:
        if person.user_id == current_user.id:
            db.session.delete(person)
            db.session.commit()

    return jsonify({})


@game_menu.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        user_profile = UserDatum.query.filter(UserDatum.id == current_user.id).first()

        return render_template("profile.html", user=current_user, user_profile=user_profile)

    if request.method == 'POST':
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        password3 = request.form.get('password3')

        user = UserDatum.query.filter_by(email=email).first()
        nickname_exists = UserDatum.query.filter_by(nickname=nickname).first()

        if nickname_exists and nickname != user.nickname:
            flash('This nickname is busy. Choose another.', category='error')
        elif nickname != current_user.nickname and password2 == '' and password3 == '' \
                and password1 == current_user.password and nickname_exists is None:
            user.nickname = nickname

            try:
                db.session.commit()
                flash('Profile changed successfully!', category='success')
                return redirect(url_for('game_menu.profile'))
            except:
                return "Something went wrong while updating..."

        elif password1 != user.password:
            flash('Incorrect current password, try again.', category='error')
        elif len(nickname) < 2:
            flash('Nickname must be greater than 1 character.', category='error')
        elif password2 != password3:
            flash('New passwords don\'t match.', category='error')
        elif len(password2) < 7:
            flash('New password must be at least 7 characters.', category='error')
        elif password1 == password2:
            flash('Your old password can not be your new password.', category='error')
        else:
            user.nickname = nickname
            user.password = password2

            try:
                db.session.commit()
                flash('Profile changed successfully!', category='success')
                return redirect(url_for('game_menu.profile'))
            except:
                return "Something went wrong while updating..."

        return redirect(url_for('game_menu.profile'))


@game_menu.route('/leaderboard/<int:page_number>')
@login_required
def leaderboard(page_number):
    # query_result = db.engine.execute(
    #     text("select row_number() over (order by (wins_amount * 4 + draws_amount * 1 - looses_amount * 5) desc), "
    #          "u.nickname, wins_amount, draws_amount, looses_amount from user_data u "
    #          "inner join (select ud1.nickname, count(m1.result = 'win' OR NULL) AS wins_amount from meetup m1 "
    #          "inner join person p1 on p1.id = m1.person_id "
    #          "inner join user_data ud1 on p1.user_id = ud1.id "
    #          "GROUP BY ud1.nickname) AS wins_table ON wins_table.nickname = u.nickname "
    #          "inner join (select ud2.nickname, count(m2.result = 'draw' OR NULL) AS draws_amount from meetup m2 "
    #          "inner join person p2 on p2.id = m2.person_id "
    #          "inner join user_data ud2 on p2.user_id = ud2.id "
    #          "GROUP BY ud2.nickname) AS draws_table ON draws_table.nickname = u.nickname "
    #          "inner join (select distinct ud3.nickname, count(m3.result = 'loose' OR NULL) AS looses_amount from meetup m3 "
    #          "inner join person p3 on p3.id = m3.person_id "
    #          "inner join user_data ud3 on p3.user_id = ud3.id "
    #          "GROUP BY ud3.nickname) AS looses_table ON looses_table.nickname = u.nickname "
    #          "order by (wins_amount * 4 + draws_amount * 1 - looses_amount * 5) desc;"))

    wins_table = \
        db.session.query(UserDatum.nickname,
                         func.COUNT(or_(Meetup.result == 'win', text('NULL'))).label('wins_amount')). \
            join(Person, Person.id == Meetup.person_id).join(UserDatum, UserDatum.id == Person.user_id). \
            group_by(UserDatum.nickname).subquery()
    draws_table = \
        db.session.query(UserDatum.nickname,
                         func.COUNT(or_(Meetup.result == 'draw', text('NULL'))).label('draws_amount')). \
            join(Person, Person.id == Meetup.person_id).join(UserDatum, UserDatum.id == Person.user_id). \
            group_by(UserDatum.nickname).subquery()
    looses_table = \
        db.session.query(UserDatum.nickname,
                         func.COUNT(or_(Meetup.result == 'loose', text('NULL'))).label('looses_amount')). \
            join(Person, Person.id == Meetup.person_id).join(UserDatum, UserDatum.id == Person.user_id). \
            group_by(UserDatum.nickname).subquery()

    alchemy_query_result = \
        db.session.query(func.row_number().over(order_by=desc(wins_table.c.wins_amount * 4 + draws_table.c.draws_amount * 1 - looses_table.c.looses_amount * 5)).label('row_number'),
                         UserDatum.nickname,
                         wins_table.c.wins_amount,
                         draws_table.c.draws_amount,
                         looses_table.c.looses_amount).\
            join(wins_table, wins_table.c.nickname == UserDatum.nickname). \
            join(draws_table, draws_table.c.nickname == UserDatum.nickname). \
            join(looses_table, looses_table.c.nickname == UserDatum.nickname).\
            order_by(desc(wins_table.c.wins_amount * 4 + draws_table.c.draws_amount * 1 - looses_table.c.looses_amount * 5))

    # print(db.session.query(func.count(alchemy_query_result.c.nickname)).all())

    leaderboard_paging = alchemy_query_result.paginate(per_page=10, page=page_number, error_out=True)

    leaderboard_temp = namedtuple('Leaderboard', alchemy_query_result.all()[0].keys())
    leaderboard_table = [leaderboard_temp(*r) for r in alchemy_query_result.all()]

    idx = 0

    for index, el in enumerate(leaderboard_table):
        if el.nickname == current_user.nickname:
            idx = index
    print(leaderboard_table[idx])

    return render_template("leaderboard.html", user=current_user,
                           user_leaderboard=leaderboard_table[idx], leaderboard_paging=leaderboard_paging)
