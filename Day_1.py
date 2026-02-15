from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message":"Hello World!"}

@app.get("/about")
def about():
    print("Hpw u doin??")
    return {"message":"This is my first Api code, I am learning from the CampusX"}