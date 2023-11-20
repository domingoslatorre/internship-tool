from flask import Flask, render_template, Blueprint, request, redirect, url_for, session, flash

import auth
from users.database import User, save_user, get_user_by_email, update_user

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


@users.route('/login', methods=['POST'])
def login_post():
    # get data from form
    email = request.form.get('email')
    password = request.form.get('password')

    # validate data
    errors = []
    if not email:
        errors.append('Email is required')
    if not password:
        errors.append('Password is required')

    # check if user exists
    user = get_user_by_email(email)
    if not user:
        errors.append('Invalid email or password')

    # check if user is active
    if user and not user.active:
        errors.append('User is not active')

    # check if password is correct
    if user and not user.check_password(password):
        errors.append('Invalid email or password')

    if errors:
        return render_template('users/login.html', errors=errors)

    # define session for logged in user
    session['user_id'] = user.id
    session['user_email'] = user.email
    session['user_name'] = user.name
    session['user_role'] = user.role

    # redirect to home page
    return redirect(url_for('index'))


@users.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))


@users.route('/profile', methods=['GET'])
@auth.minimum_role('USER')
def profile():
    return render_template('users/profile.html')


@users.route('/password', methods=['POST'])
@auth.minimum_role('USER')
def change_password():
    # get data from form
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    password_confirmation = request.form.get('password_confirmation')

    # validate data
    errors = []
    if not current_password:
        errors.append('Current Password is required')
    if not new_password:
        errors.append('New Password is required')
    if not password_confirmation:
        errors.append('Password confirmation is required')
    if new_password != password_confirmation:
        errors.append('Password confirmation does not match password')

    # check if user is active
    user = get_user_by_email(session['user_email'])
    if user and not user.active:
        errors.append('User is not active')

    # check if password is correct
    if user and not user.check_password(current_password):
        errors.append('Invalid current password')

    # check if new password is different from current password
    if user and user.check_password(new_password):
        errors.append('New password must be different from current password')

    if errors:
        return render_template('users/profile.html', errors=errors)

    # change password
    user.change_password(new_password)

    # save user to database
    update_user(user)

    # redirect to profile page
    flash('Password changed successfully')
    return redirect(url_for('users.profile'))


@users.route('/', methods=['GET'])
@auth.minimum_role('ADMIN')
def users_list():
    return render_template('users/list.html')
