#!/usr/bin/env python3
"""Parametrize templates"""
from flask import Flask, render_template
from flask_babel import Babel, _
from flask import request
import os

app = Flask(__name__)
babel = Babel(app)


class Config:
    """config falsk babel"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Gets the best match from supported languages."""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def index():
    """index"""
    return render_template('3-index.html', title=_("Welcome to Holberton"), header=_("Hello world!"))


if __name__ == '__main__':
    app.run(debug=True)
