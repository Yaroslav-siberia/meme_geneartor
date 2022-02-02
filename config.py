class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    STATIC_PLACEHOLDER_IMG = "/static/images/placeholder-image.png"
    HOST = '0.0.0.0'
    PORT = 3000


class DevelopmentConfig(Config):

    STATIC_PLACEHOLDER_IMG = "/static/images/placeholder-image.png"
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    HOST = '127.0.0.1'
    PORT = 3000


class TestingConfig(Config):
    TESTING = True
