from model.account_model import Account
from sqlalchemy import String,Integer,Column, ForeignKey

class User(Account):
    __tablename__ = "user"

    id = Column(Integer,ForeignKey("account.id", ondelete= "CASCADE"),primary_key= True)

    __mapper_args__ = {
        "polymorphic_identity" : "user"
    }

    def __repr__(self):
        return f"[{__class__.__tablename__}] --> (name: {self.name}, surname: {self.surname}, email: {self.email}, password: {self.password}, account_type: {self.account_type})"
    
    def __str__(self):
        return f"{self.name} - {self.surname} - {self.email}"
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        if other.id == self.id:
            return True
