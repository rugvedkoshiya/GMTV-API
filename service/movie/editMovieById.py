from datetime import datetime
from models.conn import userDataCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING
from service.checkers.movieChecker import getLanguage, getMovieObj, getUserDataObj


def editMovieById(apiKey, movieId, reqObj):
    response = JsonResponse()

    try:
        data = []
        checkBool = False

        userObj = apiChecker(apiKey, response)
        if userObj:
            movieObj = getMovieObj(response, movieId)
        if movieObj:
            userDataObj = getUserDataObj(response, movieObj.get("_id"), userObj.get("_id"))
        if userDataObj:
            language = getLanguage(response, reqObj.get("language"), movieObj.get("languages"))
        if language:
            editedObj = {}
            currentDatetime = datetime.now()
            editedObj["watchedLanguage"] = language
            editedObj["modifiedAt"] = currentDatetime

            userDataCollections.update_one(
                {
                    "userId" : userObj.get("_id"),
                    "movieId" : movieObj.get("_id")
                },
                {
                    "$set": editedObj
                }
            )
            data = {
                **userDataObj,
                **editedObj
            }
            del data["_id"]
            del data["userId"]
            del data["movieId"]

            response.setStatus(200)
            response.setMessage("Edited watched list")
        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in editing watched list Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()