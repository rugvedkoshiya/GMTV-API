class ErrorStringManagement():
    INTERNAL_SERVER_ERROR_500 = {"success": False,"status_message": "Internal Server Error"}
    FORBIDDEN_403 = {"success": False,"status_message": "Forbidden"}

    # Not Found Error
    NOT_FOUND_404 = {"success": False, "status_message": "The resource you requested could not be found."}
    NOT_FOUND_EPISODE_404 = {"success": False, "status_message": "This season don't have that much episodes"}
    NOT_FOUND_SEASON_404 = {"success": False, "status_message": "This tv show don't have that much seasons"}
    NOT_FOUND_LANGUAGE_404 = {"success": False, "status_message": "This tv show don't have that language"}
    NOT_FOUND_NOT_WATCHED_404 = {"success": False, "status_message": "This tv show don't have that language"}

    # Bad Request Error
    BAD_REQUEST_400 = {"success": False,"status_message": "Bad Request"}
    BAD_REQUEST_LANGUAGE_IS_NOT_AVAILABLE_400 = {"success": False,"status_message": "Provided anguage is not available for this movie"}
    BAD_REQUEST_LANGUAGE_NOT_PROVIDED_400 = {"success": False,"status_message": "Watched language not provided"}
    BAD_REQUEST_LANGUAGE_INVALID_400 = {"success": False,"status_message": "Provieded language is invalid, use ISO 639 language code"}
    BAD_REQUEST_MOVIE_NOT_WATCHED_400 = {"success": False,"status_message": "You haven't watched provided movie"}

class SuccessStringManagement():
    ADDED_TO_WATCHED_LIST = {'success' : True, 'status_message' : 'Added to watched list'}
    EDITED_TO_WATCHED_LIST = {'success' : True, 'status_message' : 'Edited to watched list'}
    REMOVED_FROM_WATCHED_LIST = {'success' : True, 'status_message' : 'Removed from watched list'}

class AuthStringManagement():
    INVALID_API_401 = {"success": False, "status_message": "Invalid API Key: You must be granted a valid key."}
    USER_EXISTS_409 = {"success": False, "status_message": "User already exists"}
    USER_NOT_FOUND_404 = {"success": False, "status_message": "User not Found"}
    WRONG_PASSWORD_401 = {"success": False, "status_message": "Wrong Password"}
    PASSWORD_NOT_SAME_401 = {"success": False, "status_message": "Password does not same"}