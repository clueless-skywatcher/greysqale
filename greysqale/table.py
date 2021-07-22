from .errors import GSQLQueryError
import inspect

from .database import GSQLDatabase
from .query import CreateTable, InsertRow, SelectWithoutFilter
from .fields import IDField

class ModelTable:
    __db__ = None
    def __init__(self, **kwargs):
        self._fields = {}

        for key, val in kwargs.items():
            self._fields[key] = val

    def __getattribute__(self, name: str):
        _fields = object.__getattribute__(self, '_fields')
        if name in _fields:
            return _fields[name]
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

    @classmethod
    def _select_table_query(cls, *columns):
        if '*' in columns and len(columns) > 1:
            raise GSQLQueryError("No point in writing * when providing other columns")
        s = SelectWithoutFilter(cls._table_name(), *columns)
        return s._build_query()

    @classmethod
    def select(cls, *columns):
        with cls.__db__.connection as conn:
            with conn.cursor() as c:
                c.execute(cls._select_table_query(*columns))
                column_names = [desc[0] for desc in c.description]
                rows = c.fetchall()
                final_rows = []
                for row in rows:
                    row_val = {}
                    for c, r in zip(column_names, row):
                        row_val[c] = r
                    final_rows.append(cls(**row_val))
        return final_rows

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._fields})"
