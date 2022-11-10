from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import ShowAccount, Deposit, Transaction as Transfer, TransferDetails
from sqlalchemy.orm import Session
from database import get_db
from models import Account, User, Transaction as TransactionModel
from typing import List
from fastapi_jwt_auth import AuthJWT


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

# DEPOSITE 
@router.put("/deposit")
def self_deposite( deposit : Deposit, db: Session = Depends(get_db), Authorize:AuthJWT=Depends()):
    print('anna')
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,detail="Invalid Token")

    current_user =Authorize.get_jwt_subject()
    print(current_user)
    user = db.query(User).filter(User.email == current_user).first()
    # print(user)
    # if not user:
    #     return {"Account does not exists"}

    user_account = db.query(Account).filter(Account.user_id == user.id)
    sender_account_no = user_account.first()
    current_balance = user_account.first().balance

    transaction = TransactionModel(sender_id = sender_account_no.account_no, receiver_id = sender_account_no.account_no, transfer_amount = deposit.balance)
    db.add(transaction)
    db.commit()

    deposit.balance += current_balance
    user_account.update(jsonable_encoder(deposit))
    db.commit()

    return {"message" : "transaction successful"}

# TRANSACTION HISTORY

@router.get('/transactions', response_model= List[TransferDetails]) 
def see_all_transaction(db: Session = Depends(get_db), Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,detail="Invalid Token")
    current_user =Authorize.get_jwt_subject()

    # sender = db.query(User).filter(User.email == current_user).first()
    # print(sender.id)
    # all_transaction = db.query(TransactionModel).filter(TransactionModel.sender_id == sender.id).first()

    all_transaction = db.query(TransactionModel).all()
    return all_transaction
# @router.get('/history')
# def all_transaction(db: Session(get_db), Authorize:AuthJWT=Depends()):
#     pass
    # history = db.query(TransactionModel).all()
    # print(history)

@router.put('/transaction')
def other_fund_deposite(transfer : Transfer, db: Session = Depends(get_db), Authorize:AuthJWT=Depends()):
    ## AuthUser -> Senders email
    ## Transaction -> Reciever's account_no, amount_to_be_tranfered

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,detail="Invalid Token")

    current_user =Authorize.get_jwt_subject()
    sender_details = db.query(User).filter(User.email == current_user).first()
    print(sender_details.id)

    pass
    # user2_account = db.query(Account).filter(Account.user_id == sender_details.id)
    # user1_account = db.query(Account).filter(Account.account_no == transaction.account_no).first()

    # if not user2_account:
    #     return {"User does not exists"}
    # user1_balance = user1_account.first().balance
    # user2_balance = user2_account.first().balance

    # transfer_amount = deposite.balance
    # print(transfer_amount)
    # if user1_balance < transfer_amount:
    #     return {"message" : "Not enough balance"}
    # user1_balance -= transfer_amount
    # user2_balance += transfer_amount

    # print(user1_balance)
    # print(user2_balance)

    # deposite.balance = user1_balance
    # print(deposite.balance)
    # user1_account.update(jsonable_encoder(deposite), exclude_unset = True)
    # deposite.balance = user2_balance
    # print(deposite.balance)
    # user2_account.update(jsonable_encoder(deposite), exclude_unset = True)
    # db.commit()
    # return {"Transaction successful"}
