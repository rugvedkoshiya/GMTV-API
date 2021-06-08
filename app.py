from flask import Flask, jsonify, request, Response, redirect
from flask_pymongo import pymongo
import requests
import secrets
import json
import re
import os
from iso_language_codes import language, language_name, language_autonym
from config import TestingConfig as APP_SETTINGS
from config import ErrorStringManagement
from config import SuccessStringManagement
from exception_handler import *

app = Flask(__name__)
app.secret_key = APP_SETTINGS.SECRET_KEY

# Get Data from Database
client = pymongo.MongoClient(APP_SETTINGS.MONGO_LINK)
db = client[APP_SETTINGS.DATABASE_NAME]
tv_collections = db[APP_SETTINGS.TV_COLLECTION_NAME]
movie_collections = db[APP_SETTINGS.MOVIE_COLLECTION_NAME]
users_collections = db[APP_SETTINGS.USER_COLLECTION_NAME]
users_data_collections = db[APP_SETTINGS.USER_DATA_COLLECTION_NAME]





# TV Show Routes
@app.route(f'/{APP_SETTINGS.VERSION}/tv/<int:tv_id>', methods=['GET'])
def tv_tv_id_func(tv_id):
    try:
        if "api" in request.args:
            api_key = request.args.get('api')
            api_check = users_collections.count_documents({"API" : api_key})

            if api_check != 0:
                tv_coll_data = tv_collections.find({"id" : tv_id}, {'_id': False})[0]
                return Response(json.dumps(tv_coll_data), status=200, mimetype='application/json')
            else:
                raise INVALID_API_401_EXCEPTION
        else:
            raise INVALID_API_401_EXCEPTION
    except INVALID_API_401_EXCEPTION:
        response =  Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except IndexError:
        response = Response(json.dumps(ErrorStringManagement.NOT_FOUND_404), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(f'/{APP_SETTINGS.VERSION}/tv/search', methods=['GET'])
def tv_search_func():
    try:
        if "api" in request.args:
            if "query" in request.args:
                api_key = request.args.get('api')
                api_check = users_collections.count_documents({"API" : api_key})
                
                if api_check != 0:
                    tv_name = request.args.get('query')
                    if "page" in request.args:
                        page = int(request.args.get('page'))
                        if page > 0:
                            tv_coll_data = tv_collections.find({"name" : re.compile(tv_name, re.IGNORECASE)}, {"_id" : False}).skip(0 if page == 1 else page*APP_SETTINGS.PAGING - APP_SETTINGS.PAGING).limit(APP_SETTINGS.PAGING)
                        else:
                            raise ValueError
                    else:
                        tv_coll_data = tv_collections.find({"name" : re.compile(tv_name, re.IGNORECASE)}, {"_id" : False}).skip(0).limit(APP_SETTINGS.PAGING)

                    # Convert Data into List
                    tv_coll_fetch_data = []
                    for data in tv_coll_data:
                        tv_coll_fetch_data.append(data)
                    response = Response(json.dumps(tv_coll_fetch_data), status=200, mimetype='application/json')
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
                else:
                    raise INVALID_API_401_EXCEPTION
            else:
                raise BAD_REQUEST_400_EXCEPTION
        else:
            raise INVALID_API_401_EXCEPTION
    except INVALID_API_401_EXCEPTION:
        response = Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except BAD_REQUEST_400_EXCEPTION as e:
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except ValueError:
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(f'/{APP_SETTINGS.VERSION}/tv/add/<int:tv_id>', methods=['GET'])
def tv_add_func(tv_id):
    try:
        if "api" in request.args:
            if "language" in request.args and "season" in request.args and "episode" in request.args:
                # check that language is valid
                l_name = language_name(request.args.get('language'))
                api_key = request.args.get('api')
                watched_language = request.args.get('language')
                current_season = int(request.args.get('season'))
                current_episode = int(request.args.get('episode'))
                api_check = users_collections.count_documents({"API" : api_key})

                if api_check != 0:
                    tv_show_available = tv_collections.count_documents({"id" : tv_id})
                    if tv_show_available == 1:
                        # check that language is available
                        language_available = tv_collections.find({"id" : tv_id}, {"_id" : False, "languages" : True})[0]["languages"]
                        if watched_language in language_available:
                            # check that season is available
                            season_available = tv_collections.find({"id" : tv_id}, {"_id" : False, "seasons" : True})[0]["seasons"]
                            if current_season <= len(season_available) and current_season > 0:
                                # check that episode is available
                                total_episode = tv_collections.find({"id" : tv_id}, {"_id" : False, "seasons" : {"$elemMatch" : {"season_number" : current_season}}})[0]["seasons"][0]["episode_count"]
                                if current_episode <= total_episode and current_episode > 0:
                                    user_id = users_collections.find({"API" : api_key}, {"_id" : True})[0]['_id']
                                    tv_already_watching = users_data_collections.count_documents({"user_id" : user_id, "tv" : {"$elemMatch" : {"tv_id" : tv_id}}})
                                    if tv_already_watching == 0:
                                        # add new
                                        print("Adding...")
                                        users_data_collections.update_one({"user_id" : user_id}, {"$push" : {"tv" : { "$each" : [{"tv_id" : tv_id, "watched_language" : watched_language, "current_season" : current_season, "current_episode" : current_episode}]}}})
                                        print("New added")
                                        response = Response(json.dumps(SuccessStringManagement.ADDED_TO_WATCHED_LIST), status=200, mimetype='application/json')
                                        response.headers['Access-Control-Allow-Origin'] = '*'
                                        return response
                                    else:
                                        # edit
                                        print("Editing...")
                                        users_data_collections.update_one({"user_id" : user_id, "tv.tv_id" : tv_id}, {"$set" : {"tv.$.watched_language" : watched_language, "tv.$.current_season" : current_season, "tv.$.current_episode" : current_episode}})
                                        print("Edit Done")
                                        response = Response(json.dumps(SuccessStringManagement.EDITED_TO_WATCHED_LIST), status=200, mimetype='application/json')
                                        response.headers['Access-Control-Allow-Origin'] = '*'
                                        return response
                                else:
                                    raise NOT_FOUND_404_EXCEPTION(ErrorStringManagement.NOT_FOUND_EPISODE_404)
                            else:
                                raise NOT_FOUND_404_EXCEPTION(ErrorStringManagement.NOT_FOUND_SEASON_404)
                        else:
                            raise NOT_FOUND_404_EXCEPTION(ErrorStringManagement.NOT_FOUND_LANGUAGE_404)
                    else:
                        raise NOT_FOUND_404_EXCEPTION
                else:
                    raise INVALID_API_401_EXCEPTION
            else:
                raise BAD_REQUEST_400_EXCEPTION(ErrorStringManagement.BAD_REQUEST_INCORRECT)
        else:
            raise INVALID_API_401_EXCEPTION
    except NOT_FOUND_404_EXCEPTION as e:
        ErrorStringManagement.NOT_FOUND_404['status_message'] = str(e)
        response = Response(json.dumps(ErrorStringManagement.NOT_FOUND_404), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except BAD_REQUEST_400_EXCEPTION as e:
        ErrorStringManagement.BAD_REQUEST_400['status_message'] = str(e)
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except INVALID_API_401_EXCEPTION:
        response = Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except (AssertionError, KeyError):
        ErrorStringManagement.BAD_REQUEST_400['status_message'] = ErrorStringManagement.BAD_REQUEST_LANGUAGE_INVALID_400
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except ValueError:
        ErrorStringManagement.BAD_REQUEST_400['status_message'] = ErrorStringManagement.BAD_REQUEST_INCORRECT
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(f'/{APP_SETTINGS.VERSION}/tv/remove/<int:tv_id>', methods=['GET'])
def tv_removewatched(tv_id):
    try:
        if "api" in request.args:
            api_key = request.args.get('api')
            api_check = users_collections.count_documents({"API" : api_key})
            
            if api_check != 0:
                user_id = users_collections.find({"API" : api_key}, {"_id" : True})[0]['_id']
                tv_available = users_data_collections.count_documents({"user_id" : user_id, "tv" : {"$elemMatch" : {"tv_id" : tv_id}}})
                print(tv_available)
                if tv_available == 1:
                    # remove tv show
                    print("Removing...")
                    users_data_collections.update_one({"user_id" : user_id}, {"$pull" : {"tv" : {"tv_id" : tv_id}}})
                    print("Removed")
                    response = Response(json.dumps(SuccessStringManagement.REMOVED_FROM_WATCHED_LIST), status=200, mimetype='application/json')
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
                else:
                    raise NOT_FOUND_404_EXCEPTION
            else:
                raise INVALID_API_401_EXCEPTION
        else:
            raise INVALID_API_401_EXCEPTION
    except NOT_FOUND_404_EXCEPTION as e:
        ErrorStringManagement.NOT_FOUND_404['status_message'] = str(e)
        response = Response(json.dumps(ErrorStringManagement.NOT_FOUND_404), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except INVALID_API_401_EXCEPTION:
        response = Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    

@app.route(f'/{APP_SETTINGS.VERSION}/tv/watch', methods=['GET'])
def tv_watched():
    try:
        if "api" in request.args:
            api_key = request.args.get('api')
            api_check = users_collections.count_documents({"API" : api_key})

            if api_check != 0:
                user_id = users_collections.find({"API" : api_key}, {"_id" : True})[0]['_id']
                tv_show_watched_count = users_data_collections.count_documents({"user_id" : user_id, "tv" : {"$exists" : True, "$not" : {"$size" : 0}}})
                if tv_show_watched_count != 0:
                    tv_show_watched = users_data_collections.find({"user_id" : user_id, "tv" : {"$exists" : True, "$not" : {"$size" : 0}}})[0]['tv']
                    
                    watched_tv_data = []
                    if "page" in request.args:
                        page = int(request.args.get('page'))
                        if page > 0:
                            for i in range(0 if page == 1 else APP_SETTINGS.PAGING*(page-1), APP_SETTINGS.PAGING if page == 1 else APP_SETTINGS.PAGING*page):
                                if i < len(tv_show_watched):
                                    tv_coll_data = tv_collections.find({"id" : tv_show_watched[i]['tv_id']}, {'_id': False})
                                    for data in tv_coll_data:
                                        data['watched_language'] = tv_show_watched[i]['watched_language']
                                        data['current_season'] = tv_show_watched[i]['current_season']
                                        data['current_episode'] = tv_show_watched[i]['current_episode']
                                        watched_tv_data.append(data)
                                else:
                                    break
                        else:
                            raise ValueError
                    else:
                        for i in range(0, APP_SETTINGS.PAGING):
                            if i < len(tv_show_watched):
                                tv_coll_data = tv_collections.find({"id" : tv_show_watched[i]['tv_id']}, {'_id': False})
                                for data in tv_coll_data:
                                    data['watched_language'] = tv_show_watched[i]['watched_language']
                                    data['current_season'] = tv_show_watched[i]['current_season']
                                    data['current_episode'] = tv_show_watched[i]['current_episode']
                                    watched_tv_data.append(data)
                            else:
                                break

                    response = Response(json.dumps(watched_tv_data), status=200, mimetype='application/json')
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
                else:
                    response = Response(json.dumps([]), status=200, mimetype='application/json')
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
            else:
                raise INVALID_API_401_EXCEPTION
        else:
            raise INVALID_API_401_EXCEPTION
    except INVALID_API_401_EXCEPTION:
        response = Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except ValueError:
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response





# Movie Routes
@app.route(f'/{APP_SETTINGS.VERSION}/movie/<int:movie_id>', methods=['GET'])
def movie_id_func(movie_id):
    try:
        api_key = request.args.get('api')
        api_check = users_collections.count_documents({"API" : api_key})

        if api_check != 0:
            movie_coll_data = movie_collections.find({"id" : movie_id}, {'_id': False})[0]
            # Convert Data into List
            response = Response(json.dumps(movie_coll_data), status=200, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            raise INVALID_API_401_EXCEPTION

    except INVALID_API_401_EXCEPTION:
        response = Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except IndexError:
        response = Response(json.dumps(ErrorStringManagement.NOT_FOUND_404), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(f'/{APP_SETTINGS.VERSION}/movie/search', methods=['GET'])
def movie_search_name():
    try:
        if "api" in request.args:
            if "query" in request.args:
                if request.args.get("query") != "":
                    api_key = request.args.get('api')
                    api_check = users_collections.count_documents({"API" : api_key})
                    
                    if api_check != 0:
                        movie_name = request.args.get('query')
                        if "page" in request.args:
                            page = int(request.args.get('page'))
                            movie_coll_data = movie_collections.find({"name" : re.compile(movie_name, re.IGNORECASE)}, {'_id': False}).skip(0 if page == 1 else page*APP_SETTINGS.PAGING - APP_SETTINGS.PAGING).limit(APP_SETTINGS.PAGING)
                        else:
                            movie_coll_data = movie_collections.find({"name" : re.compile(movie_name, re.IGNORECASE)}, {'_id': False}).skip(0).limit(APP_SETTINGS.PAGING)

                        # Convert Data into List
                        movie_coll_fetch_data = []
                        for data in movie_coll_data:
                            movie_coll_fetch_data.append(data)
                        response = Response(json.dumps(movie_coll_fetch_data), status=200, mimetype='application/json')
                        response.headers['Access-Control-Allow-Origin'] = '*'
                        return response
                    else:
                        raise INVALID_API_401_EXCEPTION
                else:
                    raise BAD_REQUEST_400_EXCEPTION(ErrorStringManagement.BAD_REQUEST_INCORRECT)
            else:
                raise BAD_REQUEST_400_EXCEPTION(ErrorStringManagement.BAD_REQUEST_INCORRECT)
        else:
            raise INVALID_API_401_EXCEPTION

    except NOT_FOUND_404_EXCEPTION as e:
        ErrorStringManagement.NOT_FOUND_404['status_message'] = str(e)
        response = Response(json.dumps(ErrorStringManagement.NOT_FOUND_404), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except BAD_REQUEST_400_EXCEPTION as e:
        ErrorStringManagement.BAD_REQUEST_400['status_message'] = str(e)
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except INVALID_API_401_EXCEPTION:
        response = Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except ValueError:
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(f'/{APP_SETTINGS.VERSION}/movie/add/<int:movie_id>', methods=['GET'])
def movie_addwatched(movie_id):
    try:
        if "api" in request.args:
            if "language" in request.args:
                l_name = language_name(request.args.get('language'))
                api_key = request.args.get('api')
                watched_language = request.args.get('language')
                api_check = users_collections.count_documents({"API" : api_key})

                if api_check != 0:
                    movie_available = movie_collections.count_documents({"id" : movie_id})
                    if movie_available == 1:
                        # check that language is available
                        language_available = movie_collections.find({"id" : movie_id}, {"_id" : False, "languages" : True})[0]["languages"]
                        if watched_language in language_available:
                            user_id = users_collections.find({"API" : api_key}, {"_id" : True})[0]['_id']
                            movie_already_watched = users_data_collections.count_documents({"user_id" : user_id, "movie" : {"$elemMatch" : {"movie_id" : movie_id}}})
                            print(movie_already_watched)
                            if movie_already_watched == 0:
                                # add new
                                print("Adding...")
                                users_data_collections.update_one({"user_id" : user_id}, {"$push" : {"movie" : { "$each" : [{"movie_id" : movie_id, "watched_language" : watched_language}]}}})
                                print("New added")
                                response = Response(json.dumps(SuccessStringManagement.ADDED_TO_WATCHED_LIST), status=200, mimetype='application/json')
                                response.headers['Access-Control-Allow-Origin'] = '*'
                                return response
                            else:
                                # edit
                                print("Editing...")
                                users_data_collections.update_one({"user_id" : user_id, "movie.movie_id" : movie_id}, {"$set" : {"movie.$.watched_language" : watched_language}})
                                print("Edit Done")
                                response = Response(json.dumps(SuccessStringManagement.EDITED_TO_WATCHED_LIST), status=200, mimetype='application/json')
                                response.headers['Access-Control-Allow-Origin'] = '*'
                                return response
                                
                        else:    
                            raise BAD_REQUEST_400_EXCEPTION(ErrorStringManagement.BAD_REQUEST_LANGUAGE_IS_NOT_AVAILABLE_400)
                    else:
                        raise NOT_FOUND_404_EXCEPTION 
                else:
                    raise INVALID_API_401_EXCEPTION
            else:
                raise BAD_REQUEST_400_EXCEPTION(ErrorStringManagement.BAD_REQUEST_LANGUAGE_NOT_PROVIDED_400)
        else:
            raise INVALID_API_401_EXCEPTION
    except NOT_FOUND_404_EXCEPTION as e:
        ErrorStringManagement.NOT_FOUND_404['status_message'] = str(e)
        response = Response(json.dumps(ErrorStringManagement.NOT_FOUND_404), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except BAD_REQUEST_400_EXCEPTION as e:
        ErrorStringManagement.BAD_REQUEST_400['status_message'] = str(e)
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except INVALID_API_401_EXCEPTION:
        response = Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except (AssertionError, KeyError):
        ErrorStringManagement.BAD_REQUEST_400['status_message'] = ErrorStringManagement.BAD_REQUEST_LANGUAGE_INVALID_400
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(f'/{APP_SETTINGS.VERSION}/movie/remove/<int:movie_id>', methods=['GET'])
def movie_removewatched(movie_id):
    try:
        if "api" in request.args:
            api_key = request.args.get('api')
            api_check = users_collections.count_documents({"API" : api_key})

            if api_check != 0:
                movie_available = movie_collections.count_documents({"id" : movie_id})
                if movie_available == 1:
                    user_id = users_collections.find({"API" : api_key}, {"_id" : True})[0]['_id']
                    movie_already_watched = users_data_collections.count_documents({"user_id" : user_id, "movie" : {"$elemMatch" : {"movie_id" : movie_id}}})
                    print(movie_already_watched)
                    if movie_already_watched == 1:
                        # remove movie
                        print("Removing...")
                        users_data_collections.update_one({"user_id" : user_id}, {"$pull" : {"movie" : {"movie_id" : movie_id}}})
                        print("Removed")
                        response = Response(json.dumps(SuccessStringManagement.REMOVED_FROM_WATCHED_LIST), status=200, mimetype='application/json')
                        response.headers['Access-Control-Allow-Origin'] = '*'
                        return response
                    else:
                        # User haven't watch movie
                        raise BAD_REQUEST_400_EXCEPTION(ErrorStringManagement.BAD_REQUEST_MOVIE_NOT_WATCHED_400)
                else:
                    raise NOT_FOUND_404_EXCEPTION
            else:
                raise INVALID_API_401_EXCEPTION
        else:
            raise INVALID_API_401_EXCEPTION
    except NOT_FOUND_404_EXCEPTION as e:
        ErrorStringManagement.NOT_FOUND_404['status_message'] = str(e)
        response = Response(json.dumps(ErrorStringManagement.NOT_FOUND_404), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except BAD_REQUEST_400_EXCEPTION as e:
        ErrorStringManagement.BAD_REQUEST_400['status_message'] = str(e)
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=404, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except INVALID_API_401_EXCEPTION:
        response = Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(f'/{APP_SETTINGS.VERSION}/movie/watch', methods=['GET'])
def movie_watched():
    try:
        if "api" in request.args:
            api_key = request.args.get('api')
            api_check = users_collections.count_documents({"API" : api_key})

            if api_check != 0:
                user_id = users_collections.find({"API" : api_key}, {"_id" : True})[0]['_id']
                movie_watched_count = users_data_collections.count_documents({"user_id" : user_id, "movie" : {"$exists" : True, "$not" : {"$size" : 0}}})
                if movie_watched_count != 0:
                    movie_watched = users_data_collections.find({"user_id" : user_id, "movie" : {"$exists" : True, "$not" : {"$size" : 0}}})[0]['movie']

                    watched_movie_data = []
                    if "page" in request.args:
                        page = int(request.args.get('page'))
                        if page > 0:
                            for i in range(0 if page == 1 else APP_SETTINGS.PAGING*(page-1), APP_SETTINGS.PAGING if page == 1 else APP_SETTINGS.PAGING*page):
                                if i < len(movie_watched):
                                    movie_coll_data = movie_collections.find({"id" : movie_watched[i]['movie_id']}, {'_id': False})
                                    for data in movie_coll_data:
                                        data['watched_language'] = movie_watched[i]['watched_language']
                                        watched_movie_data.append(data)
                                else:
                                    break
                        else:
                            raise ValueError
                    else:
                        for i in range(0, APP_SETTINGS.PAGING):
                            if i < len(movie_watched):
                                movie_coll_data = movie_collections.find({"id" : movie_watched[i]['movie_id']}, {'_id': False})
                                for data in movie_coll_data:
                                    data['watched_language'] = movie_watched[i]['watched_language']
                                    watched_movie_data.append(data)
                            else:
                                break

                    response = Response(json.dumps(watched_movie_data), status=200, mimetype='application/json')
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
                else:
                    response = Response(json.dumps([]), status=200, mimetype='application/json')
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
            else:
                raise INVALID_API_401_EXCEPTION
        else:
            raise INVALID_API_401_EXCEPTION

    except INVALID_API_401_EXCEPTION:
        response = Response(json.dumps(ErrorStringManagement.INVALID_API_401), status=401, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except ValueError:
        response = Response(json.dumps(ErrorStringManagement.BAD_REQUEST_400), status=400, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        # print(e)
        response = Response(json.dumps(ErrorStringManagement.INTERNAL_SERVER_ERROR_500), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response





# Api routes
def api_unique(api_key):
    api_check = users_collections.count_documents({"API" : api_key})
    if api_check != 0:
        return api_unique(secrets.token_urlsafe(32))
    else:
        return api_key


@app.route(f'/{APP_SETTINGS.VERSION}/api/generate', methods=['POST'])
def generate_api():
    if APP_SETTINGS.DEBUG:
        try:
            generated_api = api_unique(secrets.token_urlsafe(32))

            new_user = {
                "First Name" : request.form['fname'],
                "Last Name" : request.form['lname'],
                "Mobile" : request.form['mobile'],
                "Email" : request.form['email'].lower(),
                "IP" : request.remote_addr,
                "Country" : None,
                "Region" : None,
                "City" : None,
                "API" : generated_api,
                "Worker" : 0,
                "Admin" : 0,
                "Superuser" : 0
            }

            if "superuser" in request.form:
                if request.form['superuser'] == APP_SETTINGS.SUPER_USER:
                    new_user['Admin'] = 1
                    new_user['Superuser'] = 1
                    new_user['Worker'] = 1
            elif "admin" in request.form:
                if request.form['admin'] == APP_SETTINGS.ADMIN_USER:
                    new_user['Admin'] = 1
                    new_user['Worker'] = 1
            elif "worker" in request.form:
                if request.form['worker'] == APP_SETTINGS.WORKER_USER:
                    new_user['Worker'] = 1

            email_check = users_collections.count_documents({"Email" : request.form['email'].lower()})
            mobile_check = users_collections.count_documents({"Mobile" : request.form['mobile']})

            if email_check == 0 and mobile_check == 0:
                user_id = users_collections.insert_one(new_user).inserted_id
                user_data = {
                    "user_id" : user_id,
                    "tv" : [],
                    "movie" : []
                }
                users_data_collections.insert_one(user_data)
                response = Response(json.dumps({'status' : 'success', 'api' : generated_api}), status=201, mimetype='application/json')
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            else:
                response = Response("User Already Exist", status=409, mimetype='application/json')
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
        except Exception as e:
            print(e)
            response = Response("Internal Server Error", status=500, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    else:
        try:
            response = requests.get(f"{APP_SETTINGS.IP_LOOKUP_WEBSITE}{request.environ['HTTP_X_FORWARDED_FOR']}").json()
            if response['status'] == "success":
                generated_api = secrets.token_urlsafe(32)
                new_user = {
                    "First Name" : request.form['fname'],
                    "Last Name" : request.form['lname'],
                    "Mobile" : request.form['mobile'],
                    "Email" : request.form['email'].lower(),
                    "IP" : request.environ['HTTP_X_FORWARDED_FOR'],
                    "Country" : response['country'],
                    "Region" : response['regionName'],
                    "City" : response['city'],
                    "API" : generated_api,
                    "Worker" : 0,
                    "Admin" : 0,
                    "Superuser" : 0
                }

                if "superuser" in request.form:
                    if request.form['superuser'] == APP_SETTINGS.SUPER_USER:
                        new_user['Admin'] = 1
                        new_user['Superuser'] = 1
                        new_user['Worker'] = 1
                elif "admin" in request.form:
                    if request.form['admin'] == APP_SETTINGS.ADMIN_USER:
                        new_user['Admin'] = 1
                        new_user['Worker'] = 1
                elif "worker" in request.form:
                    if request.form['worker'] == APP_SETTINGS.WORKER_USER:
                        new_user['Worker'] = 1

                email_check = users_collections.count_documents({"Email" : request.form['email'].lower()})
                mobile_check = users_collections.count_documents({"Mobile" : request.form['mobile']})

                if email_check == 0 and mobile_check == 0:
                    users_collections.insert_one(new_user).inserted_id
                    response = Response(json.dumps({'status' : 'success', 'api' : generated_api}), status=201, mimetype='application/json')
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
                else:
                    response = Response("User Already Exist", status=409, mimetype='application/json')
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
            else:
                raise Exception
        except Exception as e:
            response = Response("Internal Server Error", status=500, mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response





# Docs route
@app.route(f'/{APP_SETTINGS.VERSION}', methods=['GET'])
def redirect_docs():
    return redirect(f"{APP_SETTINGS.VERSION}/docs", code=302)


@app.route(f'/{APP_SETTINGS.VERSION}/docs', methods=['GET'])
def docs():
    return redirect(APP_SETTINGS.DOCUMENTATION_LINK, code=302)





# Error handlers
@app.errorhandler(400) 
def error400(e): 
    response = Response(json.dumps({'status' : '400 Error'}), status=400, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.errorhandler(404) 
def error404(e): 
    response = Response(json.dumps({'status' : '404 Not Found'}), status=404, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.errorhandler(500) 
def error500(e):
    response = Response(json.dumps({'status' : '500 Internal Server Error'}), status=500, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response





# Run app
if __name__ == "__main__":
    app.run(debug = APP_SETTINGS.DEBUG)