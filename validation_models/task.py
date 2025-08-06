from pydantic import BaseModel
from datetime import date

class CreateTaskValidation(BaseModel):
    name:str
    priority:int
    due_date:date
    description:str|None=None
    assigned_to:str
    
class UpdateTaskValidation(BaseModel):
    name:str|None=None
    isdone:bool|None=None
    priority:int|None=None
    due_date:date|None=None
    description:str|None=None
    assigned_to:str|None=None