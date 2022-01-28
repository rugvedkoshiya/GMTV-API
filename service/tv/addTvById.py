from models.conn import tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from service.checkers.tvChecker import getEpisode, getLanguage, getSeason, getTvObj
from models.config import Config as SETTING


def addTvById(apiKey, tvId, reqObj):
# language bool
    response = JsonResponse()
    try:
        data = []
        tvObj = None
        language = None
        season = None
        episode = None

        userObj = apiChecker(apiKey, response)
        if userObj:
            tvObj = getTvObj(response, tvId)
            print(tvObj)
        if tvObj:
            season = getSeason(response, reqObj.get("season"), tvObj.get("number_of_seasons"))
        if season:
            episode = getEpisode(response, reqObj.get("episode"), season, tvObj.get("seasons"))
        if episode:
            language = getLanguage(response, reqObj.get("language"), tvObj.get("languages"))
        print(language, season, episode)
        

        # response.setStatus(200)
        # response.setMessage("demo api")
        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in adding tv show by id => Contact Mr. Grey" + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()