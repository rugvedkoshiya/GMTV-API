import re
from models.conn import tvCollections, userDataCollections


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


def getUserDataObj(response, tvId, userId):
    userDataObj = userDataCollections.find_one({"userId": userId, "tvId": tvId})
    if userDataObj != None:
        return userDataObj
    else:
        response.setStatus(404)
        response.setError("No TV Show found with provided ID")
        return None

def getLanguage(response, language, languageArray):
    if language:
        if language in languageArray:
            return True, language
        else:
            response.setStatus(400)
            response.setError("This show is not in this language which you have provided")
            return False, None
    else:
        return True, None


def getSeason(response, season, seasons, isEditing):
    if season:
        try:
            if 0 < int(season) <= seasons:
                return True, int(season)
            else:
                response.setStatus(400)
                response.setError("This show does not have that much seasons")
                return False, None    
        except:
            response.setStatus(400)
            response.setError("Provided season number is invalid")
            return False, None
    else:
        if isEditing:
            return True, None
        response.setStatus(400)
        response.setError("You have not provided season number")
        return False, None


def checkEpisode(response, seasons, seasonNo, episode):
    print(episode)
    for season in seasons:
        if season.get("season_number") == seasonNo:
            if 0 < int(episode) <= season.get("episode_count"):
                return True, int(episode)

    response.setStatus(400)
    response.setError("This show does not have that much episodes")
    return False, None


def getEpisode(response, episode, seasonNo, seasons, userDataObj, isEditing):
    # loophole: take episode = 0 and test it
    if episode:
        try:
            if isEditing:
                if seasonNo:
                    return checkEpisode(response, seasons, seasonNo, episode)
                else:
                    return checkEpisode(response, seasons, userDataObj.get("currentSeason"), episode)
            else:
                return checkEpisode(response, seasons, seasonNo, episode)
        except:
            response.setStatus(400)
            response.setError("Provided episode number is invalid")
            return False, None
    else:
        if isEditing:
            if seasonNo:
                response.setStatus(400)
                response.setError("You cannot change season without episode")
                return False, None
            else:
                return True, None
        response.setStatus(400)
        response.setError("You have not provided episode number")
        return False, None