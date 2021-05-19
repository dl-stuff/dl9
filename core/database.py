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

    def textlabel_view(self, table: str, textfields: Sequence) -> str:
        fields = []
        joins = []
        for field in self.pragma("table_info", table):
            field = field["name"]
            if field in textfields:
                for region in TEXT_REGIONS:
                    fields.append(f"TextLabel{region}{field}._Text AS {field}{region}")
                    joins.append(f"LEFT JOIN TextLabel{region} AS TextLabel{region}{field} ON {table}.{field}=TextLabel{region}{field}._Id")
            else:
                fields.append(f"{table}.{field}")
        fieldstr = ",".join(fields)
        joinsstr = "\n" + "\n".join(joins)
        viewname = f"view_{table}"
        query = f"DROP VIEW IF EXISTS {viewname}"
        self.conn.execute(query)
        query = f"CREATE VIEW {viewname} AS SELECT {fieldstr} FROM {table} {joinsstr}"
        self.conn.execute(query)
        self.conn.commit()
        return viewname


DBM = DBManager()
