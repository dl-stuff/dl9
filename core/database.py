"""sqlite3 wrappers"""
import sqlite3
import os
from typing import List, Sequence, Tuple, Any

CONF_FILE = os.path.join(os.path.dirname(__file__), "conf.sqlite")


class DBData(sqlite3.Row):
    """subclass of sqlite3.Row"""

    def items(self) -> Tuple[str, Any]:
        for key in self.keys():
            yield key, self[key]


TEXT_REGIONS = ("", "JP", "CN")


class DBManager:
    def __init__(self, db_file: str = CONF_FILE) -> None:
        """Bare bones DB conn/cursor manager"""
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = DBData
        self.tables = {}

    def __del__(self):
        self.conn.close()
        self.conn = None

    def query_one(self, query: str, param: tuple = tuple()) -> DBData:
        cursor = self.conn.cursor()
        cursor.execute(query, param)
        return cursor.fetchone()

    def query_all(self, query: str, param: tuple = tuple()) -> List[DBData]:
        cursor = self.conn.cursor()
        cursor.execute(query, param)
        return cursor.fetchall()

    def pragma(self, operation: str, table: str) -> DBData:
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA {operation}({table})")
        return cursor.fetchall()


DBM = DBManager()
