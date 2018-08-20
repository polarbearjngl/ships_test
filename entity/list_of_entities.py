# coding=utf-8
from entity.entities import Ship, Weapon, Hull, Engine


class ListOfEntities(object):
    """класс для получения списка всех элементов из таблицы в БД"""

    def __init__(self, db_connect):
        self.conn = db_connect

    def get_all_ships(self):
        """Получить все ships"""
        ships_from_db = self.conn.select_all_from_table('SHIPS')
        ships = []
        for info in ships_from_db:
            ships.append(Ship(name=info['SHIP'], weapon=info['WEAPON'], hull=info['HULL'], engine=info['ENGINE']))
        return ships

    def get_all_weapons(self):
        """Получить все weapons"""
        weapons = []
        weapons_from_db = self.conn.select_all_from_table('WEAPONS')
        for info in weapons_from_db:
            weapons.append(Weapon(name=info['WEAPON'], reload_speed=info['RELOAD_SPEED'],
                                  rotational_speed=info['ROTATIONAL_SPEED'], diameter=info['DIAMETER'],
                                  power_volley=info['POWER_VOLLEY'], count=info['COUNT']))
        return weapons

    def get_all_hulls(self):
        """Получить все hulls"""
        hulls = []
        hulls_from_db = self.conn.select_all_from_table('HULLS')
        for info in hulls_from_db:
            hulls.append(Hull(name=info['HULL'], armor=info['ARMOR'], type=info['TYPE'], capacity=info['CAPACITY']))

        return hulls

    def get_all_engines(self):
        """Получить все engines"""
        engines = []
        engines_from_db =  self.conn.select_all_from_table('ENGINES')
        for info in engines_from_db:
            engines.append(Engine(name=info['ENGINE'], power=info['POWER'], type=info['TYPE']))

        return engines