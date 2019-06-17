"""
Default Flask app startup settings.

Overridable by specifying APP_SETTINGS_FILE.
"""

MONGO_DB_NAME = "ctf"
MONGO_ADDR = "mongo"
MONGO_PORT = 27017
MONGO_USER = None
MONGO_PW = None

SECRET_KEY = "INSECURE_DEFAULT_CHANGE_ME"

SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_PATH = "/"
SESSION_COOKIE_NAME = "flask"
