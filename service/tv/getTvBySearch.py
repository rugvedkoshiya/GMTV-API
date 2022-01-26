import imp
from models.conn import tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import pageChecker, queryChecker
from models.config import Config as SETTING
import re


def getTvBySearch(requestObj):
    response = JsonResponse()
    pageSize = 20

    try:
        pageBool = False
        data = []

        queryBool, query = queryChecker(response, requestObj.get("query"))
        if queryBool:
            pageBool, page = pageChecker(response, requestObj.get("page"))
        if pageBool:
            data = tvCollections.find({"name" : re.compile(query, re.IGNORECASE)}, {"_id" : False}).skip(0 if page == 1 else page*SETTING.PAGING - SETTING.PAGING).limit(SETTING.PAGING)
            data = list(data)
            response.setStatus(200)
            response.setMessage("tv data fetched")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching a popular tv shows => " + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()