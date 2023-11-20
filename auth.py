import logging

from flask import session, redirect, url_for

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def login_required(view):
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            logger.warning('User is not logged in.')
            return redirect(url_for('users.login'))
        return view(*args, **kwargs)

    return wrapped
