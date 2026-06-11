from model.courier_model import Courier
from model.account_model import Account
from model.package_model import Package
from model.status_model import Status
from sqlalchemy import select,func
from sqlalchemy.orm import selectinload, with_loader_criteria

def get_by_id(session,courier_id):
    return session.execute(select(Courier).where(Courier.id == courier_id).options(selectinload(Courier.packages)
            .selectinload(Package.statuses),with_loader_criteria(Package,Package.active == True))).unique().scalar_one_or_none()

def get_all(session):
    return session.execute(select(Courier).options(selectinload(Courier.packages)
            .selectinload(Package.statuses),with_loader_criteria(Package,Package.active == True))).unique().scalars().all()

def get_available_couriers(session):
    return session.execute(select(Courier).outerjoin(Courier.packages,Package.active == True).group_by(Courier.id, Account.id).having(func.count(Package.id)< Courier.max_load)).scalars().all()

def get_less_packages_courier(session):
    return session.execute(select(Courier).outerjoin(Courier.packages).group_by(Account.id, Courier.id)
                           .order_by(func.count(Package.id).filter(Package.active == True).asc())
                           .options(selectinload(Courier.packages),with_loader_criteria(Package, Package.active == True)).limit(1)).scalar_one_or_none()
    

def create(session,courier):
    session.add(courier)
    session.commit()
    session.refresh(courier)
    return session.execute(select(Courier).where(Courier.id == courier.id).options(selectinload(Courier.packages)
            .selectinload(Package.statuses),with_loader_criteria(Package,Package.active == True))).unique().scalar_one_or_none()

def update(session,courier):
    courier = session.merge(courier)
    session.commit()
    session.refresh(courier)
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



