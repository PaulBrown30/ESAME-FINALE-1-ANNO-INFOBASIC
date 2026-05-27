from model.account_model import Courier
from sqlalchemy import select

def get_by_id(session,courier_id):
    return session.get(Courier,courier_id)

def get_all(session):
    return session.execute(select(Courier)).scalars().all()
    

def create(session,courier):
    session.add(courier)
    session.commit()
    return courier

def delete(session,courier_id):
    courier = session.get(Courier,courier_id)
    if courier == None:
        return False
    
    session.delete(courier)
    session.commit()
    return True


