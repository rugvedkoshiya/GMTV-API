from datetime import datetime
from models.conn import tvCollections, userDataCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING
from service.checkers.movieChecker import getLanguage, getMovieObj


def addMovieById(apiKey, movieId, reqObj):
    response = JsonResponse()

    try:
        data = []
        checkBool = False

        userObj = apiChecker(apiKey, response)
        if userObj:
            movieObj = getMovieObj(response, movieId)
        if movieObj:
            checkBool, language = getLanguage(response, reqObj.get("language"), movieObj.get("languages"))
        if checkBool:
            userDataTvObj = userDataCollections.find_one({"userId" : userObj.get("_id"), "movieId" : movieObj.get("_id")})
            if not userDataTvObj:
                currentDatetime = datetime.now()
                newObj = {
                    "userId": userObj.get("_id"),
                    "movieId": movieObj.get("_id"),
                    "watchedLanguage" : language,
                    "createdAt": currentDatetime,
                    "modifiedAt": currentDatetime,
                }
                userDataCollections.insert_one(newObj)
                data = newObj
                del data["_id"]
                del data["userId"]
                del data["movieId"]

                response.setStatus(200)
                response.setMessage("Added into watched list")
            else:
                response.setStatus(409)
                response.setMessage("Already added into watched list")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching a popular tv shows => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()