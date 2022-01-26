from models.conn import tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING


def getTvPopular(requestObj):
    response = JsonResponse()
    pageSize = 20

    try:
        data = []

        pageBool, page = pageChecker(response, requestObj.get("page"))
        if pageBool:
            tvCollData = tvCollections.find({}, {'_id': False}).sort([('popularity', -1)]).skip(0 if page == 1 else page*SETTING.PAGING - SETTING.PAGING).limit(SETTING.PAGING)
    
            # Convert Data into List
            data["tv"] = []
            for tvShow in tvCollData:
                data["tv"].append(tvShow)

        response.setStatus(200)
        response.setMessage("tv data fetched")
        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching a popular tv shows => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()