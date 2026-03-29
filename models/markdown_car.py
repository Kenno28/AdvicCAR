from pydantic import BaseModel
from typing import Optional
from car import Car

class Markdown_Car(BaseModel):
    '''
    Class to have a structured way to work with the markdowns
    '''

    title:str
    car:Car
