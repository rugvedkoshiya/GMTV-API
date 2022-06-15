from service.getter import getApiKey
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
getMovieBySearchModel.add_argument("query", type=str, required=True, help="Query parameter for movie", location="args")
getMovieBySearchModel.add_argument("page", type=int, required=False, help="For pagination", location="args")

addMovieModel = reqparse.RequestParser()
addMovieModel.add_argument("language", type=str, required=True, help="language in which user has seen the movie", location="json")

editMovieModel = reqparse.RequestParser()
editMovieModel.add_argument("language", type=str, required=True, help="language in which user has seen the movie", location="json")

getMovieWatchedModel = reqparse.RequestParser()
getMovieWatchedModel.add_argument("page", type=int, required=False, help="For pagination", location="args")

@movie.route("/popular")
class MoviePopular(Resource):
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
        apiKey = getApiKey(request)
        output = addMovieById(apiKey, movieId, requestObj)
        return jsonify(output)

    @api.doc(responses={200: "OK"})
    @api.expect(editMovieModel)
    def put(self, movieId):
        requestObj = validateParameters(request.json, ["language"])
        apiKey = getApiKey(request)
        output = editMovieById(apiKey, movieId, requestObj)
        return jsonify(output)

    @api.doc(responses={200: "OK"})
    @api.expect()
    def delete(self, movieId):
        apiKey = getApiKey(request)
        output = deleteMovieById(apiKey, movieId)
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
class MovieWatched(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(getMovieWatchedModel)
    def get(self):
        requestObj = validateParameters(request.args, ["page"])
        output = getMovieWatchedList(requestObj)
        return jsonify(output)
