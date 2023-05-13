from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import app_config

class Database:
    def __init__(self):
        self.engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI, echo=False, pool_size=20, max_overflow=0)

    def get_session(self):
        self.session = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.get_session()
        return self.session()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.engine.dispose()
    
    

    

