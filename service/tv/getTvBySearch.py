import collections
import imp
from models.conn import tvCollections
from service.JsonResponse import JsonResponse
from service.checkers.commonChecker import pageChecker, queryChecker
from models.config import Config as SETTING
import re


def getTvBySearch(reqObj):
    response = JsonResponse()
    pageSize = 20

    try:
        data = []
        pageBool = False

        queryBool, query = queryChecker(response, reqObj.get("query"))
        if queryBool:
            pageBool, page = pageChecker(response, reqObj.get("page"))
        if pageBool:
            collectionObjs = tvCollections.find({"name" : re.compile(query, re.IGNORECASE)}, {"_id" : False}).skip(0 if page == 1 else page*SETTING.PAGING - SETTING.PAGING).limit(SETTING.PAGING)
            data = list(collectionObjs)
            response.setStatus(200)
            response.setMessage("TV data fetched")

        response.setData(data)
    except Exception as e:
        response.setStatus(500) # Internal error
        response.setError("Error in fetching popular tv shows by search => Contact Mr. Grey" + str(e))
        # logConfig.logError("Error in fetching a content  => " + str(e))
    finally:
        return response.returnResponse()