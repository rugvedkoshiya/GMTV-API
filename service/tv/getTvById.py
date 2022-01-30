from models.conn import tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING
from service.checkers.tvChecker import getTvObj


def getTvById(tvId):
    response = JsonResponse()

    try:
        data = []
        # userObj = apiChecker(apiKey, response)
        # if userObj:
        tvObj = getTvObj(response, tvId)
        if tvObj:
            data = tvObj
            del data['_id']
            response.setStatus(200)
            response.setMessage("TV data fetched")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching tv by id Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()