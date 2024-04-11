import os

# to load environment varibles from env file import dotenv.
from dotenv import load_dotenv

load_dotenv()


# configuration file in software devloment is used for setting configuration for development and production phase of application.
# for develoment configuration like database_url and  jwt_key might be diffrent and for production it will be diffrent.

class DevelopmentConfig():
    DEBUG=True
    dev_db_url = "sqlite:///dev_library.db"
    
class ProductionConfig():
    DEBUG=True
    prod_db_url = os.getenv("PRODUCTION_DB_URL")
    