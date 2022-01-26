from flask import Flask, g
from datetime import datetime
import time, decimal, json
from flask_restx import Api


app = Flask(__name__)

@app.before_request
def before_request():
    print("before_request")
    g.start_time = time.time()
    g.response = {}


def myconverter(o):
    if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
        return o.__str__()
    elif isinstance(o, decimal.Decimal):
        return float(o)


@app.after_request
def after_request(res):
    print("after_request")
    try:
        if (res.get_data()).decode("utf-8") == "null\n":
            res.set_data(json.dumps(g.response, default=myconverter))
        return res
    except Exception as e:
        return res


api = Api(
    app,
    version="1.0",
    title="GMTV",
    description="GMTV API Documentation",
    security=["api_key"],
    prefix="/v1",
)
