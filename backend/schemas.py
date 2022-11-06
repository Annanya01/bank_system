from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class CreateToken(UserCreate) :
    email: EmailStr
    password: str

class ShowUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class ShowAccount(BaseModel):
    user_id : int
    account_no: int
    balance: float

    class Config:
        orm_mode = True

class Settings(BaseModel):
    authjwt_secret_key:str='ea89de0d23fa63864faa983dd60c616769f5b165c255e8fe9593d845e2891cec'

class LoginModel(BaseModel):
    email:str
    password:str

class Deposite(BaseModel):
    balance: float

class Transaction(BaseModel):
    user_id : int
    balance : float



