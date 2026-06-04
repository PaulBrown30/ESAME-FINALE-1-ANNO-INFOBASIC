from model.package_model import Package
from model.status_model import Status
from sqlalchemy import select, not_

def get_by_id(session,package_id):
    return session.get(Package,package_id)

def get_all(session):
    return session.execute(select(Package)).scalars().all()
    
def create(session,package):
    session.add(package)

    status = session.get(Status,"S-001")
    if status == None:
        return False
    
    package.statuses.append(status)

    session.commit()
    session.refresh(package)
    return package

def delete_by_id(session,package_id):
    package = session.get(Package,package_id)
    if package == None:
        return False
    
    session.delete(package)
    session.commit()
    return True

def add_status(session,package_id,status_id):
    # questa riga controlla che esista un pacco con quel ID e che non abbia gia uno status con l'ID da inserire!
    package = session.execute(select(Package).where(Package.id == package_id, not_(Package.statuses.any(Status.id == status_id)))).scalar_one_or_none()

    if package == None:
        return False
    
    status = session.get(Status,status_id)
    if status == None:
        return False
    
    package.statuses.append(status)
    session.commit()
    return True

def set_inactive(session,package_id):
    package = session.get(Package,package_id)
    if package == None:
        return False
    
    package.active = False
    
    session.commit()
    session.refresh(package)
    return package




    
    

def check_used_id(session,package):
    return session.execute(select(Package).where(Package.id == package.id)).scalar_one_or_none()

