import inspect

from .database import GSQLDatabase
from .query import CreateTable
from .fields import IDField
from greysqale import query

class ModelTable:
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
            IDField(name = f"Id"),
        ]

        x = inspect.getmembers(cls, lambda x: not inspect.isroutine(x))
        x = [a for a in x if not (a[0].startswith('__') and a[0].endswith('__'))]
        
        for a in x:
            a[1].field_name = a[0]
            fields.append(a[1])

        query = CreateTable(cls._table_name(), fields)
        return query._build_query()