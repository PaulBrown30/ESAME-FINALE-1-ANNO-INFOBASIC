from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://postgres:database@localhost:5432/GESTORE_SPEDIZIONI",echo=True)


localSession = sessionmaker(bind = engine)

Base = declarative_base()

def get_session():
    return localSession()


def db_init():

    Base.metadata.create_all(bind = engine)