from models.conn import movieCollections
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING


def getMoviePopular(reqObj):
    response = JsonResponse()

    try:
        data = []

        pageBool, page = pageChecker(response, reqObj.get("page"))
        if pageBool:
            movieCollData = movieCollections.find({}, {'_id': False}).sort([('popularity', -1)]).skip(page*SETTING.PAGING - SETTING.PAGING).limit(SETTING.PAGING)
    
            # Convert Data into List
            for movie in movieCollData:
                data.append(movie)

            response.setStatus(200)
            response.setMessage("movie data fetched")
        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching a popular tv shows => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()