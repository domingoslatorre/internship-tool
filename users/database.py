import sqlite3
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import bcrypt


class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'


@dataclass
class User:
    id: int | None
    name: str
    email: str
    password: bytes
    role: UserRole
    active: bool
    created_at: datetime

    @staticmethod
    def from_form(name, email, password):
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return User(None, name, email, hash_password, UserRole.USER, False, datetime.now())

    @staticmethod
    def from_db_row(row):
        return User(*row)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def change_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def get_connection():
    return sqlite3.connect('database.sqlite')


def save_user(user: User) -> User:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (name, email, password, role, active) VALUES (?, ?, ?, ?, ?)',
                   (user.name, user.email, user.password, user.role.value, user.active))

    user.id = cursor.lastrowid

    connection.commit()
    connection.close()
    return user


def get_user_by_email(email: str) -> User | None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    connection.close()
    if result is None:
        return None
    return User.from_db_row(result)


def get_user_by_id(id: int) -> User | None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
    result = cursor.fetchone()
    connection.close()
    if result is None:
        return None
    return User.from_db_row(result)


def update_user(user: User) -> User:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET name = ?, email = ?, password = ?, role = ?, active = ? WHERE id = ?',
                   (user.name, user.email, user.password, user.role, user.active, user.id))
    connection.commit()
    connection.close()
    return user


def find_all_users() -> list[User]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users ORDER BY name')
    result = cursor.fetchall()
    connection.close()
    return [User.from_db_row(row) for row in result]
