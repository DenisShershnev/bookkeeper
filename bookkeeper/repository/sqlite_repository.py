from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from typing import Any
import sqlite3
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense

from datetime import datetime


class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        names = ', '.join(self.fields.keys())
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table_name} ({names})
        ''')
        connection.commit()
        connection.close()

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({p})',
                values
            )
            obj.pk = cur.lastrowid
            # con.commit()
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        cls_temp = list(self.table_name)
        cls_temp[0] = cls_temp[0].upper()
        cls = eval(''.join(cls_temp))
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute(f'''
        SELECT *
        FROM {self.table_name}
        ''')
        table = cursor.fetchall()
        connection.close()

        if pk > len(table):
            return None
        ltable = list(table[pk - 1])
        if ltable == [None] * len(self.fields) or ltable == [''] * len(self.fields):
            return None
        for i in range(len(self.fields)):
            try:
                datetime.strptime(ltable[i], '%Y-%m-%d %H:%M:%S.%f')
            except:
                pass
            else:
                ltable[i] = datetime.strptime(ltable[i], '%Y-%m-%d %H:%M:%S.%f')
        obj = cls(*ltable)
        obj.pk = pk
        return obj

    def delete(self, pk: int) -> None:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'''
            SELECT *
            FROM {self.table_name}
            ''')
            table = cur.fetchall()
            table[pk - 1] = tuple([None] * len(self.fields))
            cur.execute(
                f'DELETE FROM {self.table_name}',
            )
            for values in table:
                cur.execute(
                    f'INSERT INTO {self.table_name} ({names}) VALUES ({p})',
                    values
                )
            # con.commit()
        con.close()

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        cls_temp = list(self.table_name)
        cls_temp[0] = cls_temp[0].upper()
        cls = eval(''.join(cls_temp))
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute(f'''
                    SELECT *
                    FROM {self.table_name}
                    ''')
        table = cursor.fetchall()
        connection.close()
        if table == []:
            return []
        ltable = list(table[0])
        # if ltable != [None] * len(self.fields)
        k = 0
        while list(table[k]) == [None] * len(self.fields) or list(table[k]) == [''] * len(self.fields):
            if k >= (len(table) - 1):
                return []
            k = k + 1
        ltable = list(table[k])
        for j in range(len(self.fields)):
            try:
                datetime.strptime(ltable[j], '%Y-%m-%d %H:%M:%S.%f')
            except:
                pass
            else:
                ltable[j] = datetime.strptime(ltable[j], '%Y-%m-%d %H:%M:%S.%f')
        list_of_elements = [cls(*ltable)]
        list_of_elements[0].pk = k + 1
        for i in range(k, len(table) - 1):
            ltable = list(table[i + 1])
            if ltable != [None] * len(self.fields) and ltable != [''] * len(self.fields):
                for j in range(len(self.fields)):
                    try:
                        datetime.strptime(ltable[j], '%Y-%m-%d %H:%M:%S.%f')
                    except:
                        pass
                    else:
                        ltable[j] = datetime.strptime(ltable[j], '%Y-%m-%d %H:%M:%S.%f')
                list_of_elements.append(cls(*ltable))
                list_of_elements[-1].pk = i + 2
        if where is None:
            return list_of_elements
        return [obj for obj in list_of_elements
                if all(getattr(obj, attr) == value for attr, value in where.items())]

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'''
                    SELECT *
                    FROM {self.table_name}
                    ''')
            table = cur.fetchall()
            cur.execute(
                f'UPDATE {self.table_name} SET ({names}) = ({p}) WHERE ({names}) = ({p})',
                tuple([getattr(obj, x) for x in self.fields]) + table[obj.pk - 1]
            )
            # con.commit()
        con.close()
