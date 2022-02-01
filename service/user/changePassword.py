from models.conn import userCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from models.config import Config as SETTING
from service.checkers.commonChecker import passwordChecker
from passlib.hash import sha256_crypt


def changePassword(apiKey, reqObj):
    response = JsonResponse()

    try:
        data = []

        userObj = apiChecker(apiKey, response)
        if userObj:
            password = passwordChecker(response, reqObj.get("newPassword"))
        if password:
            if sha256_crypt.verify(reqObj.get("oldPassword"), userObj.get("password")):
                userCollections.update_one(
                    {
                        "_id" : userObj.get("_id")
                    },
                    {
                        "$set": {
                            "password": sha256_crypt.hash(password),
                        }
                    }
                )
                response.setStatus(200)
                response.setMessage("Password changed")
            else:
                response.setStatus(403)
                response.setMessage("Wrong password")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in demo Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()