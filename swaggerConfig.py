from flask import Flask, g
from datetime import datetime
import time, decimal, json
from flask_restx import Api
from flask_mail import Mail
from models.config import Config as SETTING


app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = SETTING.MAIL_SERVER
app.config['MAIL_PORT'] = SETTING.MAIL_PORT
app.config['MAIL_USERNAME'] = SETTING.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = SETTING.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.before_request
def before_request():
    g.start_time = time.time()
    g.response = {}


def myconverter(o):
    if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
        return o.__str__()
    elif isinstance(o, decimal.Decimal):
        return float(o)


@app.after_request
def after_request(res):
    print(time.time() - g.start_time)
    try:
        if (res.get_data()).decode("utf-8") == "null\n":
            res.set_data(json.dumps(g.response, default=myconverter))
        return res
    except Exception as e:
        return res

authorizations = {
    'api_key' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'X-API-Key'
    }
}

api = Api(
    app,
    version="1.0",
    title="GMTV",
    description="GMTV API Documentation",
    authorizations=authorizations,
    security=["api_key"],
    prefix="/v1",
)
