from pydantic import BaseModel

class AuthValidation(BaseModel):
    username:str
    password:str