from models.conn import movieCollections, userDataCollections


def getMovieObj(response, movieId):
    if movieId != None:
        movieObj = movieCollections.find_one({"id" : movieId})
        if movieObj != None:
            return movieObj
        else:
            response.setStatus(404)
            response.setError("No Movie found with provided ID")
            return None
    else:
        response.setStatus(400)
        response.setError("Invalid Movie ID")
        return None


def getLanguage(response, language, languageArray):
    if language:
        if language in languageArray:
            return language
        else:
            response.setStatus(400)
            response.setError("This movie is not in this language which you have provided")
            return None
    else:
        response.setStatus(400)
        response.setError("No language provided")
        return None


def getUserDataObj(response, tvId, userId):
    userDataObj = userDataCollections.find_one({"userId": userId, "movieId": tvId})
    if userDataObj != None:
        return userDataObj
    else:
        response.setStatus(404)
        response.setError("No movie found with provided ID")
        return None