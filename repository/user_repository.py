from model.user_model import User
from model.package_model import Package
from sqlalchemy import select,not_


def get_by_id(session,user_id):
    return session.get(User,user_id)

def create(session,user):
    session.add(user)
    session.commit()
    return user

def add_package(session,user_id,package_id):
    # questa riga controlla che esiste un utente con quel ID e che non abbia gia un pacco con l'ID da inserire!
    user = session.execute(select(User).where(User.id == user_id, not_(User.packages.any(Package.id == package_id)))).scalar_one_or_none()
    if user == None:
        return False
    
    package = session.get(Package,package_id)
    if package == None:
        return False
    
    user.packages.append(package)
    session.commit()
    return True

