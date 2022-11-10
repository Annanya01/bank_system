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

class TransferDetails(BaseModel):
    sender_id : int
    receiver_id : int
    transfer_amount: float

    class Config:
        orm_mode = True

class ShowAccount(BaseModel):
    user_id : int
    account_no: int
    balance: float

    class Config:
        orm_mode = True

class Settings(BaseModel):
    authjwt_secret_key:str='beb6e688aca5a8bc26c9e34a850b78bc682a2eba8ca8157e905c88dc0ec3d002'

class LoginModel(BaseModel):
    email:str
    password:str

class Deposit(BaseModel):
    balance: float

class Transaction(BaseModel):
    account_no : str
    balance : float



class ResponseModel(BaseModel):
    detail: str

