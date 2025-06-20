from pydantic import BaseModel, condecimal

# Schema for creating a new address entry
class AddressCreate(BaseModel):
    place_name: str
    city: str
    lat: condecimal(max_digits=9, decimal_places=6)
    long: condecimal(max_digits=9, decimal_places=6)

# Schema for response, includes the address ID
class AddressResponse(AddressCreate):
    id: int

    class Config:
        orm_mode = True