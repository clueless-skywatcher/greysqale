from psycopg2.pool import SimpleConnectionPool, ThreadedConnectionPool

class GSQLPoolmaker:
    def __init__(self, minconn, maxconn, db, user, password, host, threaded = False) -> None:
        self.minconn = minconn
        self.maxconn = maxconn
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        
        if not threaded:
            self._conn_pool = SimpleConnectionPool(
                minconn, 
                maxconn, 
                database = db,
                user = user,
                password = password,
                host = host
            )
        else:
            self._conn_pool = ThreadedConnectionPool(
                minconn, 
                maxconn, 
                database = db,
                user = user,
                password = password,
                host = host
            )

    def get_connection(self):
        return self._conn_pool.getconn()

    def put_connection(self):
        return self._conn_pool.putconn()
        
    def __enter__(self):
        self.connection = self._conn_pool.getconn()
        return self.connection

    def __exit__(self, ):
        self._conn_pool.putconn(self.connection)