from fastapi import FastAPI,status
from routers import auth,project
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.include_router(auth.router)
app.include_router(project.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/',status_code=status.HTTP_200_OK)
def test():
    return {'message':"Working"}

