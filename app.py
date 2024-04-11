# now here we will be uniting all blueprints of application into one. so lets import them.

from src.resorces.book import blp as BooksBluprint
from src.resorces.user import blp as UserBlueprint
from src.resorces.issue import blp as IssueBlueprint

# we will be needing load_dotenv to choose specific environment
from dotenv import load_dotenv

from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

from src.db.database import db


import os

from src.config import DevelopmentConfig,ProductionConfig


load_dotenv()

API_DEFAULT_PATH ="/api/v1"

# now we will call flask function create_app which will creat flask application along with application configuration and its other settings
def create_app(db_url = None):
    # we have initialized flask app with Flask method
    app = Flask(__name__)
    
    # now lets configurate other application settings
    """
    here we are setting PROPAGATE_EXCEPTIONS = True, meaning that when our app is handling request and error comes 
    then our flask app will show error rather than hiding the error.
    """
    app.config["PROPAGATE_EXCEPTIONS"]=True
    """
    API_TITLE="library API" this will give our swagger documentation title or our entore API title as Library API
    """
    app.config["API_TITLE"]="library_api"
    """
    "API_VERSION="V1" we will be setting version for our API to keep track of our api
    """
    app.config["API_VERSION"]="v1"
    """
    OPENAPI_VERSION="1.0.0 this will keep our openapi version to 1.0.0
    """
    app.config["OPENAPI_VERSION"]="3.0.3"
    """
    now lets give default url route to access diff api in our app
    """
    app.config["OPENAPI_URL_PREFIX"]="api/v1"
    """
    url to get swagger-ui documentation
    """
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    """
    lets choose db based on env variables
    """
    app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///dev_library.db"
    
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui-dist/dist"

    
    # now lets prepare SQLALchemy sessions.by doing this we can use sqlalchemy session,modules and etc
    db.init_app(app)
    
    # lets initialize flask_migrate module for database migrations.
    migrate = Migrate(app,db)
    # here we will be defining restful services to access HTTP methods.HTTP ,ethods defined in blueprints.
    api = Api(app)
    
    
    
    # now lets register all blueprints to get all part of application routes and threr methods.
    api.register_blueprint(UserBlueprint,url_prefix = API_DEFAULT_PATH)
    api.register_blueprint(IssueBlueprint,url_prefix = API_DEFAULT_PATH)
    api.register_blueprint(BooksBluprint,url_prefix = API_DEFAULT_PATH)
    
    return app