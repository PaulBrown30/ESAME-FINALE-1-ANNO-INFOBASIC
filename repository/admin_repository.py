from model.account_model import Admin


def get_by_id(session,admin_id):
    return session.get(Admin,admin_id)


def create(session,admin):
    session.add(admin)
    session.commit()
    return admin