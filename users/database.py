import sqlite3
from dataclasses import dataclass
from datetime import datetime
import bcrypt


@dataclass
class User:
    def __init__(self, _id, name, email, password, created_at):
        self.id = _id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at

    @staticmethod
    def from_form(name, email, password):
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return User(None, name, email, hash_password, datetime.now())

    @staticmethod
    def from_db_row(row):
        return User(*row)


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


def get_user_by_email(email) -> User | None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    connection.close()
    if result is None:
        return None
    return User.from_db_row(result)
