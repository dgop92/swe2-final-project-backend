from decouple import Csv, config

LOGGING_CONFIG_FILE = config("LOGGING_CONFIG_FILE", default="logging-dev.conf")
