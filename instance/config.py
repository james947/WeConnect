import os

class BaseConfig(object):
    """Base configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(BaseConfig):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(BaseConfig):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:8247@localhost/weconnect_test'
    DEBUG = True

class StagingConfig(BaseConfig):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(BaseConfig):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
            'development': DevelopmentConfig,
            'testing': TestingConfig,
            'staging': StagingConfig,
            'production': ProductionConfig,
            }