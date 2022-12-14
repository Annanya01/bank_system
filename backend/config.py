import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Settings:

    SECRET_KEY : str = os.getenv('SECRET_KEY')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 10

settings = Settings()