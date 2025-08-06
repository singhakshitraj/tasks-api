from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from db.connection import connect_to_db
from utils.password import hash_password,verify_password
from utils.current_user import create_access_token
router=APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/register')
def _register(user:OAuth2PasswordRequestForm=Depends(),connection=Depends(connect_to_db)):
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
def _login(user:OAuth2PasswordRequestForm=Depends(),connection=Depends(connect_to_db)):
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