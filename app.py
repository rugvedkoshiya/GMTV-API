from flask import Flask, jsonify, request, Response
from config import TestingConfig as APP_SETTINGS
from flask_pymongo import pymongo
import requests
import secrets
import json
import re
import os
from iso_language_codes import language, language_name, language_autonym

app = Flask(__name__)
app.secret_key = APP_SETTINGS.SECRET_KEY

# Get Data from Database
client = pymongo.MongoClient(APP_SETTINGS.MONGO_LINK)
db = client[APP_SETTINGS.DATABASE_NAME]
tv_collections = db[APP_SETTINGS.TV_COLLECTION_NAME]
movie_collections = db[APP_SETTINGS.MOVIE_COLLECTION_NAME]
users_collections = db[APP_SETTINGS.USER_COLLECTION_NAME]
users_data_collections = db[APP_SETTINGS.USER_DATA_COLLECTION_NAME]

@app.route('/', methods=['GET'])
def index():
    try:
        api_key = request.args.get('api')
        api_check = users_collections.count_documents({"API" : api_key})

        if api_check != 0:
            tv_coll_data = tv_collections.find({}, {'_id': False})
            # Convert Data into List
            tv_coll_fetch_data = []
            for data in tv_coll_data:
                tv_coll_fetch_data.append(data)
            return Response(json.dumps(tv_coll_fetch_data), status=200, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except Exception as e:
        return Response("Internal Server Error", status=500, mimetype='application/json')


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
                return Response("Unauthorized", status=401, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except IndexError:
        return Response("Movie Not Found", status=404, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=500, mimetype='application/json')


@app.route(f'/{APP_SETTINGS.VERSION}/tv/search', methods=['GET'])
def tv_search_func():
    try:
        if "api" in request.args:
            if "query" in request.args:
                api_key = request.args.get('api')
                api_check = users_collections.count_documents({"API" : api_key})
                
                if api_check != 0:
                    tv_name = request.args.get('query')
                    tv_coll_data = tv_collections.find({"name" : re.compile(tv_name, re.IGNORECASE)}, {'_id': False})
                    # Convert Data into List
                    tv_coll_fetch_data = []
                    for data in tv_coll_data:
                        tv_coll_fetch_data.append(data)
                    return Response(json.dumps(tv_coll_fetch_data), status=200, mimetype='application/json')
                else:
                    return Response("Unauthorized", status=401, mimetype='application/json')
            else:
                return Response("No Movie Name Passed", status=401, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except Exception as e:
        return Response("Internal Server Error", status=500, mimetype='application/json')


@app.route(f'/{APP_SETTINGS.VERSION}/tv/add/<int:tv_id>', methods=['GET'])
def tv_add_func(tv_id):
    try:
        if "api" in request.args:
            if "language" in request.args and "season" in request.args and "episode" in request.args:
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
                                        return Response(json.dumps("{'status' : 200, 'message' : 'Data Added Successfully'}"), status=200, mimetype='application/json')
                                    else:
                                        # edit
                                        print("Editing...")
                                        users_data_collections.update_one({"user_id" : user_id, "tv.tv_id" : tv_id}, {"$set" : {"tv.$.watched_language" : watched_language, "tv.$.current_season" : current_season, "tv.$.current_episode" : current_episode}})
                                        print("Edit Done")
                                        return Response(json.dumps("{'status' : 200, 'message' : 'Data Edited Successfully'}"), status=200, mimetype='application/json')
                                else:
                                    return Response("episode vadhi na gaya?", status=401, mimetype='application/json')
                            else:
                                return Response("etli badhi season chhe j nai", status=401, mimetype='application/json')
                        else:
                            print("nathi")
                    else:
                        return Response("TV Show Not Available", status=401, mimetype='application/json')
                else:
                    return Response("Unauthorized", status=401, mimetype='application/json')
            else:
                return Response("Data not Given", status=401, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except AssertionError:
        return Response("This is not valid language code", status=500, mimetype='application/json')
    except KeyError:
        return Response("This language is not avialable", status=500, mimetype='application/json')
    except ValueError:
        return Response("Season & episode name are not correct", status=500, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=500, mimetype='application/json')

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
                    return Response(json.dumps("{'status' : 200, 'message' : 'TV Show Removed Successfully'}"), status=200, mimetype='application/json')
                else:
                    return Response("You haven't watch this movie", status=401, mimetype='application/json')
            else:
                return Response("Unauthorized", status=401, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=500, mimetype='application/json')
    

@app.route(f'/{APP_SETTINGS.VERSION}/tv/watch/', methods=['GET'])
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
                    for tvshow in tv_show_watched:
                        tv_coll_data = tv_collections.find({"id" : tvshow['tv_id']}, {'_id': False})
                        # Convert Data into List
                        for data in tv_coll_data:
                            data['watched_language'] = tvshow['watched_language']
                            data['current_season'] = tvshow['current_season']
                            data['current_episode'] = tvshow['current_episode']
                            watched_tv_data.append(data)

                    return Response(json.dumps(watched_tv_data), status=200, mimetype='application/json')
                else:
                    return Response("No TV show you have watched yet", status=200, mimetype='application/json')
            else:
                return Response("Unauthorized", status=401, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except Exception as e:
        return Response("Internal Server Error", status=500, mimetype='application/json')








# Movie Routes
@app.route(f'/{APP_SETTINGS.VERSION}/movie/<int:movie_id>', methods=['GET'])
def movie_id_func(movie_id):
    try:
        api_key = request.args.get('api')
        api_check = users_collections.count_documents({"API" : api_key})

        if api_check != 0:
            movie_coll_data = movie_collections.find({"id" : movie_id}, {'_id': False})[0]
            # Convert Data into List
            return Response(json.dumps(movie_coll_data), status=200, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except IndexError:
        return Response("Movie not available", status=500, mimetype='application/json')
    except Exception as e:
        return Response("Internal Server Error", status=500, mimetype='application/json')


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
                        movie_coll_data = movie_collections.find({"name" : re.compile(movie_name, re.IGNORECASE)}, {'_id': False})
                        # Convert Data into List
                        movie_coll_fetch_data = []
                        for data in movie_coll_data:
                            movie_coll_fetch_data.append(data)
                        return Response(json.dumps(movie_coll_fetch_data), status=200, mimetype='application/json')
                    else:
                        return Response("Unauthorized", status=401, mimetype='application/json')
                else:
                    return Response("No name Provided", status=401, mimetype='application/json')
            else:
                return Response("No Movie Name Given", status=401, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except Exception as e:
        return Response("Internal Server Error", status=500, mimetype='application/json')


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
                                return Response(json.dumps("{'status' : 200, 'message' : 'Data Added Successfully'}"), status=200, mimetype='application/json')
                            else:
                                # edit
                                print("Editing...")
                                users_data_collections.update_one({"user_id" : user_id, "movie.movie_id" : movie_id}, {"$set" : {"movie.$.watched_language" : watched_language}})
                                print("Edit Done")
                                return Response(json.dumps("{'status' : 200, 'message' : 'Data Edited Successfully'}"), status=200, mimetype='application/json')
                        else:    
                            return Response("Language is not available for this movie", status=401, mimetype='application/json')
                    else:
                        return Response("Movie Not Available", status=401, mimetype='application/json')
                else:
                    return Response("Unauthorized", status=401, mimetype='application/json')
            else:
                return Response("Watched Language not provided", status=401, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except AssertionError:
        return Response("language code 2 chracter no hoy", status=500, mimetype='application/json')
    except KeyError:
        return Response("Key Error language chhe nai avi kai", status=500, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=500, mimetype='application/json')


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
                        return Response(json.dumps("{'status' : 200, 'message' : 'Movie Removed Successfully'}"), status=200, mimetype='application/json')
                    else:
                        # User haven't watch movie
                        return Response("You haven't watch this movie", status=401, mimetype='application/json')
                else:
                    return Response("Movie Not Available", status=401, mimetype='application/json')
            else:
                return Response("Unauthorized", status=401, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=500, mimetype='application/json')


@app.route(f'/{APP_SETTINGS.VERSION}/movie/watch/', methods=['GET'])
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
                    for movie in movie_watched:
                        movie_coll_data = movie_collections.find({"id" : movie['movie_id']}, {'_id': False})
                        # Convert Data into List
                        for data in movie_coll_data:
                            data['watched_language'] = movie['watched_language']
                            watched_movie_data.append(data)

                    return Response(json.dumps(watched_movie_data), status=200, mimetype='application/json')
                else:
                    return Response("No Movie you have watched yet", status=200, mimetype='application/json')
            else:
                return Response("Unauthorized", status=401, mimetype='application/json')
        else:
            return Response("Unauthorized", status=401, mimetype='application/json')
    except Exception as e:
        return Response("Internal Server Error", status=500, mimetype='application/json')




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
                return Response(json.dumps({'status' : 'success', 'api' : generated_api}), status=201, mimetype='application/json')
            else:
                return Response("User Already Exist", status=409, mimetype='application/json')
        except Exception as e:
            print(e)
            return Response("Internal Server Error", status=500, mimetype='application/json')
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
                    return Response(json.dumps({'status' : 'success', 'api' : generated_api}), status=201, mimetype='application/json')
                else:
                    return Response("User Already Exist", status=409, mimetype='application/json')
            else:
                raise Exception
        except Exception as e:
            return Response("Internal Server Error", status=500, mimetype='application/json')






# Error handlers
@app.errorhandler(400) 
def error400(e): 
  return Response(json.dumps({'status' : '400 Error'}), status=400, mimetype='application/json')

@app.errorhandler(404) 
def error404(e): 
  return Response(json.dumps({'status' : '404 Not Found'}), status=404, mimetype='application/json')

@app.errorhandler(500) 
def error500(e): 
    return Response(json.dumps({'status' : '500 Internal Server Error'}), status=500, mimetype='application/json')


# Run app
if __name__ == "__main__":
    app.run(debug = APP_SETTINGS.DEBUG)