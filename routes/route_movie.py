from service.movie.addMovieById import addMovieById
from service.movie.deleteMovieById import deleteMovieById
from service.movie.editMovieById import editMovieById
from service.movie.getMovieById import getMovieById
from service.movie.getMovieBySearch import getMovieBySearch
from service.movie.getMoviePopular import getMoviePopular
from service.movie.getMovieWatchedList import getMovieWatchedList
from swaggerConfig import api
from flask_restx import reqparse, Resource
from flask import jsonify, request
from service.validators.validationFunctions import validateParameters 

movie = api.namespace("movie", description="Movie Apis")

getMoviePopularModel = reqparse.RequestParser()
getMoviePopularModel.add_argument("page", type=int, required=False, help="For pagination", location="args")

getMovieBySearchModel = reqparse.RequestParser()
getMovieBySearchModel.add_argument("query", type=str, required=True, help="Query parameter for tv show", location="args")
getMovieBySearchModel.add_argument("page", type=int, required=False, help="For pagination", location="args")

addMovieModel = reqparse.RequestParser()
addMovieModel.add_argument("language", type=str, required=True, help="language in which user has seen tv show", location="json")
addMovieModel.add_argument("season", type=int, required=True, help="season number where user is on", location="json")
addMovieModel.add_argument("episode", type=int, required=True, help="episode number of searson where user is on", location="json")

editMovieModel = reqparse.RequestParser()
editMovieModel.add_argument("language", type=str, required=True, help="language in which user has seen tv show", location="json")
editMovieModel.add_argument("season", type=int, required=True, help="season number where user is on", location="json")
editMovieModel.add_argument("episode", type=int, required=True, help="episode number of searson where user is on", location="json")

getMovieWatchedModel = reqparse.RequestParser()
getMovieWatchedModel.add_argument("page", type=int, required=False, help="For pagination", location="args")

@movie.route("/popular")
class TvPopular(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(getMoviePopularModel)
    def get(self):
        requestObj = validateParameters(request.args, ["page"])
        output = getMoviePopular(requestObj)
        return jsonify(output)

@movie.route("/<int:movieId>")
class MovieById(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect()
    def get(self, movieId):
        output = getMovieById(movieId)
        return jsonify(output)

    @api.doc(responses={200: "OK"})
    @api.expect(addMovieModel)
    def post(self, movieId):
        requestObj = validateParameters(request.json, ["language"])
        output = addMovieById(movieId, requestObj)
        return jsonify(output)

    @api.doc(responses={200: "OK"})
    @api.expect(editMovieModel)
    def put(self, movieId):
        requestObj = validateParameters(request.json, ["language"])
        output = editMovieById(movieId, requestObj)
        return jsonify(output)

    @api.doc(responses={200: "OK"})
    @api.expect()
    def delete(self, movieId):
        output = deleteMovieById(movieId)
        return jsonify(output)

@movie.route("/search")
class MovieBySearch(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(getMovieBySearchModel)
    def get(self):
        requestObj = validateParameters(request.args, ["query", "page"])
        output = getMovieBySearch(requestObj)
        return jsonify(output)

@movie.route("/watched")
class MovieBySearch(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(getMovieWatchedModel)
    def get(self):
        requestObj = validateParameters(request.args, ["page"])
        output = getMovieWatchedList(requestObj)
        return jsonify(output)
