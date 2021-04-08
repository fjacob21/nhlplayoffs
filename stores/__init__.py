import memory_store
import postgres_store
from .store_config import StoreConfig

DB_TYPE_DEBUG = 1
DB_TYPE_TEST = 2
DB_TYPE_PROD = 3

_db_type = DB_TYPE_PROD
config = StoreConfig()


def get():
    if config.store == "memory":
        return memory_store.get()
    elif config.store == "postgres":
        return postgres_store.get(config.user, config._password, config.database, config.server, config.port)


def release():
    if config.store == "memory":
        memory_store.release()
    elif config.store == "postgres":
        postgres_store.release()


def set_type(db_type):
    global _db_type
    release()
    _db_type = db_type
