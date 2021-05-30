from config import ErrorStringManagement

class INVALID_API_401_EXCEPTION(Exception):
    """
    Exception raised for invalid api key provided.
    """

    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return ErrorStringManagement.INVALID_API_401['status_message']

class NOT_FOUND_404_EXCEPTION(Exception):
    """
    Exception raised when resources not found.
    """

    def __init__(self, message=ErrorStringManagement.NOT_FOUND_404['status_message']):
        self.message = message
        super().__init__(self)

    def __str__(self):
        return self.message

class BAD_REQUEST_400_EXCEPTION(Exception):
    """
    Exception raised when required query not provided.
    """

    def __init__(self, message=ErrorStringManagement.BAD_REQUEST_400['status_message']):
        self.message = message
        super().__init__(self)

    def __str__(self):
        return self.message