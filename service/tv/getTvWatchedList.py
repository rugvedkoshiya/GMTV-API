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
                    { "$project": {"_id": 0, "userId": 0, "tvId": 0}},
                ]
            )
            print(list(watchedTvObj))
            # data = list(watchedTvObj)
            # for row in data:
            #     del data["_id"]
            #     del data["userId"]
            #     del data["tvId"]
            # data = list(watchedTvObj)

        response.setStatus(200)
        response.setMessage("demo api")
        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching watched tv shows Contact Mr. Grey => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()