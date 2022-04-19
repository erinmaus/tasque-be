from datetime import timedelta
import logging
from os import environ

TASQUE_SECRET_KEY = environ.get("TASQUE_SECRET_KEY")
TASQUE_JWT_EXPIRATION_MINUTES = timedelta(
    minutes=int(environ.get("TASQUE_JWT_EXPIRATION_MINUTES"))
)
TASQUE_LOGGING_LEVEL = logging.DEBUG
TASQUE_ORIGINS = [
    "http://localhost:3000",
    "https://tasque.itsyrealm.com",
    "https://master.d274tqh5gof6v7.amplifyapp.com/",
]
