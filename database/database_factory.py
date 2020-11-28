from sqlalchemy import create_engine
from config import DevConfig, TestConfig, ProdConfig
from os import environ
 
class DatabaseFactory:
    
    @staticmethod
    def get():
        env = environ.get('FLASK_ENV')
        if env == 'development':
            engine = create_engine(DevConfig.DATABASE_URI)
        elif env == 'test':
            engine = create_engine(TestConfig.DATABASE_URI)
        elif env == 'production':
            engine = create_engine(ProdConfig.DATABASE_URI)
        return engine
