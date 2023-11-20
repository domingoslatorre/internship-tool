from flask import Flask
import database

app = Flask(__name__)

database.migrate()
database.setup_admin()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
