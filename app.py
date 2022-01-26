from swaggerConfig import app
import os
import routes.route_auth
import routes.route_movie
import routes.route_tv
from models.config import Config as SETTING

if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run(port=5000, debug=SETTING.DEBUG)
