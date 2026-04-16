from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from src.predict_v1 import predict_api

app = FastAPI()

class FlightDetails(BaseModel):
    AIRLINE: str
    ORIGIN: str
    DEST: str
    FL_DATE: str
    CRS_DEP_TIME: int

@app.get("/")
def index():
    return {"Message":"API is running"}

@app.post("/predict")
def predict(input_data: FlightDetails):
    try:
        results = predict_api(input_data.model_dump())
        return results
    except Exception as e:
        return {"Error":str(e)}
    

