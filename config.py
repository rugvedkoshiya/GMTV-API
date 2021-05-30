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
    VERSION = "v1"

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
    VERSION = "v1"

class ErrorStringManagement():
    INVALID_API_401 = {"success": False, "status_message": "Invalid API Key: You must be granted a valid key."}
    NOT_FOUND_404 = {"success": False, "status_message": "The resource you requested could not be found."}
    INTERNAL_SERVER_ERROR_500 = {"success": False,"status_message": "Internal Server Error"}
    BAD_REQUEST_400 = {"success": False,"status_message": "Bad Request"}
    FORBIDDEN_403 = {"success": False,"status_message": "Forbidden"}

    NOT_FOUND_EPISODE_404 = "This season don't have that much episodes"
    NOT_FOUND_SEASON_404 = "This tv show don't have that much seasons"
    NOT_FOUND_LANGUAGE_404 = "This tv show don't have that language"
    NOT_FOUND_NOT_WATCHED_404 = "This tv show don't have that language"

    BAD_REQUEST_INCORRECT = "Request is not proper"
    BAD_REQUEST_LANGUAGE_IS_NOT_AVAILABLE_400 = "Provided anguage is not available for this movie"
    BAD_REQUEST_LANGUAGE_NOT_PROVIDED_400 = "Watched language not provided"
    BAD_REQUEST_LANGUAGE_INVALID_400 = "Provieded language is invalid, use ISO 639 language code"
    BAD_REQUEST_MOVIE_NOT_WATCHED_400 = "You haven't watched provided movie"

class SuccessStringManagement():
    ADDED_TO_WATCHED_LIST = {'status' : 200, 'message' : 'Added to watched list'}
    EDITED_TO_WATCHED_LIST = {'status' : 200, 'message' : 'Edited to watched list'}
    REMOVED_FROM_WATCHED_LIST = {'status' : 200, 'message' : 'Removed from watched list'}