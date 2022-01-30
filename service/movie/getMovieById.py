from models.conn import tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING
from service.checkers.movieChecker import getMovieObj


def getMovieById(movieId):
    response = JsonResponse()

    try:
        data = []
        movieObj = getMovieObj(response, movieId)
        if movieObj:
            data = movieObj
            del data['_id']
            response.setStatus(200)
            response.setMessage("Movie data fetched")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching a popular tv shows => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()