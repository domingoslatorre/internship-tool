from flask import Flask, render_template, Blueprint, request, redirect, url_for

from users.database import User, save_user, get_user_by_email

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/register', methods=['GET'])
def register():
    return render_template('users/register.html')


@users.route('/register', methods=['POST'])
def register_post():
    # get data from form
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmation = request.form.get('password_confirmation')

    # validate data
    errors = []
    if not name:
        errors.append('Name is required')
    if not email:
        errors.append('Email is required')
    if not password:
        errors.append('Password is required')
    if not password_confirmation:
        errors.append('Password confirmation is required')
    if password != password_confirmation:
        errors.append('Password confirmation does not match password')

    # check if user already exists
    if get_user_by_email(email):
        errors.append('User with this email already exists')

    if errors:
        return render_template('users/register.html', errors=errors, name=name, email=email)

    # create user
    user = User.from_form(name=name, email=email, password=password)

    # save user to database
    save_user(user)

    # redirect to login page
    return redirect(url_for('users.login'))


@users.route('/login', methods=['GET'])
def login():
    return render_template('users/login.html')

