from sqlalchemy.orm import Session 
from sqlalchemy import *

class DBSettings():
    @staticmethod
    def get_session():
        engine = create_engine(f"postgresql+psycopg2://postgres:root@localhost:5432/pr10_sistem")
        return Session(bind=engine)