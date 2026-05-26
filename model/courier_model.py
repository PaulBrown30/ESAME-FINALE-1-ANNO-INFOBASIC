from model.account_model import Account
from sqlalchemy import String,Integer,Column, ForeignKey
from sqlalchemy.orm import relationship

class Courier(Account):
    __tablename__ = "courier"

    id = Column(Integer,ForeignKey("account.id", ondelete= "CASCADE"),primary_key= True)
    phone_number = Column(String(10), nullable= False)
    max_load = Column(Integer, nullable= False, default = 0)
    birth_date = Column(String, nullable= False)

    courier_package = relationship("Package",back_populates="package_courier")

    __mapper_args__ = {
        "polymorphic_identity" : "courier"
    }

    def __repr__(self):
        return f"[{__class__.__tablename__}] --> (name: {self.name}, surname: {self.surname}, email: {self.email}, password: {self.password}, phone_number: {self.phone_number}, max_load: {self.max_load}, birth date: {self.birth_date})"
    
    def __str__(self):
        return f"{self.name} - {self.surname} - {self.email} - {self.phone_number} - {self.max_load} - {self.birth_date}"
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "password": self.password,
            "phone_number": self.phone_number,
            "max_load": self.max_load,
            "birth_date": self.birth_date
        }