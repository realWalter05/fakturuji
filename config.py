
class Config(object):
    DEBUG = True
    TESTING = False

    SECRET_KEY = "I\x99\x1a\x88o\x95\xcdIr\xbe\xed\xa8\xbav\x82G1\x98\x17\xb5\x7f\rJ~"

    DB_HOST  = "localhost"
    DB_USERNAME  = "root"
    DB_PASSWORD  = "Fakturuji_db123"
    DB_DATABASE  = "faktury"

    FAKTURA_CSS_PATH = "/var/www/fakturuji/static/css/faktura.css"

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    ENV = "production"
    pass


class DevelopmentConfig(Config):
    ENV = "development"

    DB_HOST  = "localhost"
    DB_USERNAME  = "root"
    DB_PASSWORD  = ""
    DB_DATABASE  = "faktury"
    DEBUG = True

    FAKTURA_CSS_PATH = "C:/Users/zikav/dev/Python/fakturuji/static/css/faktura.css"
