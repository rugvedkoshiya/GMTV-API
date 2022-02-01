from models.conn import userCollections, userDataCollections
from service.JsonResponse import JsonResponse
from models.config import Config as SETTING
import secrets
from passlib.hash import sha256_crypt
from service.checkers.commonChecker import displayNameChecker, emailCheckerForSignup, ipAddressChecker, passwordChecker, usernameCheckerForSignup
import requests

# roles
# 0 - user
# 1 - worker
# 2 - admin
# 3 - superuser

def signup(reqObj, ipAddress):
    response = JsonResponse()

    try:
        data = []
        usernameBool = False
        displayNameBool = False

        emailBool, email = emailCheckerForSignup(response, reqObj.get("email"))
        if emailBool:
            usernameBool, username = usernameCheckerForSignup(response, reqObj.get("username"))
        if usernameBool:
            password = passwordChecker(response, reqObj.get("password"))
        if password:
            displayNameBool, displayName = displayNameChecker(response, reqObj.get("displayName"))
        if displayNameBool:

            # generate API key
            apiKey = generateApiKey(secrets.token_urlsafe(32))
            userObj = {
                "email" : email,
                "password" : sha256_crypt.hash(password),
                "username": username,
                "displayName": displayName,
                "ip" : ipAddress,
                "country" : None,
                "region" : None,
                "city" : None,
                "api" : apiKey,
                "role" : 0,
                "emailVerified" : False,
                "emailVerifiedOn" : None
            }
            ipAddressChecker()
            
            if reqObj.get("role") != None:
                if reqObj.get("role") == SETTING.WORKER_USER:
                    userObj['role'] = 1
                elif reqObj.get("role") == SETTING.ADMIN_USER:
                    userObj['role'] = 2
                elif reqObj.get("role") == SETTING.SUPER_USER:
                    userObj['role'] = 3

            
            userCollections.insert_one(userObj).inserted_id
            data = {
                "apiKey": apiKey,
                "email": email,
                "username": username,
                "displayName": displayName,
                "success": True,
            }
            response.setStatus(200)
            response.setMessage("Signup successfully")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in Signup Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()


def generateApiKey(apiKey):
    apiCheck = userCollections.count_documents({"api" : apiKey})
    if apiCheck != 0:
        return generateApiKey(secrets.token_urlsafe(32))
    else:
        return apiKey