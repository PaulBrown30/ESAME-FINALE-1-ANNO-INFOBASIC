from persistence.db_config import Base
from sqlalchemy import Column,Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from model.package_model import package_status


admitted_status_transitions = Table (
    "ammitted_status_transitions",
    Base.metadata,
    Column("existing_status_id", String(5), ForeignKey("status.id", ondelete="CASCADE"), primary_key=True),
    Column("added_status_id", String(5), ForeignKey("status.id", ondelete="CASCADE"), primary_key=True),
)

class Status(Base):
    __tablename__ = "status"

    id = Column(String(5),primary_key=True)
    name = Column(String(30), nullable=False, unique= False)
    description = Column(String(100), nullable=False)

    packages = relationship("Package",
                            secondary= package_status,
                            back_populates= "statuses" )

    next_ammitted_statuses = relationship("Status",
                            secondary = admitted_status_transitions,
                            primaryjoin = (id == admitted_status_transitions.c.existing_status_id),
                            secondaryjoin = (id == admitted_status_transitions.c.added_status_id),
                            foreign_keys=[
                                admitted_status_transitions.c.existing_status_id,
                                admitted_status_transitions.c.added_status_id,
                            ],)

    def __repr__(self):
        return f"[{self.__class__.__tablename__}] --> (id: {self.id}, name: {self.name}, description: {self.description})"

    def __str__(self):
        return f"{self.name} - {self.description}"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return other.id == self.id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }