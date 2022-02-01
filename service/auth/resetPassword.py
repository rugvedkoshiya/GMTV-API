from datetime import datetime, timedelta
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import passwordChecker, userCheckerForLogin
from models.config import Config as SETTING
from models.conn import resetPassword, userCollections
from passlib.hash import sha256_crypt


def getResetPassword(resetKey, ipAddress):
    response = JsonResponse()

    try:
        data = []

        resetObj = resetPassword.find_one({"resetKey": resetKey})
        if resetObj:
            if not resetObj.get("resetOn"):
                currentDatetime = datetime.now()
                if (currentDatetime - timedelta(hours=24)) < resetObj.get("requestedOn"):
                    userObj = userCollections.find_one({"_id": resetObj.get("userId")}, {"email": True, "_id": False}) 
                    data = {
                        "email": userObj.get("email")
                    }
                    response.setStatus(200)
                    response.setMessage("Give your new password")
                else:
                    response.setStatus(410)
                    response.setMessage("Password reset link has been expired")
            else:
                response.setStatus(409)
                response.setMessage("You have already reseted your password")
        else:
            response.setStatus(404)
            response.setMessage("Invalid Reset Key")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in Login => Contact Mr. Grey" + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()


def postResetPassword(resetKey, reqObj, ipAddress):
    response = JsonResponse()

    try:
        data = []

        password = passwordChecker(response, reqObj.get("password"))
        if password:
            resetObj = resetPassword.find_one({"resetKey": resetKey})
            if resetObj:
                if not resetObj.get("resetOn"):
                    currentDatetime = datetime.now()
                    if (currentDatetime - timedelta(hours=24)) < resetObj.get("requestedOn"):
                        userCollections.update_one(
                            {
                                "_id": resetObj.get("userId")
                            },
                            {
                                "$set": {
                                    "password": sha256_crypt.hash(password),
                                }
                            }
                        )
                        resetPassword.update_one(
                            {
                                "_id": resetObj.get("_id")
                            },
                            {
                                "$set": {
                                    "resetOn": currentDatetime,
                                }
                            }
                        )
                        response.setStatus(200)
                        response.setMessage("Your password has been successfully reset, Login to your account now")
                    else:
                        response.setStatus(410)
                        response.setMessage("Password reset link has been expired")
                else:
                    response.setStatus(409)
                    response.setMessage("You have already reseted your password")
            else:
                response.setStatus(404)
                response.setMessage("Invalid Reset Key")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in Login => Contact Mr. Grey" + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()