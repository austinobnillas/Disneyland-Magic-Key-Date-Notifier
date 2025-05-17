from fastapi import APIRouter, HTTPException, status, Request, Response, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from datetime import date
from models.user import User
from models.reservation import Reservation
from core.jwt import verify_token
from passlib.hash import bcrypt

router = APIRouter()

class NewReservation(BaseModel):
    magic_key_type: str
    target_date: date

@router.post("/trackreservation")
async def track_reservation(reservation: NewReservation, response: Response, request: Request, db: Session = Depends(get_db)):
    user = verify_token(request.cookies.get("access_token"))

    new_reservation = Reservation(
        user_id = user['user_id'],
        magic_key_type=reservation.magic_key_type,
        target_date=reservation.target_date
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    
    return new_reservation

@router.get("/getreservations")
async def get_reservations(response: Response, request: Request, db: Session = Depends(get_db)):
    user = verify_token(request.cookies.get("access_token"))
    reservations = db.query(Reservation).filter(Reservation.user_id == user['user_id']).all()
    return reservations

@router.delete("/deletereservation/{reservation_id}")
async def delete_reservation(reservation_id: int, response: Response, request: Request, db: Session = Depends(get_db)):
    user = verify_token(request.cookies.get("access_token"))
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id, Reservation.user_id == user['user_id']).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found or not authorized to delete"
        )
    # Delete the reservation
    db.delete(reservation)
    db.commit()
    return {"message": f"Reservation for {reservation.target_date} deleted"}
    
