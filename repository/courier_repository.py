from model.courier_model import Courier
from model.package_model import Package
from sqlalchemy import select,func

def get_by_id(session,courier_id):
    return session.get(Courier,courier_id)

def get_all(session):
    return session.execute(select(Courier)).scalars().all()

def get_available_couriers(session):
    return session.execute(select(Courier).outerjoin(Courier.packages).group_by(Courier.id).having(func.count(Package.id)< Courier.max_load)).scalars().all()
    
def create(session,courier):
    session.add(courier)
    session.commit()
    session.refresh(courier)
    return courier

def update(session,courier):
    courier = session.merge(courier)
    session.commit()
    return courier

def delete_by_id(session,courier_id):
    courier = session.get(Courier,courier_id)
    if courier == None:
        return False
    
    session.delete(courier)
    session.commit()
    return True

def check_used_phone_number(session,courier):
    return session.execute(select(Courier).where(Courier.id != courier.id, Courier.phone_number == courier.phone_number)).scalar_one_or_none()



