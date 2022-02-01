from flask_pymongo import pymongo
from models.config import Config as SETTING

# Get Data from Database
client = pymongo.MongoClient(SETTING.MONGO_LINK)
db = client[SETTING.DATABASE_NAME]
tvCollections = db[SETTING.TV_COLLECTION_NAME]
movieCollections = db[SETTING.MOVIE_COLLECTION_NAME]
userCollections = db[SETTING.USER_COLLECTION_NAME]
userDataCollections = db[SETTING.USER_DATA_COLLECTION_NAME]
resetPassword = db[SETTING.RESET_PASSWORD_COLLECTION_NAME]