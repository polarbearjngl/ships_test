# coding=utf-8
import os
import random

import nose
from hamcrest import assert_that, equal_to

from database import Database
from entity.entities import Ship, Weapon, Hull, Engine
from entity.list_of_entities import ListOfEntities

DATABASE_PATH = 'sqlite_database/ships.db'
DATABASE_DUMP_SQL = 'sqlite_database/ships_dump.sql'
DATABASE_DUMP_PATH = 'sqlite_database/ships_dump.db'


def setup_func():
    """Выполнение предусловий"""

    db_connect = Database(dbname=DATABASE_PATH)
    db_connect.create_default_tables()

    ships = []
    engines = []
    hulls = []
    weapons = []

    # generate random engines
    for i in range(1, 7):
        e_name = 'Engine{index}'.format(index=i)
        e_power = random.choice(range(1, 7))
        e_type = random.choice(range(1, 7))
        engine = Engine(name=e_name, power=e_power, type=e_type)
        db_connect.execute_statement(engine.insert())
        engines.append(engine)

    # generate random hulls
    for j in range(1, 6):
        h_name = 'Hull{index}'.format(index=j)
        h_armor = random.choice(range(1, 6))
        h_type = random.choice(range(1, 6))
        h_capacity = random.choice(range(1, 6))
        hull = Hull(name=h_name, armor=h_armor, type=h_type, capacity=h_capacity)
        db_connect.execute_statement(hull.insert())
        hulls.append(hull)

    # generate random weapons
    for k in range(1, 21):
        w_name = 'Weapon{index}'.format(index=k)
        w_reload_speed = random.choice(range(1, 21))
        w_rotational_speed = random.choice(range(1, 21))
        w_diameter = random.choice(range(1, 21))
        w_power_volley = random.choice(range(1, 21))
        w_count = random.choice(range(1, 21))
        weapon = Weapon(name=w_name, reload_speed=w_reload_speed, rotational_speed=w_rotational_speed,
                        diameter=w_diameter, power_volley=w_power_volley, count=w_count)
        db_connect.execute_statement(weapon.insert())
        weapons.append(weapon)

    # generate random ships
    for g in range(1, 201):
        s_name = 'Ship{index}'.format(index=g)
        s_weapon = random.choice(weapons).name
        s_hull = random.choice(hulls).name
        s_engine = random.choice(engines).name
        ship = Ship(name=s_name, weapon=s_weapon, hull=s_hull, engine=s_engine)
        db_connect.execute_statement(ship.insert())
        ships.append(ship)

    db_connect.create_dump(dump_name=DATABASE_DUMP_SQL, new_dbname=DATABASE_DUMP_PATH)

    list_of_entities = ListOfEntities(db_connect=db_connect)
    ships = list_of_entities.get_all_ships()
    weapons = list_of_entities.get_all_weapons()
    hulls = list_of_entities.get_all_hulls()
    engines = list_of_entities.get_all_engines()

    # change values randomly
    for engine in engines:
        db_connect.execute_statement(engine.random_change())

    for hull in hulls:
        db_connect.execute_statement(hull.random_change())

    for weapon in weapons:
        db_connect.execute_statement(weapon.random_change())

    for ship in ships:
        s_weapon = random.choice(weapons).name
        s_hull = random.choice(hulls).name
        s_engine = random.choice(engines).name
        db_connect.execute_statement(ship.random_change(new_engine=s_engine, new_hull=s_hull, new_weapon=s_weapon))

    db_connect.close_connection()


def teardown_func():
    """Удаление созданных данных"""

    db_connect = Database(dbname=DATABASE_PATH)
    db_dump_connect = Database(dbname=DATABASE_DUMP_PATH)
    list_of_entities = ListOfEntities(db_connect=db_connect)

    ships = list_of_entities.get_all_ships()
    weapons = list_of_entities.get_all_weapons()
    hulls = list_of_entities.get_all_hulls()
    engines = list_of_entities.get_all_engines()

    # delete info from db after test
    for list_of_entity in [ships, weapons, hulls, engines]:
        for entity in list_of_entity:
            db_connect.execute_statement(entity.remove())

    db_connect.close_connection()
    db_dump_connect.close_connection()
    os.remove(DATABASE_DUMP_PATH)


@nose.with_setup(setup=setup_func, teardown=teardown_func)
def test_ships():
    """Генератор для создания тестов"""

    ships_db = Database(dbname=DATABASE_PATH)
    ships_db_dump = Database(dbname=DATABASE_DUMP_PATH)

    for i in range(0, 200):
        yield assert_engine, i, ships_db, ships_db_dump

    for i in range(0, 200):
        yield assert_hull, i, ships_db, ships_db_dump

    for i in range(0, 200):
        yield assert_weapon, i, ships_db, ships_db_dump

    ships_db.close_connection()
    ships_db_dump.close_connection()


def assert_engine(index, ships_db, ships_db_dump):
    """Тест для engine"""
    list_of_entities = ListOfEntities(db_connect=ships_db)
    list_of_dump_entities = ListOfEntities(db_connect=ships_db_dump)

    ship = list_of_entities.get_all_ships()[index]
    dump_ship = list_of_dump_entities.get_all_ships()[index]

    engine = ships_db.get_engine(name=ship.engine)
    dump_engine = ships_db_dump.get_engine(name=dump_ship.engine)

    assert_that(ship.name, equal_to(dump_ship.name), u'Ship\'s name not equal to expected')
    assert_that(ship.engine, equal_to(dump_ship.engine), u'Engine\'s name not equal to expected')

    assert_that(engine, equal_to(dump_engine), u'Engine\'s params not equal to expected')


def assert_hull(index, ships_db, ships_db_dump):
    """Тест для hull"""

    list_of_entities = ListOfEntities(db_connect=ships_db)
    list_of_dump_entities = ListOfEntities(db_connect=ships_db_dump)

    ship = list_of_entities.get_all_ships()[index]
    dump_ship = list_of_dump_entities.get_all_ships()[index]

    hull = ships_db.get_hull(name=ship.hull)
    dump_hull = ships_db_dump.get_hull(name=dump_ship.hull)

    assert_that(ship.name, equal_to(dump_ship.name), u'Ship\'s name not equal to expected')
    assert_that(ship.hull, equal_to(dump_ship.hull), u'Hull\'s name not equal to expected')
    assert_that(hull, equal_to(dump_hull), u'Hull\'s params not equal to expected')


def assert_weapon(index, ships_db, ships_db_dump):
    """Тест для weapon"""

    list_of_entities = ListOfEntities(db_connect=ships_db)
    list_of_dump_entities = ListOfEntities(db_connect=ships_db_dump)

    ship = list_of_entities.get_all_ships()[index]
    dump_ship = list_of_dump_entities.get_all_ships()[index]

    weapon = ships_db.get_weapon(name=ship.weapon)
    dump_weapon = ships_db_dump.get_weapon(name=dump_ship.weapon)

    assert_that(ship.name, equal_to(dump_ship.name), u'Ship\'s name not equal to expected')
    assert_that(ship.hull, equal_to(dump_ship.hull), u'weapon\'s name not equal to expected')

    assert_that(weapon, equal_to(dump_weapon), u'weapon\'s params not equal to expected')
