from database import get_db
from models.reservation import Reservation

def compare_dates(data, key):
    db = next(get_db())
    reservations = db.query(Reservation).filter(Reservation.magic_key_type == key).all()
    print(key)
    print(reservations)


