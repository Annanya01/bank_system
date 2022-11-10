import os as _os

import dotenv as _dotenv
import jwt as _jwt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import email_validator as _email_check
import fastapi as _fastapi
import fastapi.security as _security

import database as _database
import schemas as _schemas
import models as _models
import random

oauth2schema = _security.OAuth2PasswordBearer("/api/token")

async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

async def create_user(user: _schemas.UserCreate, db: _orm.Session):

    account_no = random.randint(100000000000,999999999999)

    try:
        valid = _email_check.validate_email(email=user.email)

        email = valid.email
    except _email_check.EmailNotValidError:
        raise _fastapi.HTTPException(status_code=404, detail="Please enter a valid email")

    user_obj = _models.User(first_name = user.first_name, last_name = user.last_name, email=email, hashed_password=_hash.bcrypt.hash(user.password))

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    account_obj = _models.Account(account_no = account_no, user_id = user_obj.id)
    db.add(account_obj)
    db.commit()
    db.refresh(account_obj)

    return user_obj

async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email=email, db=db)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user

async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    user_dict = user_obj.dict()
    del user_dict["date_created"]

    token = _jwt.encode(user_dict, )

    return dict(access_token=token, token_type="bearer")
