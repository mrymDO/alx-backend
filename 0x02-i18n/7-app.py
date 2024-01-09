#!/usr/bin/env python3
"""Infer appropriate time zone"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz import UnknownTimeZoneError, timezone
from datetime import datetime

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


def get_user(user_id: int) -> dict:
    """
    Get user information based on user ID. returns dict or none
    """
    return users.get(user_id, {})


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
    locale: str = request.args.get("locale", "")
    if locale in app.config["LANGUAGES"]:
        return locale

    if g.user:
        locale = g.user.get("locale", "")
        if locale and locale in app.config["LANGUAGES"]:
            return locale

    locale = request.headers.get("locale", "")
    if locale and locale in app.config["LANGUAGES"]:
        return locale

    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone() -> str:
    """
    Get the timezone for localization.
    """
    try:
        if request.args.get("timezone"):
            time_zone = request.args.get("timezone")
            _ = timezone(time_zone)  # Validate timezone
        elif g.user and g.user.get("timezone"):
            time_zone = g.user.get("timezone")
            _ = timezone(time_zone)  # Validate timezone
        else:
            time_zone = app.config["BABEL_DEFAULT_TIMEZONE"]
    except UnknownTimeZoneError:
        time_zone = app.config["BABEL_DEFAULT_TIMEZONE"]

    return time_zone


@app.route('/')
def index():
    """
    Render the index page.
    """
    current_time = datetime.now(pytz.timezone(get_timezone()))
    return render_template('7-index.html', time=current_time)


if __name__ == '__main__':
    app.run(debug=True)
