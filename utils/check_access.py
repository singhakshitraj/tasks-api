from fastapi import HTTPException,status
from uuid import UUID

def check_access(cur,idx:UUID,user:dict):
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