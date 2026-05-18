from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional

class Patient(BaseModel):
    name: str
    age : int
    weight :float = Field(..., gt=0, lt=100)
    married:bool=False
    email:EmailStr
    linkedin_url:AnyUrl
    allergies :Optional[List[str]]=None
    contact:Dict[str,str]

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)

patienta = {'name':'sourav', 'age':23, 'weight':34.5,'allergies':['pollen','dust','peanuts'],'contact':{'email':'xyz@abc.com','phone':'4568456'}}

patient1 = Patient(**patienta)


