#!/usr/bin/env python3
"""
Use user locale
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)


class Config:
    """
    Config class for Flask app
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

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


@babel.localeselector
def get_locale() -> str:
    """
    Get the locale for localization.
    """
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale

    if g.user:
        locale = g.user.get("locale")
        if locale and locale in app.config["LANGUAGES"]:
            return locale

    locale = request.headers.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale

    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(debug=True)
