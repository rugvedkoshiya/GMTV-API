from dotenv import load_dotenv
load_dotenv()


from swaggerConfig import app
import os
import routes.route_auth
import routes.route_movie
import routes.route_tv
import routes.route_user
from models.config import Config as SETTING


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run(port=SETTING.PORT, debug=SETTING.DEBUG)
