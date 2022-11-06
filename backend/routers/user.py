from fastapi import APIRouter
from schemas import ShowUser, UserCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from database import get_db
from models import User, Account
from typing import List
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash,check_password_hash

import random

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# def func(user1:LoginModel,access_token:str, db: Session = Depends(get_db)):
#     user_to_update = db.query(User).filter(User.email==user1.email).first()
#     user_to_update.token= access_token
#     db.commit()

@router.get('/')
def hello():
    return {'message' : 'hola'}

@router.post('/users', status_code = 201, response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        account_no = random.randint(10000,99999)

        new_user = User(first_name = user.first_name, last_name = user.last_name, email = user.email, password = generate_password_hash(user.password))
        print(account_no)
        print(user.first_name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        accounts = Account(account_no = account_no, user_id = new_user.id)
        db.add(accounts)
        db.commit()
        db.refresh(accounts)

        return new_user
    except IntegrityError :
        return {"msg": "email already exists"}

@router.get('/users/all', response_model= List[ShowUser])
def get_all_users(db:Session=Depends(get_db)):
    user = db.query(User).all()
    return user

@router.get('/users/{id}', response_model=ShowUser)
def get_user_by_id(id:int, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, details = f"item {id} does not exists")
    return user