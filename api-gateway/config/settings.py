from decouple import Csv, config

CORS_ORIGIN_WHITELIST = config("CORS_ORIGIN_WHITELIST", cast=Csv())
LOGGING_CONFIG_FILE = config("LOGGING_CONFIG_FILE", default="logging-dev.conf")
