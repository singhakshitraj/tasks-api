from fastapi import APIRouter,Depends,HTTPException,status
from .auth import get_current_user
from validation_models.project import ProjectValidation,UpdateProjectValidation
from db.connection import connect_to_db
from uuid import UUID
from fastapi.responses import JSONResponse

router=APIRouter(
    prefix='/project'
)

def check_access(cur:any,idx:UUID,user:dict):
    cur.execute('''
        SELECT owner FROM project
        WHERE project_id=%s
    ''',(str(idx),)
    )
    data=cur.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Project with that id does not exist.')
    if data['owner']!=user['username']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have access to this resource.")
    return True

@router.post('',status_code=status.HTTP_201_CREATED)
def create_project(data:ProjectValidation,user:dict=Depends(get_current_user),connection=Depends(connect_to_db)):
    with connection.cursor() as cur:
        cur.execute('''
            INSERT INTO project(title,description,owner)
            VALUES(%s,%s,%s)        
            RETURNING *
        ''',(data.title,data.description or f"New Project By {user.get('username')}",user.get('username'))
        )
        new_project=cur.fetchone()
        if new_project is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to add data in DB')
        return {
            'message':'Successfully Created!',
            'title':new_project.get('title'),
            'user': user.get('username')
        }
        
@router.get('',status_code=status.HTTP_200_OK)
def get_project(user:dict=Depends(get_current_user),connection=Depends(connect_to_db)):
    with connection.cursor() as cur:
        cur.execute('''
            SELECT * FROM project
            WHERE owner=%s
        ''',(user['username'],)
        )
        data=cur.fetchall()
        return {
            'message':'Successfully Fetched!',
            'data':data
        }
        
@router.get('/{idx}')
def project_details(idx:UUID,user:dict=Depends(get_current_user),connection=Depends(connect_to_db)):
    with connection.cursor() as cur:
        try:
            check_access(cur=cur,idx=idx,user=user)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        cur.execute('''
            SELECT P.title as proj_title
            ,P.description as proj_desc
            ,T.name as task_name
            ,T.description as task_desc
            ,T.assigned_to
            FROM project P 
            INNER JOIN tasks T
            ON P.project_id=T.project_id
            WHERE P.project_id=%s
            ORDER BY T.priority,T.due_date
        ''',(str(idx),)
        )
        result=cur.fetchall()
        return {
            'message':'Successfully Fetched!',
            'details': result
        }
        
@router.patch('/{idx}')
def update_project(idx:UUID,data:UpdateProjectValidation,user=Depends(get_current_user),connection=Depends(connect_to_db)):
    with connection.cursor() as cur:
        try:
            check_access(cur=cur,idx=idx,user=user)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        cur.execute('''
            UPDATE project
            SET title=COALESCE(%s,title),description=COALESCE(%s,description),isopen=COALESCE(%s,isopen)
            WHERE project_id=%s
            RETURNING title,description,isopen
        ''',(data.title,data.description,data.isopen,str(idx))
        )
        new_data=cur.fetchone()
        if new_data is None:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,detail='Updation Unsuccessful!')
        return {
            'message':'Successfully Updated!',
            'data':{
                'title':new_data.get('title'),
                'description':new_data.get('description'),
                'isOpen':new_data['isopen']
            }
        }
        
@router.delete('/{idx}',status_code=status.HTTP_204_NO_CONTENT)
def delete_project(idx:UUID,user=Depends(get_current_user),connection=Depends(connect_to_db)):
    with connection.cursor() as cur:
        try:
            check_access(cur=cur,idx=idx,user=user)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        cur.execute('''
            DELETE FROM project
            WHERE project_id=%s
            RETURNING title
        ''',(str(idx),)            
        )
        deleted_project=cur.fetchone()
        if delete_project is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Unable to Delete Project!')        