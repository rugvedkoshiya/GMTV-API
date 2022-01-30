from models.conn import userCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from models.config import Config as SETTING


def changeEmail(apiKey, reqObj):
    response = JsonResponse()

    try:
        data = []

        userObj = apiChecker(apiKey, response)
        if userObj:
            if reqObj.get("email"):
                emailObj = userCollections.find_one(
                    {
                        "email" : reqObj.get("email")
                    }
                )
                if emailObj:
                    data = {
                        "username": userObj.get("email"),
                        "emailVerified": userObj.get("emailVerifiedOn"),
                        "emailVerifiedOn": userObj.get("emailVerifiedOn"),
                        "status": False,
                    }
                    response.setStatus(409)
                    response.setMessage("Email is already in use")
                else:
                    userCollections.update_one(
                        {
                            "_id" : userObj.get("_id")
                        },
                        {
                            "$set": {
                                "email": reqObj.get("email"),
                                "emailVerified": False,
                                "emailVerifiedOn": None,
                            }
                        }
                    )
                    data = {
                        "username": reqObj.get("email"),
                        "emailVerified": False,
                        "emailVerifiedOn": None,
                        "status": True,
                    }
                    response.setStatus(200)
                    response.setMessage("Email changed")
            else:
                response.setStatus(400)
                response.setMessage("Email not provided")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in demo Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()