from fastapi import HTTPException,status,APIRouter,Path,Depends
from fastapi.responses import JSONResponse
from routers.auth import connect_to_db
from uuid import UUID
from utils.check_access import check_access
from utils.current_user import get_current_user
from validation_models.task import CreateTaskValidation,UpdateTaskValidation

router=APIRouter()

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_task(data:CreateTaskValidation,idx:UUID=Path(...),user=Depends(get_current_user),connection=Depends(connect_to_db)):
    with connection.cursor() as cur:
        cur.execute('''
            SELECT email FROM users
            WHERE username=%s
        ''',(data.assigned_to,)
        )
        assigned_to=cur.fetchone()
        if assigned_to is None:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='No User found with username provided in assigned_to')
        email=assigned_to['email']
        cur.execute('''
            INSERT INTO tasks(name,project_id,priority,due_date,description,assigned_to)
            VALUES(%s,%s,%s,%s,%s,%s)
            RETURNING name,assigned_to
        ''',(data.name,str(idx),data.priority,data.due_date,data.description,data.assigned_to)      
        )
        new_task=cur.fetchone()
        if new_task is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Task not Created!')
        return {
            'messgae':'Task Added',
            'task':{
                'name':new_task.get('name'),
                'assigned_to':new_task.get('assigned_to')
            }
        }
        
@router.get('/',status_code=status.HTTP_200_OK)
def get_tasks(status:bool=False,limit:int=20,offset:int=0,idx:UUID=Path(...),connection=Depends(connect_to_db),user=Depends(get_current_user)):
    with connection.cursor() as cur:
        cur.execute('''
            SELECT name,description,isdone,priority,due_date,assigned_to,task_id
            FROM tasks
            WHERE project_id=%s AND isdone=%s
            ORDER BY priority DESC,due_date
            LIMIT %s OFFSET %s
        ''',(str(idx),status,limit,offset)
        )
        tasks=cur.fetchall()
        return {
            'messgae':'Fetched Successfully!',
            'data':tasks
        }
        
@router.get('/{task_id}',status_code=status.HTTP_200_OK)
def get_task_details(task_id:str,idx:UUID=Path(...),connection=Depends(connect_to_db),user=Depends(get_current_user)):
    with connection.cursor() as cur:
        cur.execute('''
            SELECT T.name as task_name,T.assigned_to,P.title as project_name,P.owner,T.isdone,T.priority,T.due_date
            FROM project P 
            INNER JOIN tasks T 
            ON P.project_id=T.project_id
            WHERE T.task_id=%s
        ''',(task_id,)
        )
        task=cur.fetchone()
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Task not Found!')
        return {
            'message':"Fetched Successfully!",
            'data':task
        }

@router.patch('/{task_id}',status_code=status.HTTP_202_ACCEPTED)
def update_task_details(task_id:UUID,data:UpdateTaskValidation,user=Depends(get_current_user),connection=Depends(connect_to_db)):
    with connection.cursor() as cur:
        cur.execute('''
            UPDATE tasks
            SET name=COALESCE(%s,name),
            isdone=COALESCE(%s,isdone),
            priority=COALESCE(%s,priority),
            due_date=COALESCE(%s,due_date),
            description=COALESCE(%s,description),
            assigned_to=COALESCE(%s,assigned_to)
            WHERE task_id=%s
            returning task_id
        ''',(data.name,data.isdone,data.priority,data.due_date,data.description,data.assigned_to,str(task_id))
        )
        updated_task=cur.fetchone()
        if updated_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Unable to update')
        return {
            'message':"Updated Successfull!",
            'task-id':updated_task
        }
        
@router.delete('/{task_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:str,connection=Depends(connect_to_db),user=Depends(get_current_user)):
    with connection.cursor() as cur:
        cur.execute('''
            DELETE FROM tasks
            WHERE task_id=%s
            RETURNING name
        ''',(str(task_id),)            
        )
        deleted_project=cur.fetchone()
        if deleted_project is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Unable to Delete Task!')     