import os
import sqlite3
import logging

import bcrypt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
    logger.info('Creating database connection...')
    connection = sqlite3.connect('database.sqlite')

    with open('schema.sql') as f:
        logger.info('Creating database schema...')
        connection.executescript(f.read())

    logger.info('Database schema created.')


def setup_admin():
    name = os.environ.get('ADMIN_NAME')
    email = os.environ.get('ADMIN_EMAIL')
    password = bcrypt.hashpw(os.environ.get('ADMIN_PASSWORD').encode('utf-8'), bcrypt.gensalt())

    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    if result is not None:
        logger.info('Admin user already exists.')
        return

    logger.info('Creating admin user.')
    cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                   (name, email, password))
    connection.commit()
    connection.close()
