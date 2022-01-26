from service.tv.addTvById import addTvById
from service.tv.deleteTvById import deleteTvById
from service.tv.editTvById import editTvById
from service.tv.getTvById import getTvById
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
        requestObj = validateParameters(request.args, ["page"])
        output = getTvPopular(requestObj)
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
        requestObj = validateParameters(request.json, ["language", "season", "episode"])
        output = addTvById(tvId, requestObj)
        return jsonify(output)

    @api.doc(responses={200: "OK"})
    @api.expect(editTvModel)
    def put(self, tvId):
        requestObj = validateParameters(request.json, ["language", "season", "episode"])
        output = editTvById(tvId, requestObj)
        return jsonify(output)

    @api.doc(responses={200: "OK"})
    @api.expect()
    def delete(self, tvId):
        output = deleteTvById(tvId)
        return jsonify(output)

@tv.route("/search")
class TvBySearch(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(getTvBySearchModel)
    def get(self):
        requestObj = validateParameters(request.args, ["query", "page"])
        output = getTvBySearch(requestObj)
        return jsonify(output)

@tv.route("/watched")
class TvBySearch(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(getTvWatchedModel)
    def get(self):
        requestObj = validateParameters(request.args, ["page"])
        output = getTvWatchedList(requestObj)
        return jsonify(output)
