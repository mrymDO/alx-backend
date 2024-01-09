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
def get_locale():
    """
    Get the locale for localization.
    """
    requested_locale = request.args.get('locale')
    if requested_locale and requested_locale in app.config['LANGUAGES']:
        return requested_locale

    # 2. Locale from user settings
    if g.user and 'locale' in g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    # 3. Locale from request headers
    header_locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if header_locale:
        return header_locale

    # 4. Default locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(debug=True)
