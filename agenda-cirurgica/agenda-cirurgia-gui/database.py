import sqlite3

from config import BANCO


def conectar():
    return sqlite3.connect(BANCO)