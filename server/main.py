from fastapi import FastAPI
from database import engine, Base
from models import user, reservation
from controllers import users, reservations

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])


@app.get("/")
async def root():
    return {"message": "Hello World"}