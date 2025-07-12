import re
from pydantic import BaseModel,Field,field_validator


class DateTimeModel(BaseModel):
    date:str=Field(description="Properly formatted date and time , Format: DD-MM-YYYY HH:MM",pattern=r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$')

    @field_validator("date")
    def check_format_date(cls,v):
        if not re.match(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$',v):
            raise ValueError("The date and time should be in proper format - 'DD-MM-YYYY HH:MM' ")
        return v


class DateModel(BaseModel):
    date:str=Field(description="Properly formatted date, Format - 'DD-MM-YY' ",pattern=r'^\d{2}-\d{2}-\d{4}$')

    @field_validator("date")
    def check_format_date(cls,v):
        if not re.match(r'^\d{2}-\d{2}-\d{4}$',v):
            raise ValueError("The dat must be in proper format-'DD-MM-YYYY' ")
        return v

class IdentificationNumberModel(BaseModel):
    id:int=Field(description="Identification Number: (6-7 digits long)",ge=7,le=8)
    
    @field_validator("id")
    def validate_the_field(cls,v):
        if not re.match(r'^\d{7,8}$',str(v)):
            raise ValueError("Id should be of 7 or 8 digit number")

        return v
        
            

