from fastapi import APIRouter, HTTPException, status, Request, Response, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, EmailStr
from database import get_db
from models.user import User
from core.jwt import create_access_token, verify_token
from passlib.hash import bcrypt

router = APIRouter()

class RegisterUser(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=3)
    confirm_password: str

class RegisteredUser(BaseModel):
    email: EmailStr
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

@router.post('/register')
async def register(user: RegisterUser, response: Response, db: Session = Depends(get_db)):
    try: 
        if user.password != user.confirm_password:
            raise HTTPException(
                status_code=400,
                detail="Passwords do not match."
            )
        # Check if the email is already registered
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered."
            )
        # Hash the password
        hashed_password = bcrypt.hash(user.password)
        # Create new user
        new_user = User(email=user.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_access_token({"user_id": new_user.id})

        # Set JWT as a cookie
        response.set_cookie(key="access_token", value=token, httponly=True)
        return {
            "message": "Registration successful!",
            "user": {
                "id": new_user.id,
                "email": new_user.email
            }
        }
    except Exception as e:
        print(f"Error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.post('/login',
    summary="Login",
    description="""
    This endpoint allows a user to log in by providing their email and password.  
    Upon successful login, a JWT token is generated and set as a cookie.
    """,
    responses={
        200: {"description": "Login successful, JWT token set in cookie."},
        401: {"description": "Invalid email or password."}
    })
async def login(user: LoginUser, response: Response, db: Session = Depends(get_db)):
    account = db.query(User).filter(User.email == user.email).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    is_valid_password = bcrypt.verify(user.password, account.password)
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    token = create_access_token({"user_id": account.id})
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {
        "message": "Login successful",
        "user": {
            "id": account.id,
            "email": account.email,
        }
    }
@router.post('/logout')
async def logout(response: Response):
    # Clear the cookie by setting it to an empty string and expiring it immediately
    response.delete_cookie(key="access_token")
    return {
        "message": "Successfully logged out."
    }

@router.get('/test')
async def register(response: Response, request: Request):
    verified_token = verify_token(request.cookies.get("access_token"))
    return {"message": "this is test", "token": verified_token}