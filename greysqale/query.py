import psycopg2

from .fields import IntegerField, IDField, VarcharField
from .constraints import NotNull, Serial

SQL_CREATE_QUERY = "CREATE TABLE IF NOT EXISTS {}({});"

class Query:
    def __init__(self, *args, **kwargs):
        self._query = None
        self.cursor = None
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        return self.cursor.execute(self.query.format(self.args))

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

    @property
    def generated_query(self):
        return self._query