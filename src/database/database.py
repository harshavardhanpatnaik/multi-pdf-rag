import sqlite3
import os

db = "database.db"


def get_connection():
    conn = sqlite3.Connection(db)
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS documents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL,
    filename TEXT NOT NULL,
    embedded INTEGER)
                   """)
    conn.close()


def insert_pdf(path):
    filename = os.path.basename(path)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
                   INSERT INTO documents(path,filename,embedded) values(?,?,?)
                   """,
        (path, filename, 0),
    )
    document_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return document_id


def check_pdf(path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
                   select * from documents where path = ?
                   """,
        (path,),
    )
    data = cursor.fetchall()
    conn.close()

    return data


def show():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" SELECT id,filename FROM documents where embedded = 1""")
    data = cursor.fetchall()
    conn.close()

    return data


def ret(document_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT """)
