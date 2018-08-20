# coding=utf-8
import os
import sqlite3


class Database:

    _sql_insert_ships_table = """CREATE TABLE IF NOT EXISTS SHIPS (SHIP varchar(256) NOT NULL,
                                                                    WEAPON varchar(256) NOT NULL,
                                                                    HULL varchar(256) NOT NULL,
                                                                    ENGINE varchar(256) NOT NULL,
                                                                    PRIMARY KEY (SHIP));"""

    _sql_insert_weapons_table = """CREATE TABLE IF NOT EXISTS WEAPONS (WEAPON varchar(256) NOT NULL,
                                                                        RELOAD_SPEED number NOT NULL,
                                                                        ROTATIONAL_SPEED number NOT NULL,
                                                                        DIAMETER number NOT NULL,
                                                                        POWER_VOLLEY number NOT NULL,
                                                                        COUNT number NOT NULL,
                                                                        PRIMARY KEY (WEAPON));"""

    _sql_insert_hulls_table = """CREATE TABLE IF NOT EXISTS HULLS (HULL varchar(256) NOT NULL,
                                                                     ARMOR number NOT NULL,
                                                                     TYPE number NOT NULL,
                                                                     CAPACITY number NOT NULL,
                                                                     PRIMARY KEY (HULL));"""

    _sql_insert_engines_table = """CREATE TABLE IF NOT EXISTS ENGINES (ENGINE varchar(256) NOT NULL,
                                                                       POWER number NOT NULL,
                                                                       TYPE number NOT NULL,
                                                                       PRIMARY KEY (ENGINE));"""

    _sql_get_weapon = """SELECT * FROM WEAPONS WHERE WEAPON LIKE '{name}'"""

    _sql_get_hull = """SELECT * FROM HULLS WHERE HULL LIKE '{name}'"""

    _sql_get_engine = """SELECT * FROM ENGINES WHERE ENGINE LIKE '{name}'"""

    _sql_select_all = """SELECT * FROM {table_name}"""

    def __init__(self, dbname):
        self._conn = self.init_connection(dbname=dbname)
        self._cursor = self._conn.cursor()

    @staticmethod
    def init_connection(dbname):
        return sqlite3.connect(database=dbname)

    @property
    def get_connection(self):
        return self._conn

    def close_connection(self):
        self._conn.close()

    def create_default_tables(self):
        """Создать таблицы по-умолчанию, если они отсутствуют"""
        for statement in [self._sql_insert_ships_table,
                          self._sql_insert_engines_table,
                          self._sql_insert_hulls_table,
                          self._sql_insert_weapons_table]:
            self._cursor.execute(statement)

    def execute_statement(self, statement):
        """Выполнить команду SQL"""
        result = self._cursor.execute(statement)
        self._conn.commit()
        if result:
            return self.cursor_to_dict(cursor=result)

    def select_all_from_table(self, table):
        """Получить все записи из таблицы"""
        result = self._cursor.execute(self._sql_select_all.format(table_name=table))
        return self.cursor_to_dict(cursor=result)

    def get_weapon(self, name):
        """Получить weapon по имени"""
        return self.execute_statement(self._sql_get_weapon.format(name=name))[0]

    def get_hull(self, name):
        """Получить hull по имени"""
        return self.execute_statement(self._sql_get_hull.format(name=name))[0]

    def get_engine(self, name):
        """Получить engine по имени"""
        return self.execute_statement(self._sql_get_engine.format(name=name))[0]

    def rec_to_dict(self, description, values, dic):
        """Сгенерировать словарь"""
        for i in xrange(len(values)):
            key = description[i][0]
            if not dic.has_key(key):
                dic[description[i][0]] = values[i]

        return dic

    def cursor_to_dict(self, cursor):
        """Преобразовать курсор базы данных в словарь"""
        array = []
        for rec in cursor.fetchall():
            dic = {}
            self.rec_to_dict(description=cursor.description, values=rec, dic=dic)
            array.append(dic)
        return array

    def create_dump(self, dump_name, new_dbname):
        """Создать Дамп БД"""
        with open(dump_name, 'w') as f:
            for line in self._conn.iterdump():
                f.write('%s\n' % line)
            f.close()

        with open(dump_name, 'r') as f:
            statement = f.read()
            f.close()

        dump_db = Database(dbname=new_dbname)
        dump_db._cursor.executescript(statement)
        os.remove(dump_name)
        return dump_db


