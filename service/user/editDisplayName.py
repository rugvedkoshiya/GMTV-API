from models.conn import userCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from models.config import Config as SETTING
from service.checkers.generater import roleGenerator


def editDisplayName(apiKey, reqObj):
    response = JsonResponse()

    try:
        data = []

        userObj = apiChecker(apiKey, response)
        if userObj:
            if reqObj.get("displayName"):
                userCollections.update_one(
                    {
                        "_id" : userObj.get("_id"),
                    },
                    {
                        "$set": {
                            "displayName": reqObj.get("displayName")
                        }
                    }
                )
                data = {
                    "email": userObj.get("email"),
                    "username": userObj.get("username"),
                    "displayName": reqObj.get("displayName"),
                    "country": userObj.get("country"),
                    "api": userObj.get("api"),
                    "role": roleGenerator(userObj.get("role")),
                }
                response.setStatus(200)
                response.setMessage("Display Name changed")
            else:
                response.setStatus(400)
                response.setMessage("Display Name not provided")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in demo Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()