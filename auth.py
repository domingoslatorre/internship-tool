import logging
from functools import wraps

from flask import session, redirect, url_for

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def minimum_role(role):
    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get('user_id'):
                logger.warning('User is not logged in.')
                return redirect(url_for('users.login'))

            if session.get('user_role') == 'ADMIN':
                return view(*args, **kwargs)

            if session.get('user_role') != role:
                logger.warning('User does not have the required role.')
                return redirect(url_for('index'))
            return view(*args, **kwargs)

        return wrapped

    return login_required
