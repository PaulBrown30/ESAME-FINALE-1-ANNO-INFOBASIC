from persistence.db_config import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
import datetime


package_user = Table(
    "package_user",
    Base.metadata,
    Column("package_id", String(10),ForeignKey("package.id"), primary_key=True),
    Column("user_id",Integer ,ForeignKey("user.id"), primary_key=True),    
    )

package_status = Table(
    "package_status",
    Base.metadata,
    Column("package_id", String(10), ForeignKey("package.id"), primary_key=True),
    Column("status_id", String(10), ForeignKey("status.id"), primary_key=True),
    Column("datetime",DateTime, default= datetime.datetime.now(), nullable= False)
    )


class Package(Base):
    __tablename__= "package"

    id = Column(String(10), primary_key= True)
    price = Column(Numeric(8,2), nullable= False)
    weight = Column(Numeric(6,2), nullable= False)
    sender_name = Column(String(30), nullable= False)
    sender_surname = Column(String(30), nullable= False)
    sender_cap = Column(String(5), nullable= False)
    receiver_name = Column(String(30), nullable= False)
    receiver_surname = Column(String(30), nullable= False)
    receiver_cap = Column(String(5), nullable= False)
    estimated_arrival_date = Column(String(10), nullable= False)

    courier_id = Column(Integer, ForeignKey("courier.id"), nullable= False)
    courier = relationship("Courier",back_populates="packages")

    users = relationship("User",
                        secondary= package_user,
                        back_populates= "packages")

    statuses = relationship("Status",
                            secondary= package_status,
                            back_populates= "packages")

    def __repr__(self):
        return f"[{self.__class__.__tablename__}] --> (id: {self.id}, price: {self.price}, weight: {self.weight}, sender_name: {self.sender_name}, sender_surname: {self.sender_surname}, sender_cap: {self.sender_cap}, receiver_name: {self.receiver_name}, receiver_surname: {self.receiver_surname}, receiver_cap: {self.receiver_cap}, estimated_arrival_date: {self.estimated_arrival_date})"

    def __str__(self):
        return f"{self.id} - {self.price} - {self.weight} - {self.sender_name} - {self.sender_surname} - {self.sender_cap} - {self.receiver_name} - {self.receiver_surname} - {self.receiver_cap} -{self.estimated_arrival_date}"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return other.id == self.id
    
    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "weight": self.weight,
            "sender_name": self.sender_name,
            "sender_surname": self.sender_surname,
            "sender_cap": self.sender_cap,
            "receiver_name": self.receiver_name,
            "receiver_surname": self.receiver_surname,
            "receiver_cap": self.receiver_cap,
            "estimated_arrival_date": self.estimated_arrival_date,
        }



        

