from sqlalchemy import Column, Integer, String, Numeric
from .database import Base

# Define Address class inheriting from Base
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    place_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    lat = Column(Numeric(9, 6), nullable=False)
    long = Column(Numeric(9, 6), nullable=False)