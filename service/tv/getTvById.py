from models.conn import tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING


def getTvById(tvId):
    response = JsonResponse()

    try:
        data = tvCollections.find_one({"id" : tvId}, {'_id': False})

        if data != None:
            response.setStatus(200)
            response.setMessage("tv data fetched")
        else:
            response.setStatus(404)
            response.setError("Tv show does not exists with this tv id")
            data = []
        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching tv by id => Contact Mr. Grey" + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()