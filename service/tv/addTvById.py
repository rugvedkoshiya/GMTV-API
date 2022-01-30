from models.conn import tvCollections, userDataCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from service.checkers.tvChecker import getEpisode, getLanguage, getSeason, getTvObj
from models.config import Config as SETTING
from datetime import datetime


def addTvById(apiKey, tvId, reqObj):
    response = JsonResponse()

    try:
        data = []
        checkBool = False

        userObj = apiChecker(apiKey, response)
        if userObj:
            tvObj = getTvObj(response, tvId)
        if tvObj:
            checkBool, season = getSeason(response, reqObj.get("season"), tvObj.get("number_of_seasons"), False)
        if checkBool:
            checkBool, episode = getEpisode(response, reqObj.get("episode"), season, tvObj.get("seasons"), None, False)
        if checkBool:
            checkBool, language = getLanguage(response, reqObj.get("language"), tvObj.get("languages"))
        if checkBool:
            userDataTvObj = userDataCollections.find_one({"userId" : userObj.get("_id"), "tvId" : tvObj.get("_id")})
            if not userDataTvObj:
                currentDatetime = datetime.now()
                newObj = {
                    "userId": userObj.get("_id"),
                    "tvId": tvObj.get("_id"),
                    "watchedLanguage" : language,
                    "currentSeason" : season,
                    "currentEpisode" : episode,
                    "createdAt": currentDatetime,
                    "modifiedAt": currentDatetime,
                }
                userDataCollections.insert_one(newObj)
                data = newObj
                del data["_id"]
                del data["userId"]
                del data["tvId"]

                response.setStatus(200)
                response.setMessage("Added into watched list")
            else:
                response.setStatus(409)
                response.setMessage("Already added into watched list")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in adding tv show by id Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()