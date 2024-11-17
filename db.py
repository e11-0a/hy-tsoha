from config import config
from psycopg_pool import ConnectionPool

connection_pool = ConnectionPool(
    config["database"]["connection_string"], open=True)