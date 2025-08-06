from fastapi import FastAPI,status
from routers import auth,project

app=FastAPI()

app.include_router(auth.router)
app.include_router(project.router)

@app.get('/',status_code=status.HTTP_200_OK)
def test():
    return {'message':"Working"}

