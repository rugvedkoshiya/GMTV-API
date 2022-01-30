from models.conn import userDataCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING
from service.checkers.movieChecker import getMovieObj


def deleteMovieById(apiKey, movieId):
    response = JsonResponse()

    try:
        data = []

        userObj = apiChecker(apiKey, response)
        if userObj:
            movieObj = getMovieObj(response, movieId)
        if movieObj:
            result = userDataCollections.delete_one(
                {
                    "userId" : userObj.get("_id"),
                    "movieId" : movieObj.get("_id"),
                }
            )
            if result.deleted_count:
                response.setStatus(200)
                response.setMessage("Deleted from watched list")
            else:
                response.setStatus(404)
                response.setMessage("We did not find this movie in watched list")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in deleting movie from watched list Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()