from fastapi import FastAPI
from database import engine, Base
from models import user, reservation
from controllers import users, reservations

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Magic Key Notifier API",
    description="API for monitoring and notifying Disneyland Magic Key reservation availability.",
    version="1.0.0",
    contact={
        "name": "Austin Obnillas",
        "email": "austin@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    )

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(reservations.router, prefix="/api/reservations", tags=["Reservations"])

@app.get("/")
async def root():
    return {"message": "Hello World"}