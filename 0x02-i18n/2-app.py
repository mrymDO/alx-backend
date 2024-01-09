#!/usr/bin/env python3
"""Get locale from request"""
from flask import Flask
from flask import request
from flask_babel import Babel
from flask import render_template

app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """config falsk babel"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Gets the best match from supported languages."""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """index"""
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run(debug=True)