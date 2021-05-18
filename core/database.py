"""Simple sqlite3 wrapper"""
import sqlite3
import os

CONF_FILE = os.path.join(os.path.dirname(__file__), "conf.sqlite")


class DBManager:
    pass