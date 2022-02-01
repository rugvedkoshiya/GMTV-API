from os import getenv

class Config():
    DEBUG = False if getenv("DEBUG") == "False" else True
    PORT = getenv("PORT")
    DOCUMENTATION_LINK = "https://gmtv.stoplight.io/docs/v1/overview.json"
    SECRET_KEY = getenv("SECRET_KEY")
    MONGO_LINK = getenv("MONGO_LINK")
    MONGO_USERNAME = getenv("MONGO_USERNAME")
    MONGO_PASSWORD = getenv("MONGO_PASSWORD")
    DATABASE_NAME = getenv("DATABASE_NAME")
    TV_COLLECTION_NAME = "TV"
    MOVIE_COLLECTION_NAME = "Movie"
    USER_COLLECTION_NAME = "Users"
    USER_DATA_COLLECTION_NAME = "UserData"
    IP_LOOKUP_WEBSITE = "http://ip-api.com/json/"
    SUPER_USER = getenv("SUPER_USER")
    ADMIN_USER = getenv("ADMIN_USER")
    WORKER_USER = getenv("WORKER_USER")
    VERSION = "v1"
    PAGING = 20