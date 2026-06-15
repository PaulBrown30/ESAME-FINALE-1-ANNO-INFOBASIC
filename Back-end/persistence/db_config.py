from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_ENV = BASE_DIR / ".env.local"
load_dotenv(dotenv_path=PATH_ENV)

NOME_UTENTE_DATABASE = os.environ.get("NOME_UTENTE_DATABASE")
PASSWORD_DATABASE = os.environ.get("PASSWORD_DATABASE")
PORT = os.environ.get("PORT")
NOME_DATABASE = os.environ.get("NOME_DATABASE")

print(NOME_DATABASE, PASSWORD_DATABASE)

engine = create_engine(f"postgresql://{NOME_UTENTE_DATABASE}:{PASSWORD_DATABASE}@localhost:{PORT}/{NOME_DATABASE}",echo=True)


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