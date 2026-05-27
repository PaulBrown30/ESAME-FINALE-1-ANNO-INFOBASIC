from model.package_model import Package
from sqlalchemy import select

def get_by_id(session,package_id):
    return session.get(Package,package_id)

def get_all(session):
    return session.execute(select(Package)).scalars().all()
    

def create(session,package):
    session.add(package)
    session.commit()
    return package

def delete(session,package_id):
    package = session.get(Package,package_id)
    if package == None:
        return False
    
    session.delete(package)
    session.commit()
    return True

