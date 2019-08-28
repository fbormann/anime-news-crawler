import os
from pony.orm import Database

db = Database()

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "user": os.environ["DB_USER"],
    "pwd": os.environ["DB_PWD"]
}