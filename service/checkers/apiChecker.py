import re
from models.conn import userCollections

def apiChecker(apiKey, response):
    if apiKey != None:
        userObj = userCollections.find_one({"api" : apiKey})
        if userObj != None:
            return userObj
        else:
            response.setStatus(401)
            response.setError("Invalid API key")
            return None
    else:
        response.setStatus(401)
        response.setError("API key not provided")
        return None