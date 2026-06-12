from model.status_model import Status
from sqlalchemy import select

def get_by_id(session,status_id):
    return session.get(Status,status_id)

def get_all(session):
    return session.execute(select(Status)).scalars().all()

def create(session,status):
    session.add(status)
    session.commit()
    session.refresh(status)
    return status

def add_status_transitions(session,existing_status, added_status):
    if added_status in existing_status.next_ammitted_statuses:
        return False
    existing_status.next_ammitted_statuses.append(added_status)
    session.commit()
    return True

def check_used_name(session,status):
    return session.execute(select(Status).where(Status.name == status.name, Status.id != status.id)).scalar_one_or_none()

def check_used_id(session,status):
    return session.execute(select(Status).where(Status.id == status.id)).scalar_one_or_none()



