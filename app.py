import os

from flask import Flask, render_template
from flask_wtf import CSRFProtect

import database
from users.handler import users

app = Flask(__name__)
app.register_blueprint(users)
app.secret_key = os.environ.get('APP_SECRET_KEY').encode('utf-8')
csrf = CSRFProtect(app)

database.migrate()
database.setup_admin()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
