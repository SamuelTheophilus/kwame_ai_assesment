from os import environ, path
from dotenv import load_dotenv

project_root = path.abspath(path.join(path.dirname(__file__), ".."))
load_dotenv(path.join(project_root, ".env"))


class Config(object):
    DEBUG = False
    TESTING = False
    ELASTIC_SEARCH_URL = "http://localhost:9200"
    FLASK_ENV = "production"
    
class DevConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"

class TestingConfig(Config):
    TESTING = True
    FLASK_ENV = "testing"


config_name = {
    "production": Config,
    "development": DevConfig,
    "testing": TestingConfig
}

def get_config():
    environment = environ.get("environment", "development")
    return config_name.get(environment)
