from models.conn import tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING


def editTvById(tvId, requestObj):
    response = JsonResponse()

    try:
        data = []

        response.setStatus(200)
        response.setMessage("demo api")
        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in editing tv show by id => Contact Mr. Grey" + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()