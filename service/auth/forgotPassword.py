from datetime import datetime, timedelta
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import ipAddressChecker, userCheckerForLogin
from models.config import Config as SETTING
from models.conn import resetPassword
import secrets

def forgotPassword(reqObj, ipAddress):
    response = JsonResponse()

    try:
        data = []

        userObj = userCheckerForLogin(response, reqObj.get("username"))
        if userObj:
            currentDatetime = datetime.now()
            resetObj = resetPassword.find_one({"userId": userObj.get("_id"), "resetOn": None})
            if resetObj:
                if (currentDatetime - timedelta(hours=24)) < resetObj.get("requestedOn"):
                    newResetObj = {}
                    ipAddressChecker(newResetObj, ipAddress)
                    resetPassword.update_one(
                        {
                            "_id": resetObj.get("_id")
                        },
                        {
                            "$set": {
                                "requestedOn": currentDatetime,
                                **newResetObj
                            }
                        }
                    )
                    sendEmail(userObj.get("email"), resetObj.get("resetKey"))
                else:
                    resetKey = generateResetKey(secrets.token_urlsafe(64))
                    newResetObj = {}
                    ipAddressChecker(newResetObj, ipAddress)
                    resetPassword.update_one(
                        {
                            "_id": resetObj.get("_id")
                        },
                        {
                            "$set": {
                                "requestedOn": currentDatetime,
                                "resetKey": resetKey,
                                **newResetObj
                            }
                        }
                    )
                    sendEmail(userObj.get("email"), resetKey)
            else:
                resetKey = generateResetKey(secrets.token_urlsafe(64))
                newResetObj = {
                    "userId": userObj.get("_id"),
                    "requestedOn": currentDatetime,
                    "resetOn": None,
                    "resetKey": resetKey
                }
                ipAddressChecker(newResetObj, ipAddress)
                resetPassword.insert_one(newResetObj)

                sendEmail(userObj.get("email"), resetKey)
                data = {
                    "email": userObj.get("email"),
                    "displayName": userObj.get("displayName"),
                }
                response.setStatus(200)
                response.setMessage("Password reset link has been emaild you")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in Login Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()


def generateResetKey(resetKey):
    resetCheck = resetPassword.count_documents({"resetKey" : resetKey})
    if resetCheck != 0:
        return generateResetKey(secrets.token_urlsafe(64))
    else:
        return resetKey

def sendEmail(email, resetKey):
    print(resetKey)