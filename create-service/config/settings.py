from decouple import Csv, config

DATABASE = {
    "mongo_url": config("MONGO_URL"),
    "db_name": config("DB_NAME"),
}

LOGGING_CONFIG_FILE = config("LOGGING_CONFIG_FILE", default="logging-dev.conf")
