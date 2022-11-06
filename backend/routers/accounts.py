from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from schemas import ShowAccount, Deposite, Transaction
from sqlalchemy.orm import Session
from database import get_db
from models import Account
from typing import List

router = APIRouter()

@router.get('/accounts/all', response_model = List[ShowAccount])
def retrive_all_accounts(db: Session = Depends(get_db)):
    print('annanya')
    all_accounts = db.query(Account).all()
    print('afss')
    return all_accounts

@router.get('/accounts/{id}', response_model=ShowAccount)
def get_account_by_id(id:int, db:Session=Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == id).first() # without first(), will return query
    if not account:
        return {"message" : "Account does not exists"}
    return account

@router.put("/deposits/{id}")
def self_deposite(id : int, deposite : Deposite ,db: Session = Depends(get_db)):
    user_account = db.query(Account).filter(Account.user_id == id)
    if not user_account:
        return {"Account does not exists"}
        
    current_balance = user_account.first().balance
    print(current_balance)
    deposite.balance += current_balance
    user_account.update(jsonable_encoder(deposite))
    db.commit()
    return {"message" : "transaction successful"}

@router.patch('/transaction/{id}')
def transaction(id : int, deposite : Deposite, transaction : Transaction, db: Session = Depends(get_db)):
    user_id = transaction.user_id
    user2_account = db.query(Account).filter(Account.user_id == id)
    user1_account = db.query(Account).filter(Account.user_id == user_id)

    if not user2_account:
        return {"User does not exists"}
    user1_balance = user1_account.first().balance
    user2_balance = user2_account.first().balance
    
    transfer_amount = deposite.balance
    print(transfer_amount)
    if user1_balance < transfer_amount:
        return {"message" : "Not enough balance"}
    user1_balance -= transfer_amount
    user2_balance += transfer_amount

    print(user1_balance)
    print(user2_balance)

    deposite.balance = user1_balance
    print(deposite.balance)
    user1_account.update(jsonable_encoder(deposite), exclude_unset = True)
    deposite.balance = user2_balance
    print(deposite.balance)
    user2_account.update(jsonable_encoder(deposite), exclude_unset = True)
    db.commit()
    return {"Transaction successful"}
