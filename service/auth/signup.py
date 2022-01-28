from models.conn import userCollections, userDataCollections
from service.JsonResponse import JsonResponse
from models.config import Config as SETTING
import secrets
from passlib.hash import sha256_crypt
from service.checkers.commonChecker import displayNameChecker, emailCheckerForSignup, passwordChecker, usernameCheckerForSignup
import requests

# roles
# 0 - user
# 1 - worker
# 2 - admin
# 3 - superuser

def signup(requestObj, ipAddress, environ):
    response = JsonResponse()

    try:
        data = []
        usernameBool = False
        passwordBool = False
        displayNameBool = False

        emailBool, email = emailCheckerForSignup(response, requestObj.get("email"))
        if emailBool:
            usernameBool, username = usernameCheckerForSignup(response, requestObj.get("username"))
        if usernameBool:
            passwordBool, password = passwordChecker(response, requestObj.get("password"))
        if passwordBool:
            displayNameBool, displayName = displayNameChecker(response, requestObj.get("displayName"))
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
            }
            if SETTING.DEBUG == False:
                ipResponse = requests.get(f"{SETTING.IP_LOOKUP_WEBSITE}{environ['HTTP_X_FORWARDED_FOR']}").json()
                if ipResponse['status'] == "success":
                    userObj["ip"] = environ['HTTP_X_FORWARDED_FOR']
                    userObj["country"] = ipResponse['country']
                    userObj["region"] = ipResponse['regionName']
                    userObj["city"] = ipResponse['city']
            
            if requestObj.get("role") != None:
                if requestObj.get("role") == SETTING.WORKER_USER:
                    userObj['role'] = 1
                elif requestObj.get("role") == SETTING.ADMIN_USER:
                    userObj['role'] = 2
                elif requestObj.get("role") == SETTING.SUPER_USER:
                    userObj['role'] = 3

            
            userId = userCollections.insert_one(userObj).inserted_id
            userDataObj = {
                "userId" : userId,
                "tv" : [],
                "movie" : []
            }
            userDataCollections.insert_one(userDataObj)
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
        response.setError("Error in Signup => Contact Mr. Grey" + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()


def generateApiKey(apiKey):
    apiCheck = userCollections.count_documents({"api" : apiKey})
    if apiCheck != 0:
        return generateApiKey(secrets.token_urlsafe(32))
    else:
        return apiKey