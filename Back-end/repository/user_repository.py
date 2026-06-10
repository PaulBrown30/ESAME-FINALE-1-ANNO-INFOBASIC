from model.user_model import User
from model.package_model import Package
from repository import package_repository
from sqlalchemy import select,not_
from sqlalchemy.orm import joinedload,selectinload


def get_by_id(session,user_id):
    return session.execute(select(User).where(User.id == user_id).options(selectinload(User.packages).selectinload(Package.statuses))).unique().scalar_one_or_none()

def create(session,user):
    session.add(user)
    session.commit()
    session.refresh(user)
    return session.execute(select(User).where(User.id == user.id).options(selectinload(User.packages).selectinload(Package.statuses))).unique().scalar_one_or_none()

def add_package(session,user_id,package_id):
    # questa riga controlla che esiste un utente con quel ID e che non abbia gia un pacco con l'ID da inserire!
    user = session.get(User,user_id)
    if user == None:
        return 0

    package = package_repository.get_by_id(session,package_id)
    if package == None:
        return 1
    
    user = session.execute(select(User).where(User.id == user_id, not_(User.packages.any(Package.id == package_id)))).scalar_one_or_none()
    if user == None:
        return 2
      
    user.packages.append(package)
    session.commit()
    session.refresh(package)
    return package



