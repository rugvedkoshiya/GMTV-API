from datetime import datetime, timedelta
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import ipAddressChecker, userCheckerForLogin
from models.config import Config as SETTING
from models.conn import resetPassword
import secrets
from flask_mail import Message
from swaggerConfig import mail, api


def forgotPassword(reqObj, ipAddress, environ):
    response = JsonResponse()
    try:
        data = []
        userObj = userCheckerForLogin(response, reqObj.get("username"))
        if userObj:
            currentDatetime = datetime.now()
            resetObj = resetPassword.find_one({"userId": userObj.get("_id"), "resetOn": None})
            emailConf = False
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
                    emailConf = sendEmail(userObj.get("email"), resetObj.get("resetKey"), environ)
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
                    emailConf = sendEmail(userObj.get("email"), resetKey, environ)
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

                emailConf = sendEmail(userObj.get("email"), resetKey, environ)

            data = {
                "email": userObj.get("email"),
                "displayName": userObj.get("displayName"),
            }
            if emailConf:
                response.setStatus(200)
                response.setMessage("Password reset link has been sent to your email")
            else:
                response.setStatus(502)
                response.setMessage("We could not able to sent mail right now please try again after 24 hours")
        else:
            response.setStatus(404)
            response.setMessage("User does not found")

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

def sendEmail(email, resetKey, environ):
    try:
        website = "https://{0}{1}/auth/resetPassword/".format(environ.get("REMOTE_ADDR"), api.prefix)
        msg = Message()
        msg.sender = SETTING.MAIL_USERNAME
        msg.add_recipient(email)
        msg.subject = "Password Reset"
        msg.body = "Reset your password with this link\n{0}{1}".format(website, resetKey)
        mail.send(msg)
        return True
    except:
        return False