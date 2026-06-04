from persistence.db_config import Base
from sqlalchemy import String,Column,Integer

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String(30), nullable= False)
    surname = Column(String(30), nullable= False)
    email = Column(String(30), nullable= False, unique= True)
    password =Column(String(255), nullable= False)
    account_type = Column(String(30), nullable= False)

    __mapper_args__ = {
        "polymorphic_on" : account_type
    }

    def __repr__(self):
        return f"[{__class__.__tablename__}] --> (name: {self.name}, surname: {self.surname}, email: {self.email}, password: {self.password})"
    
    def __str__(self):
        return f"{self.name} - {self.surname} - {self.email}"
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return other.id == self.id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email
        }