from source.routes.api import create_app#import app from source folder
import os

"get develoments settings from the env variable"
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

#starts the app
if __name__ == "__main__":
     app.run()