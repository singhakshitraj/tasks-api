from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from datetime import datetime,timedelta
import jwt,os

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data:dict):
    data.update({'expires':str(datetime.now()+timedelta(minutes=90))})
    return jwt.encode(
        data,
        key=os.environ.get('SECRET_KEY')or"",
        algorithm="HS256",
    )

def get_current_user(token=Depends(oauth2_bearer)):
    load_dotenv()
    data=jwt.decode(token,key=os.environ.get('SECRET_KEY')or"",algorithms=[os.environ.get('ALGORITHM')or""])
    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Incorrect Token!')
    elif data['expires']<=str(datetime.now()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Token Expired!')
    return {"username": data['username']}