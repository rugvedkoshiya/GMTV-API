import re
from models.conn import tvCollections


def getTvObj(response, tvId):
    if tvId != None:
        tvObj = tvCollections.find_one({"id" : tvId})
        if tvObj != None:
            return tvObj
        else:
            response.setStatus(404)
            response.setError("No TV Show found with provided ID")
            return None
    else:
        response.setStatus(400)
        response.setError("Invalid TV ID")
        return None


def getLanguage(response, language, languageArray):
    if language:
        if language in languageArray:
            return language
        else:
            response.setStatus(400)
            response.setError("This show is not in this language which you have provided")
            return None
    else:
        return None


def getSeason(response, season, seasons):
    if season:
        try:
            if 0 < int(season) <= seasons:
                return int(season)
            else:
                response.setStatus(400)
                response.setError("This show does not have that much seasons")
                return None    
        except:
            response.setStatus(400)
            response.setError("Provided season number is invalid")
            return None
    else:
        response.setStatus(400)
        response.setError("You have not provided season number")
        return None


def getEpisode(response, episode, seasonNo, seasons):
    if episode:
        try:
            for season in seasons:
                if season.get("season_number") == seasonNo:
                    if 0 < int(episode) <= season.get("episode_count"):
                        return int(episode)

            response.setStatus(400)
            response.setError("This show does not have that much episodes")
            return None    
        except:
            response.setStatus(400)
            response.setError("Provided episode number is invalid")
            return None
    else:
        response.setStatus(400)
        response.setError("You have not provided episode number")
        return None