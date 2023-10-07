from decouple import Csv, config

CORS_ORIGIN_WHITELIST = config("CORS_ORIGIN_WHITELIST", cast=Csv())
LOGGING_CONFIG_FILE = config("LOGGING_CONFIG_FILE", default="logging-dev.conf")

CREATE_PEOPLE_SERVICE_URL: str | None = config(
    "CREATE_PEOPLE_SERVICE_URL", default=None
)
READ_PEOPLE_SERVICE_URL: str | None = config("READ_PEOPLE_SERVICE_URL", default=None)
UPDATE_PEOPLE_SERVICE_URL: str | None = config(
    "UPDATE_PEOPLE_SERVICE_URL", default=None
)
DELETE_PEOPLE_SERVICE_URL: str | None = config(
    "DELETE_PEOPLE_SERVICE_URL", default=None
)

PEOPLE_SERVICE_URLS = {
    "create": CREATE_PEOPLE_SERVICE_URL,
    "read": READ_PEOPLE_SERVICE_URL,
    "update": UPDATE_PEOPLE_SERVICE_URL,
    "delete": DELETE_PEOPLE_SERVICE_URL,
}

PEOPLE_SERVICE_TYPE = config("PEOPLE_SERVICE_TYPE", default="fake")
