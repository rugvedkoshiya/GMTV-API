from service.getter import getApiKey
from service.tv.getTvById import getTvById
from service.tv.addTvById import addTvById
from service.tv.editTvById import editTvById
from service.tv.deleteTvById import deleteTvById
from service.tv.getTvBySearch import getTvBySearch
from service.tv.getTvPopular import getTvPopular
from service.tv.getTvWatchedList import getTvWatchedList
from swaggerConfig import api
from flask_restx import reqparse, Resource
from flask import jsonify, request
from service.validators.validationFunctions import validateParameters 

tv = api.namespace("tv", description="TV Apis")

getTvPopularModel = reqparse.RequestParser()
getTvPopularModel.add_argument("page", type=int, required=False, help="For pagination", location="args")

getTvBySearchModel = reqparse.RequestParser()
getTvBySearchModel.add_argument("query", type=str, required=True, help="Query parameter for tv show", location="args")
getTvBySearchModel.add_argument("page", type=int, required=False, help="For pagination", location="args")

addTvModel = reqparse.RequestParser()
addTvModel.add_argument("language", type=str, required=True, help="language in which user has seen tv show", location="json")
addTvModel.add_argument("season", type=int, required=True, help="season number where user is on", location="json")
addTvModel.add_argument("episode", type=int, required=True, help="episode number of searson where user is on", location="json")

editTvModel = reqparse.RequestParser()
editTvModel.add_argument("language", type=str, required=True, help="language in which user has seen tv show", location="json")
editTvModel.add_argument("season", type=int, required=True, help="season number where user is on", location="json")
editTvModel.add_argument("episode", type=int, required=True, help="episode number of searson where user is on", location="json")

getTvWatchedModel = reqparse.RequestParser()
getTvWatchedModel.add_argument("page", type=int, required=False, help="For pagination", location="args")


@tv.route("/popular")
class TvPopular(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(getTvPopularModel)
    def get(self):
        reqObj = validateParameters(request.args, ["page"])
        output = getTvPopular(reqObj)
        return jsonify(output)


@tv.route("/<int:tvId>")
class TvById(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect()
    def get(self, tvId):
        output = getTvById(tvId)
        return jsonify(output)


    @api.doc(responses={200: "OK"})
    @api.expect(addTvModel)
    def post(self, tvId):
        reqObj = validateParameters(request.json, ["language", "season", "episode"])
        apiKey = getApiKey(request)
        output = addTvById(apiKey, tvId, reqObj)
        return jsonify(output)


    @api.doc(responses={200: "OK"})
    @api.expect(editTvModel)
    def put(self, tvId):
        reqObj = validateParameters(request.json, ["language", "season", "episode"])
        apiKey = getApiKey(request)
        output = editTvById(apiKey, tvId, reqObj)
        return jsonify(output)


    @api.doc(responses={200: "OK"})
    @api.expect()
    def delete(self, tvId):
        apiKey = getApiKey(request)
        output = deleteTvById(apiKey, tvId)
        return jsonify(output)


@tv.route("/search")
class TvBySearch(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(getTvBySearchModel)
    def get(self):
        reqObj = validateParameters(request.args, ["query", "page"])
        output = getTvBySearch(reqObj)
        return jsonify(output)


@tv.route("/watched")
class TvWatched(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(getTvWatchedModel)
    def get(self):
        reqObj = validateParameters(request.args, ["page"])
        apiKey = getApiKey(request)
        output = getTvWatchedList(apiKey, reqObj)
        return jsonify(output)
