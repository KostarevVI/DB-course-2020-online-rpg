# coding: utf-8
from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Enum, ForeignKey, Integer, String, Table, Text, text
from sqlalchemy.orm import relationship
from .__name__ import db
from flask_login import UserMixin

metadata = db.metadata


class ClassOfPerson(db.Model):
    __tablename__ = 'class_of_person'
    __table_args__ = (
        CheckConstraint("(name)::text <> ''::text"),
        CheckConstraint("description <> ''::text")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('class_of_person_id_seq'::regclass)"))
    name = Column(String(30), nullable=False, unique=True)
    description = Column(Text, nullable=False)


class Item(db.Model):
    __tablename__ = 'item'
    __table_args__ = (
        CheckConstraint("(name)::text <> ''::text"),
        CheckConstraint("description <> ''::text")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('item_id_seq'::regclass)"))
    name = Column(String(30), nullable=False, unique=True)
    description = Column(Text, nullable=False)


class UserDatum(db.Model, UserMixin):
    __tablename__ = 'user_data'
    __table_args__ = (
        CheckConstraint("(email)::text <> ''::text"),
        CheckConstraint("(nickname)::text <> ''::text"),
        CheckConstraint("(password)::text <> ''::text")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('user_data_id_seq'::regclass)"))
    email = Column(String(40), nullable=False, unique=True)
    password = Column(String(16), nullable=False)
    nickname = Column(String(20), nullable=False, unique=True)


class Person(db.Model):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, server_default=text("nextval('person_id_seq'::regclass)"))
    class_of_person_id = Column(ForeignKey('class_of_person.id', ondelete='CASCADE'))
    health = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    user_id = Column(ForeignKey('user_data.id', ondelete='CASCADE'))
    update_date = Column(DateTime, nullable=False, server_default=text("now()"))
    is_enemy = Column(Boolean, nullable=False, server_default=text("true"))

    class_of_person = relationship('ClassOfPerson')
    user_data = relationship('UserDatum')


class Skill(db.Model):
    __tablename__ = 'skill'
    __table_args__ = (
        CheckConstraint("(name)::text <> ''::text"),
        CheckConstraint("description <> ''::text")
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('skill_id_seq'::regclass)"))
    name = Column(String(30), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    cost = Column(Integer, nullable=False)
    class_of_person_id = Column(ForeignKey('class_of_person.id', ondelete='CASCADE'))

    class_of_person = relationship('ClassOfPerson')


class InventoryPerson(db.Model):
    __tablename__ = 'inventory_person'
    __table_args__ = (
        CheckConstraint('inventory_size > 0'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('inventory_person_id_seq'::regclass)"))
    person_id = Column(ForeignKey('person.id', ondelete='CASCADE'))
    inventory_size = Column(Integer, nullable=False)

    person = relationship('Person')


class Meetup(db.Model):
    __tablename__ = 'meetup'

    id = Column(Integer, primary_key=True, server_default=text("nextval('meetup_id_seq'::regclass)"))
    person_id = Column(ForeignKey('person.id', ondelete='CASCADE'))
    result = Column(Enum('loose', 'draw', 'win', name='meetup_result'), nullable=False)
    meetup_date = Column(DateTime, nullable=False, server_default=text("now()"))
    enemy_id = Column(ForeignKey('person.id', ondelete='SET NULL'))

    enemy = relationship('Person', primaryjoin='Meetup.enemy_id == Person.id')
    person = relationship('Person', primaryjoin='Meetup.person_id == Person.id')

# Автогенерация
# t_person_skill = Table(
#     'person_skill', metadata,
#     Column('person_id', ForeignKey('person.id', ondelete='CASCADE')),
#     Column('skill_id', ForeignKey('skill.id', ondelete='CASCADE')),
#     Column('equiped', Boolean, nullable=False)
# )


class PersonSkill(db.Model):
    __tablename__ = 'person_skill'

    person_id = Column(ForeignKey('person.id', ondelete='CASCADE'), primary_key=True)
    skill_id = Column(ForeignKey('skill.id', ondelete='CASCADE'), primary_key=True)
    equiped = Column(Boolean, nullable=False)

    person = relationship('Person')
    skill = relationship('Skill')


# t_inventory_person_items = Table(
#     'inventory_person_items', metadata,
#     Column('inventory_person_id', ForeignKey('inventory_person.id', ondelete='CASCADE')),
#     Column('item_id', ForeignKey('item.id', ondelete='CASCADE')),
#     Column('add_date', DateTime, nullable=False, server_default=text("now()")),
#     Column('is_deleted', Boolean, nullable=False),
#     Column('amount', Integer, nullable=False),
#     Column('update_date', DateTime, nullable=False, server_default=text("now()")),
#     CheckConstraint('amount > 0')
# )

class InventoryPersonItems(db.Model):
    __tablename__ = 'inventory_person_items'
    __table_args__ = (
        CheckConstraint('amount >= 0'),
    )

    inventory_person_id = Column(ForeignKey('inventory_person.id', ondelete='CASCADE'), primary_key=True)
    item_id = Column(ForeignKey('item.id', ondelete='CASCADE'), primary_key=True)
    add_date = Column(DateTime, nullable=False, primary_key=True)
    is_deleted = Column(Boolean, nullable=False, primary_key=True)
    amount = Column(Integer, nullable=False, primary_key=True)
    update_date = Column(DateTime, nullable=False, primary_key=True)

    inventory_person = relationship('InventoryPerson')
    item = relationship('Item', lazy='subquery')
