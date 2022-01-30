from datetime import datetime
from models.conn import tvCollections, userDataCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from service.checkers.tvChecker import getEpisode, getLanguage, getSeason, getTvObj, getUserDataObj
from models.config import Config as SETTING


def editTvById(apiKey, tvId, reqObj):
    response = JsonResponse()
    try:
        data = []
        checkBool = False

        userObj = apiChecker(apiKey, response)
        if userObj:
            tvObj = getTvObj(response, tvId)
        if tvObj:
            userDataObj = getUserDataObj(response, tvObj.get("_id"), userObj.get("_id"))
        if userDataObj:
            checkBool, season = getSeason(response, reqObj.get("season"), tvObj.get("number_of_seasons"), True)
        if checkBool:
            checkBool, episode = getEpisode(response, reqObj.get("episode"), season, tvObj.get("seasons"), userDataObj, True)
        if checkBool:
            checkBool, language = getLanguage(response, reqObj.get("language"), tvObj.get("languages"))
        if checkBool:
            editedObj = {}
            isEdited = False
            currentDatetime = datetime.now()
            if season:
                editedObj["currentSeason"] = season
                isEdited = True
            if episode:
                editedObj["currentEpisode"] = episode
                isEdited = True
            if language:
                editedObj["watchedLanguage"] = language
                isEdited = True
            if isEdited:
                editedObj["modifiedAt"] = currentDatetime

            userDataCollections.update_one(
                {
                    "userId" : userObj.get("_id"),
                    "tvId" : tvObj.get("_id")
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
            del data["tvId"]

            response.setStatus(200)
            response.setMessage("Edited watched list")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in editing tv show watched list Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()