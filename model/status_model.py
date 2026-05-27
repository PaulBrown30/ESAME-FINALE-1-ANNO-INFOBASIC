from persistence.db_config import Base
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import relationship
from model.package_model import package_status

class Status(Base):
    __tablename__ = "status"

    id = Column(String(10),primary_key=True)
    name = Column(String(30), nullable=False, unique= False)
    description = Column(String(100), nullable=False)

    packages = relationship("Package",
                            secondary= package_status,
                            back_populates= "statuses" )

    def __repr__(self):
        return f"[{self.__class__.__tablename__}] --> (id: {self.id}, name: {self.name}, description: {self.de})"

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