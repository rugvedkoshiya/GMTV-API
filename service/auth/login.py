from models.conn import userCollections
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import userCheckerForLogin, passwordChecker
from models.config import Config as SETTING
from passlib.hash import sha256_crypt

from service.checkers.generater import roleGenerator


def login(reqObj):
    response = JsonResponse()

    try:
        data = []

        userObj = userCheckerForLogin(response, reqObj.get("username"))
        if userObj:
            password = passwordChecker(response, reqObj.get("password"))
        if password:
            if sha256_crypt.verify(password, userObj.get("password")):
                data = {
                    "email": userObj.get("email"),
                    "username": userObj.get("username"),
                    "displayName": userObj.get("displayName"),
                    "country": userObj.get("country"),
                    "api": userObj.get("api"),
                    "role": roleGenerator(userObj.get("role")),
                    "emailVerified": userObj.get("emailVerified"),
                    "emailVerifiedOn": userObj.get("emailVerifiedOn"),
                }
            else:
                response.setStatus(403)
                response.setError("Wrong password")

        response.setStatus(200)
        response.setMessage("logged in successfully")
        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in Login Contact Mr. Grey =>" + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()