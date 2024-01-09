#!/usr/bin/env python3
"""
Mock logging in
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """
    Get user information based on user ID. returns dict or none
    """
    return users.get(user_id)


@app.before_request
def before_request():
    """
    Function executed before all other functions.
    Sets the user information as a global variable on flask.g.user.
    """
    user_id = request.args.get('login_as', type=int)
    g.user = get_user(user_id)


@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(debug=True)
