import json
from service.JsonResponse import JsonResponse
from service.checkers.tvChecker import getTvObj
# from service.redis.redis import getCachedata, setCacheData
# from service.redis.redisTimeToLive import redisExpire


def getTvById(tvId):
    response = JsonResponse()

    try:
        data = []
        # redisData = getCachedata("tv:{0}".format(tvId))
        # if redisData:
            # data = json.loads(redisData.decode("utf-8"))
        # else:
        tvObj = getTvObj(response, tvId)
        if tvObj:
            data = tvObj
            del data['_id']
            response.setStatus(200)
            response.setMessage("TV data fetched")
            # setCacheData("tv:{0}".format(tvId), json.dumps(data), redisExpire.Day)

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching tv by id Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()