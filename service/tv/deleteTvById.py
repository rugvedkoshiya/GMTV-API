from models.conn import userDataCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING
from service.checkers.tvChecker import getTvObj, getUserDataObj


def deleteTvById(apiKey, tvId):
    response = JsonResponse()
    try:
        data = []

        userObj = apiChecker(apiKey, response)
        if userObj:
            tvObj = getTvObj(response, tvId)
        if tvObj:
            result = userDataCollections.delete_one(
                {
                    "userId" : userObj.get("_id"),
                    "tvId" : tvObj.get("_id"),
                }
            )
            if result.deleted_count:
                response.setStatus(200)
                response.setMessage("Deleted from watched list")
            else:
                response.setStatus(404)
                response.setMessage("We did not find this tv show in watched list")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in removing tv show by id Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()