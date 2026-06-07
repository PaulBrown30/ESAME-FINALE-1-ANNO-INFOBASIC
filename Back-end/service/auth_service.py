from repository import account_repository
from persistence.db_config import get_session
from exception.app_exception import AppException
import bcrypt
import datetime
import jwt

SECRET_KEY = "Chiave-segreta di prova"

def login(access_data):

    for field in ["email","password"]:
        if field not in access_data:
            raise AppException(f"Il campo {field} non è presente",400)

    with get_session() as session:

        account = account_repository.get_by_email(session,access_data)

        if account == None:
            raise AppException(f"Credenziali errate!",401)

        password_valida = bcrypt.checkpw(
            access_data["password"].encode("utf-8"), account.password.encode("utf-8")
        )        

        if password_valida == False:
            raise AppException(f"Credenziali errate!",401)  

        payload = {
            "id": account.id,
            "email": account.email,
            "account_type": account.account_type,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm = "HS256")

        return token,account
    
def verifica_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm="HS256")
        return payload
    except jwt.ExpiredSignatureError:
        raise AppException("Token scaduto!",401)
    except jwt.ExpiredSignatureError:
        raise AppException("Token non valido!",401)