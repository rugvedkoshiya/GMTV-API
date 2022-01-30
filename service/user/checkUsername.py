from models.conn import userCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from models.config import Config as SETTING


def checkUsername(apiKey, reqObj):
    response = JsonResponse()

    try:
        data = []

        userObj = apiChecker(apiKey, response)
        if userObj:
            if reqObj.get("username"):
                usernameObj = userCollections.find_one(
                    {
                        "username" : reqObj.get("username")
                    }
                )
                if usernameObj:
                    data = {
                        "username": reqObj.get("username"),
                        "available": False,
                    }
                    response.setStatus(200)
                    response.setMessage("Username is not available")
                else:
                    data = {
                        "username": reqObj.get("username"),
                        "available": True,
                    }
                    response.setStatus(200)
                    response.setMessage("Username is available")
            else:
                response.setStatus(400)
                response.setMessage("Useraname not provided")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in demo Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()