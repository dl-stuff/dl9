"""sqlite3 wrappers"""
from functools import lru_cache
import sqlite3
import os
from typing import Dict, List, Optional, Sequence, Tuple, Any

CONF_FILE = os.path.join(os.path.dirname(__file__), "conf.sqlite")


class DBData(sqlite3.Row):
    """subclass of sqlite3.Row"""

    def items(self) -> Tuple[str, Any]:
        for key in self.keys():
            yield key, self[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        try:
            if (res := self[key]) :
                return res
            return default
        except IndexError:
            return default


class DBManager:
    __slots__ = ["conn"]

    def __init__(self, db_file: str = CONF_FILE) -> None:
        """Bare bones DB conn/cursor manager"""
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = DBData

    def __del__(self):
        self.conn.close()
        self.conn = None

    @lru_cache
    def query_one(self, query: str, param: tuple = tuple()) -> DBData:
        cursor = self.conn.cursor()
        cursor.execute(query, param)
        return cursor.fetchone()

    def query_all(self, query: str, param: tuple = tuple()) -> List[DBData]:
        cursor = self.conn.cursor()
        cursor.execute(query, param)
        return cursor.fetchall()

    def query_all_as_dict(self, query: str, key_by: str = "_Id", param: tuple = tuple()) -> Dict[str, DBData]:
        cursor = self.conn.cursor()
        cursor.execute(query, param)
        return {row[key_by]: row for row in cursor.fetchall()}

    def pragma(self, operation: str, table: str) -> DBData:
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA {operation}({table})")
        return cursor.fetchall()


DBM = DBManager()


class FromDB:
    __slots__ = ["_query", "id", "_data", "name"]

    def __init_subclass__(cls, table: str = "", pk: str = "_Id") -> None:
        cls._query = f"SELECT * FROM {table} WHERE {pk}=?"

    def __init__(self, id: str) -> None:
        self.id = id
        self._data = DBM.query_one(self._query, param=(id,))
        self.name = None
        if self._data:
            self.name = self._data.get("_SecondName", self._data.get("_Name"))

    def __repr__(self) -> str:
        if self._data:
            return f"{self.id}-{self.name}"
        else:
            return str(self.id)
