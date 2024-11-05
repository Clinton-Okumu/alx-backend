#!/usr/bin/env python3
"""Basic Flask app with Babel, user settings, timezone and time display"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
import pytz
from datetime import datetime


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


def get_user():
    """Returns user dictionary or None if ID not found"""
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request():
    """Find user if any"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Get locale based on priority"""
    # 1. URL parameter
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # 2. User Settings
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    # 3. Request Headers
    locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if locale:
        return locale

    # 4. Default Locale
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """Get timezone based on priority"""
    try:
        # 1. URL Parameter
        timezone = request.args.get('timezone')
        if timezone:
            return pytz.timezone(timezone)

        # 2. User Settings
        if g.user and g.user.get('timezone'):
            return pytz.timezone(g.user.get('timezone'))

    except pytz.exceptions.UnknownTimeZoneError:
        pass

    # 3. Default UTC
    return pytz.timezone(app.config['BABEL_DEFAULT_TIMEZONE'])


@app.route('/', strict_slashes=False)
def index():
    """Return homepage"""
    current_time = format_datetime(datetime.now(get_timezone()))
    return render_template('index.html', current_time=current_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
