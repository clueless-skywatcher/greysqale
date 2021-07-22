import psycopg2
from psycopg2 import pool
from .pool import GSQLPoolmaker
from .errors import GSQLDatabaseError

SQL_GET_TABLES = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"

class GSQLDatabase:
    def __init__(
        self,
        username,
        password,
        dbname,
        host = '127.0.0.1',
        port = '5432',
        pool = 'none',
        pool_min = 1,
        pool_max = 10
    ):
        self.username = username
        self.password = password
        self.dbname = dbname
        self.host = host
        self.port = port

        self.pool = pool
        self.pool_max = pool_max
        self.pool_min = pool_min

        self.table_classes = []

        self.connect()

    def connect(self):
        if self.pool == 'none':
            self.connection = psycopg2.connect(dbname = self.dbname, user = self.username, password = self.password)
        elif self.pool == 'simple':
            poolmaker = GSQLPoolmaker(self.pool_min, self.pool_max, self.dbname, self.username, self.password, self.host, threaded = False)
            self.connection = poolmaker.get_connection()
        elif self.pool == 'threaded':
            poolmaker = GSQLPoolmaker(self.pool_min, self.pool_max, self.dbname, self.username, self.password, self.host, threaded = True)
            self.connection = poolmaker.get_connection()
        else:
            raise GSQLDatabaseError("Invalid option in pool variable. pool can be 'none', 'simple' or 'threaded'")

    def tables(self):
        with self.connection as conn:
            with conn.cursor() as c:
                c.execute(SQL_GET_TABLES)
                tbls = [x[0] for x in c.fetchall()]
        return tbls

    def add(self, table_cls):
        table_cls.__db__ = self
        self.table_classes.append(table_cls)
        with self.connection as conn:
            with conn.cursor() as c:
                c.execute(table_cls._create_table_query())
        