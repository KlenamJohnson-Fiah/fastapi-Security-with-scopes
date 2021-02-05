from fastapi import FastAPI

from .routers import user
from .database import SessionLocal,engine



app = FastAPI(
    title="Using Scopes for Authorization",
    description="Hopefully by the end of this we can use scopes to control what users can access",

)

app.include_router(user.router)

@app.get("/")
async def root():
    return{"message": "Welcome to this application!"}