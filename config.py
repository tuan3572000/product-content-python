
class Config(object):
    """
    Put common configs here
    """

class DevelopmentConfig(Config):
    """
    Development config
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):

    DEBUG = False

app_config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig
}