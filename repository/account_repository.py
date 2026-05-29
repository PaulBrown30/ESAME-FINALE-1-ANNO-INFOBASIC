from model.account_model import Account
from sqlalchemy import select

def check_used_email(session,account):
    return session.esecute(select(Account)).where(Account.id != account.id, Account.email == account.email).scalar_one_or_none()

