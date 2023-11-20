import sqlite3
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    def __init__(self, name, email, password):
        self.id = None
        self.name = name
        self.email = email
        self.password = password
        self.created_at = datetime.now()


def get_connection():
    return sqlite3.connect('database.sqlite')


def save_user(user) -> User:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                   (user.name, user.email, user.password))

    user.id = cursor.lastrowid

    connection.commit()
    connection.close()
    return user

