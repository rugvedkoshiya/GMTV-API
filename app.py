from swaggerConfig import app
import os
import routes.route_auth
import routes.route_movie
import routes.route_tv
import routes.route_user
from models.config import Config as SETTING
from dotenv import load_dotenv

if __name__ == "__main__":
    # print(os.environ)
    load_dotenv()
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run(port=5000, debug=SETTING.DEBUG)
