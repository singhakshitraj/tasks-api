from fastapi import APIRouter,Depends,HTTPException,status
from validation_models.login import AuthValidation
import jwt
from datetime import datetime,timedelta
import os
from passlib.context import CryptContext
from db.connection import connect_to_db
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

router=APIRouter(
    prefix='/auth',
    tags=['Authentication']
)
context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str):
    return context.hash(password)

def verify_password(plain_password,hashed_password):
    return context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    data.update({'expires':str(datetime.now()+timedelta(minutes=90))})
    return jwt.encode(
        data,
        key=os.environ.get('SECRET_KEY'),
        algorithm="HS256",
    )

def get_current_user(token=Depends(oauth2_bearer)):
    load_dotenv()
    data=jwt.decode(token,key=os.environ.get('SECRET_KEY'),algorithms=[os.environ.get('ALGORITHM')])
    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Incorrect Token!')
    elif  data['expires']<=str(datetime.now()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Token Expired!')
    return {"username": data['username']}

@router.post('/register')
def _register(user:AuthValidation,connection=Depends(connect_to_db)):
    with connection.cursor() as cur:
        cur.execute('''
            SELECT * FROM USERS
            WHERE username=%s
        ''',(user.username,)
        )
        n_user=cur.fetchone()
        if n_user is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User Already Exists. Try Logging in.')
        cur.execute('''
            INSERT INTO USERS(username,password)
            VALUES (%s,%s)
            RETURNING *
        ''',(user.username,hash_password(user.password))
        )
        new_user=cur.fetchone()
        if new_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to create new User')
        token=create_access_token({"username":user.username,"password":hash_password(user.password)})
        return {
            "Username":user.username,
            "Access-Token":token,
            "Token-Type":"bearer"
        }
        
@router.post('/login')
def _login(user:AuthValidation,connection=Depends(connect_to_db)):
    with connection.cursor() as cur:
        cur.execute('''
            SELECT * FROM USERS
            WHERE username=%s
        ''',(user.username,)
        )
        db_user=cur.fetchone()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='No User Found. Check details again.')
        if not verify_password(user.password,db_user['password']):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect Cridentials')
        token=create_access_token({"username":user.username,"password":hash_password(user.password)})
        return {
            "Username":user.username,
            "Access-Token":token,
            "Token-Type":"bearer"
        }