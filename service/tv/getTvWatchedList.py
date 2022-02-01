from models.conn import userDataCollections, tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.apiChecker import apiChecker
from service.checkers.commonChecker import pageChecker
from models.config import Config as SETTING


def getTvWatchedList(apiKey, reqObj):
    response = JsonResponse()

    try:
        data = []

        userObj = apiChecker(apiKey, response)
        if userObj:
            pageBool, page = pageChecker(response, reqObj.get("page"))
        if pageBool:
            watchedTvObj = userDataCollections.aggregate(
                [
                    {
                        "$lookup" : {
                            "from": "TV",
                            "localField": "tvId",
                            "foreignField": "_id",
                            "as": "tv"
                        },
                    },
                    {
                        "$unwind": '$tv'
                    },
                    {
                        "$sort": {
                            "createdAt": -1 
                        }
                    },
                    {
                        "$skip": page*SETTING.PAGING - SETTING.PAGING
                    },
                    {
                        "$limit": SETTING.PAGING
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "userId": 0,
                            "tvId": 0,
                            "tv._id": 0
                        }
                    },
                ]
            )
            data = list(watchedTvObj)

            response.setStatus(200)
            response.setMessage("fetched whatced list")
        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching watched tv shows Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()