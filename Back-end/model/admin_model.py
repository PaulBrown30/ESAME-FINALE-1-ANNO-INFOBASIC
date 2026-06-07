from model.account_model import Account
from sqlalchemy import String,Integer,Column, ForeignKey

class Admin(Account):
    __tablename__ = "admin"

    id = Column(Integer,ForeignKey("account.id", ondelete= "CASCADE"),primary_key= True)

    __mapper_args__ = {
        "polymorphic_identity" : "admin"
    }

    def __repr__(self):
        return f"[{__class__.__tablename__}] --> (name: {self.name}, surname: {self.surname}, email: {self.email}, password: {self.password})"
    
    def __str__(self):
        return f"{self.name} - {self.surname} - {self.email}"
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "type": self.account_type
        }