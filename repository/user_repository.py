from model.account_model import User


def get_by_id(session,user_id):
    return session.get(User,user_id)


def create(session,user):
    session.add(user)
    session.commit()
    return user
