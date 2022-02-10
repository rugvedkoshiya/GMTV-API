import json
from models.conn import tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING
# from service.redis.redis import getCachedata, setCacheData
# from service.redis.redisTimeToLive import redisExpire


def getTvPopular(reqObj):
    response = JsonResponse()

    try:
        data = []

        pageBool, page = pageChecker(response, reqObj.get("page"))
        if pageBool:
            # redisData = getCachedata("tvPopular:{0}".format(page))
            # if redisData:
                # data = json.loads(redisData.decode("utf-8"))
            # else:
            tvCollData = tvCollections.find({}, {'_id': False}).sort([('popularity', -1)]).skip(page*SETTING.PAGING - SETTING.PAGING).limit(SETTING.PAGING)
    
            # Convert Data into List
            for tvShow in tvCollData:
                data.append(tvShow)

            response.setStatus(200)
            response.setMessage("tv data fetched")
            # setCacheData("tvPopular:{0}".format(page), json.dumps(data), redisExpire.Hour)

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching a popular tv shows Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()