from flask import g


class JsonResponse:
    def __init__(self, status=0, error="", message="", data={}):
        self.__error = error
        self.__message = message
        self.__status = status
        self.__data = data

    def getError(self):
        return self.__error

    def setError(self, error):
        self.__error = error

    def getMessage(self):
        return self.__message

    def setMessage(self, message):
        self.__message = message

    def getData(self):
        return self.__data

    def setData(self, data):
        self.__data = data

    def get_status(self):
        return self.__status

    def setStatus(self, status):
        self.__status = status

    def returnResponse(self):
        response = {
            "status": self.__status,
            "message": self.__message,
            "error": self.__error,
            "data": self.__data,
        }
        g.response = response
        return response
