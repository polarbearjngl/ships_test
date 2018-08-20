# coding=utf-8
import random


class Ship(object):
    """Класс для работы с записью из таблицы SHIPS"""

    _sql_insert_ship = """INSERT INTO SHIPS (SHIP, WEAPON, HULL, ENGINE)
                          VALUES('{name}', '{weapon}', '{hull}', '{engine}');"""

    _sql_get_ship = """SELECT * FROM SHIPS WHERE SHIP LIKE '{name}'"""

    _sql_update_ship = """UPDATE SHIPS SET WEAPON = '{weapon}', HULL = '{hull}', ENGINE = '{engine}'
                          WHERE SHIP LIKE '{name}'"""

    _sql_remove = """DELETE FROM SHIPS WHERE SHIP LIKE '{name}'"""

    def __init__(self, name, weapon, hull, engine):
        self.name = name
        self.weapon = weapon
        self.hull = hull
        self.engine = engine

    def insert(self):
        """Получить команду SQL для добавления в БД"""
        return self._sql_insert_ship.format(name=self.name, weapon=self.weapon, hull=self.hull, engine=self.engine)

    def get(self):
        return self._sql_get_ship.format(name=self.name)

    def remove(self):
        """Получить команду SQL для удаления из БД"""
        return self._sql_remove.format(name=self.name)

    def random_change(self, new_weapon, new_hull, new_engine):
        """Выполнить случайное преобразование харарактеристик"""
        if random.randint(0, 1) == 1:
            self.weapon = new_weapon
        if random.randint(0, 1) == 1:
            self.hull = new_hull
        if random.randint(0, 1) == 1:
            self.engine = new_engine

        return self._sql_update_ship.format(name=self.name, weapon=self.weapon, hull=self.hull, engine=self.engine)


class Weapon(object):
    """Класс для работы с записью из таблицы WEAPONS"""

    _sql_insert_weapon = """INSERT INTO WEAPONS (WEAPON, RELOAD_SPEED, ROTATIONAL_SPEED, DIAMETER, POWER_VOLLEY, COUNT)
                            VALUES('{name}', {reload_speed}, {rotational_speed}, {diameter}, {power_volley}, {count});"""

    _sql_update_weapon = """UPDATE WEAPONS SET RELOAD_SPEED = {reload_speed}, ROTATIONAL_SPEED = {rotational_speed},
                                               DIAMETER = {diameter}, POWER_VOLLEY = {power_volley}, COUNT = {count}
                            WHERE WEAPON LIKE '{name}'"""

    _sql_remove = """DELETE FROM WEAPONS WHERE WEAPON LIKE '{name}'"""

    def __init__(self, name, reload_speed, rotational_speed, diameter, power_volley, count):
        self.name = name
        self.reload_speed = reload_speed
        self.rotational_speed = rotational_speed
        self.diameter = diameter
        self.power_volley = power_volley
        self.count = count

    def insert(self):
        """Получить команду SQL для добавления в БД"""
        return self._sql_insert_weapon.format(name=self.name, reload_speed=self.reload_speed,
                                              rotational_speed=self.rotational_speed, diameter=self.diameter,
                                              power_volley=self.power_volley, count=self.count)

    def remove(self):
        """Получить команду SQL для удаления из БД"""
        return self._sql_remove.format(name=self.name)

    def random_change(self):
        """Выполнить случайное преобразование харарактеристик"""
        if random.randint(0, 1) == 1:
            self.reload_speed = random.choice(range(1, 21))
        if random.randint(0, 1) == 1:
            self.rotational_speed = random.choice(range(1, 21))
        if random.randint(0, 1) == 1:
            self.diameter = random.choice(range(1, 21))
        if random.randint(0, 1) == 1:
            self.power_volley = random.choice(range(1, 21))
        if random.randint(0, 1) == 1:
            self.count = random.choice(range(1, 21))

        return self._sql_update_weapon.format(name=self.name, reload_speed=self.reload_speed,
                                              rotational_speed=self.rotational_speed, diameter=self.diameter,
                                              power_volley=self.power_volley, count=self.count)


class Hull(object):
    """Класс для работы с записью из таблицы HULLS"""

    _sql_insert_hull = """INSERT INTO HULLS (HULL, ARMOR, TYPE, CAPACITY)
                          VALUES('{name}', {armor}, {type}, {capacity});"""

    _sql_update_hull = """UPDATE HULLS SET ARMOR = {armor}, TYPE = {type}, CAPACITY = {capacity}
                          WHERE HULL LIKE '{name}'"""

    _sql_remove = """DELETE FROM HULLS WHERE HULL LIKE '{name}'"""

    def __init__(self, name, armor, type, capacity):
        self.name = name
        self.armor = armor
        self.type = type
        self.capacity = capacity

    def insert(self):
        """Получить команду SQL для добавления в БД"""
        return self._sql_insert_hull.format(name=self.name, armor=self.armor, type=self.type, capacity=self.capacity)

    def remove(self):
        """Получить команду SQL для удаления из БД"""
        return self._sql_remove.format(name=self.name)

    def random_change(self):
        """Выполнить случайное преобразование харарактеристик"""
        if random.randint(0, 1) == 1:
            self.armor = random.choice(range(1, 6))
        if random.randint(0, 1) == 1:
            self.type = random.choice(range(1, 6))
        if random.randint(0, 1) == 1:
            self.capacity = random.choice(range(1, 6))

        return self._sql_update_hull.format(name=self.name, armor=self.armor, type=self.type, capacity=self.capacity)


class Engine(object):
    """Класс для работы с записью из таблицы ENGINES"""

    _sql_insert_engine = """INSERT INTO ENGINES (ENGINE, POWER, TYPE)
                            VALUES('{name}', {power}, {type});"""

    _sql_update_engine = """UPDATE ENGINES SET POWER = {power}, TYPE = {type} WHERE ENGINE LIKE '{name}'"""

    _sql_remove = """DELETE FROM ENGINES WHERE ENGINE LIKE '{name}'"""

    def __init__(self, name, power, type):
        self.name = name
        self.power = power
        self.type = type

    def insert(self):
        """Получить команду SQL для добавления в БД"""
        return self._sql_insert_engine.format(name=self.name, power=self.power, type=self.type)

    def remove(self):
        """Получить команду SQL для удаления из БД"""
        return self._sql_remove.format(name=self.name)

    def random_change(self):
        """Выполнить случайное преобразование харарактеристик"""
        if random.randint(0, 1) == 1:
            self.power = random.choice(range(1, 7))
        if random.randint(0, 1) == 1:
            self.type = random.choice(range(1, 7))

        return self._sql_update_engine.format(name=self.name, power=self.power, type=self.type)
