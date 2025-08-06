from pydantic import BaseModel

class ProjectValidation(BaseModel):
    title:str
    description:str|None = None
    
class UpdateProjectValidation(BaseModel):
    title:str|None=None
    description:str|None=None
    isopen:bool|None=None