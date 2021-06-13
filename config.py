class Config(object):
    DEBUG = False
    DOCUMENTATION_LINK = "https://gmtv.stoplight.io/docs/v1/overview.json"

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = "Your Secret Key For Production"
    MONGO_LINK = "mongodb+srv://<username>:<password>@<cluster-link>/<database name>?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
    MONGO_USERNAME = "Username"
    MONGO_PASSWORD = "Password"
    DATABASE_NAME = "Database Name"
    TV_COLLECTION_NAME = "TV Show Collection Name"
    MOVIE_COLLECTION_NAME = "Movie Collection Name"
    USER_COLLECTION_NAME = "Users Collection Name"
    USER_DATA_COLLECTION_NAME = "Users Data Collection Name"
    IP_LOOKUP_WEBSITE = "http://ip-api.com/json/"
    SUPER_USER = "Superuser Auth Token"
    ADMIN_USER = "Admin Auth Token"
    WORKER_USER = "Worker Auth Token"
    VERSION = "v2-beta"
    PAGING = 20

class TestingConfig(Config):
    DEBUG = True
    SECRET_KEY = "Your Secret Key For Production"
    MONGO_LINK = "mongodb+srv://<username>:<password>@<cluster-link>/<database name>?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
    MONGO_USERNAME = "Username"
    MONGO_PASSWORD = "Password"
    DATABASE_NAME = "Database Name"
    TV_COLLECTION_NAME = "TV Show Collection Name"
    MOVIE_COLLECTION_NAME = "Movie Collection Name"
    USER_COLLECTION_NAME = "Users Collection Name"
    USER_DATA_COLLECTION_NAME = "Users Data Collection Name"
    IP_LOOKUP_WEBSITE = "http://ip-api.com/json/"
    SUPER_USER = "Superuser Auth Token"
    ADMIN_USER = "Admin Auth Token"
    WORKER_USER = "Worker Auth Token"
    VERSION = "v2-beta"
    PAGING = 20