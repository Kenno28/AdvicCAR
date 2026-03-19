from pydantic import BaseModel
from typing import Optional
from models.enum import Makes, Models, FuelType, MotorType

class Car(BaseModel):
    '''
    Class to have a structured way to work with the cars
    '''

    make:Makes
    model:Models
    km:int
    price:float
    motor:MotorType
    year_of_manufacture:int
    damaged:bool
    fuel_type:FuelType 
    description_listing: Optional[str] = None
    color: Optional[str] = None

