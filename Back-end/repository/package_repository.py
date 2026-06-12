from model.package_model import Package
from model.status_model import Status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import datetime

def get_by_id(session,package_id):
    return session.execute(select(Package).where(Package.id == package_id).options(selectinload(Package.statuses))).unique().scalar_one_or_none() 

def get_all(session):
    return session.execute(select(Package).options(selectinload(Package.statuses))).scalars().all()
    
def create(session,package):
    session.add(package)

    status = session.get(Status,"S-001")
    if status == None:
        return False
    
    package.statuses.append(status)

    session.commit()
    return session.execute(select(Package).where(Package.id == package.id).options(selectinload(Package.statuses))).unique().scalar_one_or_none() 

def delete_by_id(session,package_id):
    package = session.get(Package,package_id)
    if package == None:
        return False
    
    session.delete(package)
    session.commit()
    return True

def add_status(session,package_id,status_id):
    # questa riga controlla che esista un pacco con quel ID e che non abbia gia uno status con l'ID da inserire!
    package = session.execute(select(Package).where(Package.id == package_id).options(selectinload(Package.statuses))).scalar_one_or_none()

    if package == None:
        return 0
    
    status = session.get(Status,status_id)
    if status == None:
        return 1
    
    if not package.statuses and status_id != "S-001":
        return 2
    
    if package.statuses:
        if status not in package.statuses[-1].next_ammitted_statuses:
            return 3

    package.statuses.append(status)
    session.commit()
    session.refresh(package)
    return package

def set_inactive(session,package_id):
    package = session.get(Package,package_id)
    if package == None:
        return False
    
    package.active = False
    
    session.commit()
    session.refresh(package)
    return package

def set_arrival_date(session,package_id):
    package = session.get(Package,package_id)
    if package == None:
        return False
    
    package.actual_arrival_date = datetime.datetime.now()
    
    session.commit()
    session.refresh(package)
    return package

def check_used_id(session,package):
    return session.execute(select(Package).where(Package.id == package.id)).scalar_one_or_none()

