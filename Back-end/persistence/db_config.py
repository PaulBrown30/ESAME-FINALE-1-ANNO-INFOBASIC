from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://postgres:database@localhost:5432/GESTORE_SPEDIZIONI",echo=True)


localSession = sessionmaker(bind = engine)

Base = declarative_base()

def get_session():
    return localSession()


def db_init():
    import model.account_model
    import model.admin_model
    import model.courier_model
    import model.package_model
    import model.status_model
    import model.user_model

    Base.metadata.drop_all(bind = engine)   
    Base.metadata.create_all(bind = engine)