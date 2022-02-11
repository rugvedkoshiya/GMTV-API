import json
from service.JsonResponse import JsonResponse
from service.checkers.movieChecker import getMovieObj
from service.redis.redis import getCachedata, setCacheData
from service.redis.redisTimeToLive import redisExpire


def getMovieById(movieId):
    response = JsonResponse()

    try:
        data = []
        redisData = getCachedata("movie:{0}".format(movieId))
        if redisData:
            data = json.loads(redisData.decode("utf-8"))
        else:
            movieObj = getMovieObj(response, movieId)
            if movieObj:
                data = movieObj
                del data['_id']
                response.setStatus(200)
                response.setMessage("Movie data fetched")
                setCacheData("movie:{0}".format(movieId), json.dumps(data), redisExpire.Day)

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching movie by id Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()