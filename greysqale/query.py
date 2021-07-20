from re import S
import psycopg2

from .fields import IntegerField, IDField, VarcharField
from .constraints import NotNull, Serial

SQL_CREATE_QUERY = "CREATE TABLE IF NOT EXISTS {}({});"
SQL_INSERT_QUERY = "INSERT INTO {}({}) VALUES {};"

class Query:
    def __init__(self, *args, **kwargs):
        self._query = None
        self.cursor = None
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        return self.cursor.execute(self.query.format(self.args))

    @property
    def generated_query(self):
        return self._query

    def _build_query(self):
        pass

class CreateTable(Query):
    def __init__(self, table_name, fields) -> None:
        super(CreateTable, self).__init__()
        self.table_name = table_name
        self.fields = fields
        self._build_query()

    def _build_query(self):
        field_declarations = ', '.join([f._build_str() for f in self.fields])
        s = SQL_CREATE_QUERY.format(self.table_name, field_declarations)
        self._query = s
        return s

class InsertRow(Query):
    def __init__(self, table_name, **kwargs):
        super(InsertRow, self).__init__()
        self.table_name = table_name
        self.kw = kwargs

    def _build_query(self):
        keys = tuple(self.kw.keys())
        values = tuple(self.kw.values())
        
        s = SQL_INSERT_QUERY.format(self.table_name, ', '.join(keys), values)
        self._query = s
        return s
