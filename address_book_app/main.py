from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import AddressCreate, AddressResponse
from database import SessionLocal, engine
import models
import uvicorn
from math import radians, cos, sin, asin, sqrt

# Create the database
models.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(title="Address Book API")

# Helper function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Calculate distance between two coordinates using the Haversine formula
def calculate_distance_km(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

# --- API Endpoints ---

# Create a new address entry
@app.post("/addressBook", response_model=AddressResponse)
def create_address_view(address: AddressCreate, db: Session = Depends(get_db)):
    # Validate latitude and longitude ranges
    if not (-90 <= float(address.lat) <= 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
    if not (-180 <= float(address.long) <= 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")

    # Save address to the database
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

# Get all stored addresses
@app.get("/addressBook", response_model=list[AddressResponse])
def read_addresses(db: Session = Depends(get_db)):
    return db.query(models.Address).all()

# Update an existing address by ID
@app.put("/addressBook/{address_id}", response_model=AddressResponse)
def update_address_view(address_id: int, address: AddressCreate, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Validate latitude and longitude ranges
    if not (-90 <= float(address.lat) <= 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
    if not (-180 <= float(address.long) <= 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")

    # Update each field
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address

# Delete an address by ID
@app.delete("/addressBook/{address_id}")
def delete_address_view(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(db_address)
    db.commit()
    return {"detail": "Address deleted successfully"}

# Search addresses within a certain distance of given coordinates
@app.get("/addressBook/search", response_model=list[AddressResponse])
def search_by_location(lat: float, long: float, distance_km: float, db: Session = Depends(get_db)):
    # Validate input coordinates
    if not (-90 <= float(lat) <= 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
    if not (-180 <= float(long) <= 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")

    # Filter addresses based on distance using Haversine
    addresses = db.query(models.Address).all()
    return [addr for addr in addresses if calculate_distance_km(lat, long, float(addr.lat), float(addr.long)) <= distance_km]

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)