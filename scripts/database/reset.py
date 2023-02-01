import sqlite3
from . import*


def reset(db):
    deleteAllTable(db)
    setup(db)
