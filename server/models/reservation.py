from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    magic_key_type = Column(String(50), nullable=False)
    target_date = Column(Date, nullable=False)
    is_available = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="reservations")
