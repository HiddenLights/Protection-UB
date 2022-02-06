from os import environ

SESSION_STRING = environ.get("SESSION_STRING", None)
ARQ_API_URL = environ.get("ARQ_API_URL","http://thearq.tech/")
ARQ_API_KEY = environ.get("ARQ_API_KEY", None)
API_ID = int(environ.get("API_ID", 6))
API_HASH = environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
USERBOT_PREFIX = environ.get("USERBOT_PREFIX", None)
