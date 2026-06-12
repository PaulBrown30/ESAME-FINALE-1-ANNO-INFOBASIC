from model.account_model import Account
from sqlalchemy import String,Integer,Column, ForeignKey
from sqlalchemy.orm import relationship

class Courier(Account):
    __tablename__ = "courier"

    id = Column(Integer,ForeignKey("account.id", ondelete= "CASCADE"),primary_key= True)
    phone_number = Column(String(10), nullable= False, unique=True)
    birth_date = Column(String(10), nullable= False)
    current_cap = Column(String(5), nullable= False, default= "65124")

    packages = relationship("Package",back_populates="courier")

    __mapper_args__ = {
        "polymorphic_identity" : "courier"
    }

    def __repr__(self):
        return f"[{__class__.__tablename__}] --> (name: {self.name}, surname: {self.surname}, email: {self.email}, password: {self.password}, phone_number: {self.phone_number}, birth date: {self.birth_date})"
    
    def __str__(self):
        return f"{self.name} - {self.surname} - {self.email} - {self.phone_number} - {self.birth_date}"
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "phone_number": self.phone_number,
            "birth_date": self.birth_date,
            "type": self.account_type,
            "current_cap": self.current_cap,
            "packages": [p.to_dict() for p in self.packages]
        }