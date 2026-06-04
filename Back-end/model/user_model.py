from model.account_model import Account
from sqlalchemy import String,Integer,Column, ForeignKey
from sqlalchemy.orm import relationship
from model.package_model import package_user

class User(Account):
    __tablename__ = "user"

    id = Column(Integer,ForeignKey("account.id", ondelete= "CASCADE"),primary_key= True)

    packages = relationship("Package",
                            secondary= package_user,
                            back_populates= "users")

    __mapper_args__ = {
        "polymorphic_identity" : "user"
    }

    def __repr__(self):
        return f"[{__class__.__tablename__}] --> (name: {self.name}, surname: {self.surname}, email: {self.email}, password: {self.password}, account_type: {self.account_type})"
    
    def __str__(self):
        return f"{self.name} - {self.surname} - {self.email}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email
        }