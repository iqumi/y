import logging

from cassandra.cluster import Cluster, NoHostAvailable, Session
from cassandra.connection import AuthenticationFailed
from cassandra.query import dict_factory
from cassandra.auth import PlainTextAuthProvider

from database.queries import QUERIES, KEYSPACE
from config import DEBUG, DB

# Настройки и подключение к бд


class Cassandra:
    logger = logging.getLogger('uvicorn.error')
    session: Session

    def __init__(self):
        self.username = DB["USERNAME"]
        self.password = DB["PASSWORD"]
        self.ip = DB["IP"]
        self.port = int(DB["PORT"])

    def __enter__(self):
        """Connect to database"""
        auth = PlainTextAuthProvider(self.username, self.password)
        cluster = Cluster([self.ip], self.port, auth_provider=auth)
        try:
            Cassandra.session = cluster.connect()
            self.logger.info('Подключение к бд прошло успешно')
        except (AuthenticationFailed, NoHostAvailable) as e:
            self.logger.error(f'Подключение с бд не установленно\n{str(e)}')
            raise RuntimeError()
        self._prepare_database()
        return self

    def _prepare_database(self):
        """Set some settings, create tables before using db"""
        Cassandra.session.row_factory = dict_factory
        Cassandra.session.execute(KEYSPACE)
        Cassandra.session.execute("USE chat")
        for table in QUERIES.values():
            Cassandra.session.execute(table.CREATE)
        if DEBUG: self._populate_testdata()

    def _populate_testdata(self):
        """Populate db with test data"""
        pass

    def __exit__(self, type, value, traceback):
        """Shutdown db connection"""
        Cassandra.session.shutdown()
