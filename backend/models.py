from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True)
    first_name = Column(String, nullable= False)
    last_name = Column(String, nullable= False)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)

    accounts = relationship("Account", back_populates = "admin")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer,primary_key = True, index=True)
    account_no = Column(Integer, unique = True, nullable = False)
    balance = Column(Float, nullable = False, default=1000)
    user_id =  Column(Integer, ForeignKey("users.id"))

    admin = relationship("User",back_populates="accounts")

class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key = True, index = True)
    sender_id = Column(Integer, ForeignKey("accounts.id"))
    receiver_id = Column(Integer, ForeignKey("accounts.id"), nullable = True)
    transfer_amount = Column(Float, nullable = False)



