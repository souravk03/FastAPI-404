from fastapi import FastAPI,Path,HTTPException,Query
import json
app = FastAPI()

@app.get('/')
def hello():
    return {"message":"Hello how are you doing today??"}

@app.get('/about')
def about():
    print("!Hello World")
    return {"message":"FastApi is easy to learn and fast as its name suggests"}


def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='Patient ID from the Database', example='P001' )):
    data = load_data()
    print("Succes Loading")
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(404, detail=' 404 patient not found')


@app.get('/sort')
def sort_patient(sort_by : str =Query(..., description='sort the patient on the basis of name and Age'),
                 Order :str = Query(..., description='sort in asc or desc order')):
    fields =['name','age']

    if sort_by not in fields:
        raise HTTPException(400, detail='Enter any of the valid field {field}')
    
    if Order not in ['asc','desc']:
        raise HTTPException(400, detail='specify the asc or desc order')
    
    data =load_data()

    sort_order = True if Order=='desc' else False

    sorted_data = sorted(data.values() , keys= lambda x:x.get(sort_by,0) ,reverse=sort_order)

    return sorted_data