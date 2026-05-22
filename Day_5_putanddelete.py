from fastapi import FastAPI,Path,Query,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

import json


app = FastAPI()


class Patient(BaseModel):
    id:Annotated[str,Field(...,description='enter the patient id',example='P001')]
    name:Annotated[str,Field(...,description='enter the patient name')]
    city:Annotated[str,Field(...,description='Enter the city patient live in')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Enter the age of the patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,decription='enter the gender of the patient')]
    height:Annotated[float,Field(...,gt=0,description='Enter the height of the patient in m')]
    weight:Annotated[float,Field(...,gt=0,description='Enter the weight of the patient in kg')]


    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return "Underweight"
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return "Overweight"
        else:
            return "Obese"
        
class PatientUpdated(BaseModel):
    name:Annotated[Optional[str],Field(default=None ,description='enter the patient name')]
    city:Annotated[Optional[str],Field(default=None,description='Enter the city patient live in')]
    age:Annotated[Optional[int],Field(default=None,gt=0,lt=120,description='Enter the age of the patient')]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None,decription='enter the gender of the patient')]
    height:Annotated[Optional[float],Field(default=None,gt=0,description='  Enter the height of the patient in m')]
    weight:Annotated[Optional[float],Field(default=None,gt=0,description='Enter the weight of the patient in kg')]





def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.get('/view')
def view_patients():
    data = load_data()
    return data

@app.get('/')
def home():
    return {'message':'Patient management system'}

@app.get('/view/{patient_id}')
def view_patient(patient_id:str=Path(...,description='Enter the patient id to view details')):
    data = load_data()
    for patient in data:
        if patient['id'] == patient_id:
            return patient
    raise HTTPException(status_code=404,detail='Patient not found')

@app.post('/add')
def create_patient(patient: Patient):
    data = load_data()

    # load existing patients and check for duplicate id
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient with this id already exists')
    
    data[patient.id] = patient.model_dump(exclude={'id'})

    save_data(data)

    return JSONResponse(content={'message':'Patient added successfully'},status_code=201)


@app.put('/update/{patient_id}')
def update_patient(patient_id:str, patient_update:PatientUpdated):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value
    
    #existing_patient_info ->pydantic object-> updated bmi and verdict


    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    # pydantic object -> dict

    existing_patient = patient_pydantic_obj.model_dump(exclude={'id'})

    # update the patient info in the data
    data[patient_id] = existing_patient
    save_data(data)

    return JSONResponse(content={'message':'Patient updated successfully'},status_code=200)


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient does not exist')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(content={'message':'Patient Deleted Succesfully'},status_code=200)
