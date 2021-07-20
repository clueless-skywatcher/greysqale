from .errors import GSQLQueryError
import inspect

from .database import GSQLDatabase
from .query import CreateTable, InsertRow
from .fields import IDField
from greysqale import query

class ModelTable:
    __db__ = None
    def __init__(self, **kwargs):
        self._fields = {
            f'{self.__class__._table_name()}Id': None
        }

        for key, val in kwargs.items():
            self._fields[key] = val

    def __getattribute__(self, name: str):
        _data = object.__getattribute__(self, '_data')
        if name in _data:
            return _data[name]
        return object.__getattribute__(self, name)

    @classmethod
    def _table_name(cls):
        return cls.__name__

    @classmethod
    def _create_table_query(cls):
        fields = [
            IDField(name = f"id"),
        ]

        x = inspect.getmembers(cls, lambda x: not inspect.isroutine(x))
        x = [a for a in x if not (a[0].startswith('__') and a[0].endswith('__'))]
        
        cls.__fields__ = ['id'] + [a[0] for a in x]
        
        for a in x:
            a[1].field_name = a[0]
            fields.append(a[1])

        query = CreateTable(cls._table_name(), fields)
        return query._build_query()

    @classmethod
    def _insert_table_query(cls, **kwargs):
        cls_fields = cls.__fields__
        for k, v in kwargs.items():
            if k not in cls_fields:
                raise GSQLQueryError("Non-existent column(s) passed in keyword arguments")
        query = InsertRow(cls._table_name(), **kwargs)
        return query._build_query()

    @classmethod
    def insert(cls, **kwargs):
        with cls.__db__.connection as conn:
            with conn.cursor() as c:
                c.execute(cls._insert_table_query(**kwargs))

        