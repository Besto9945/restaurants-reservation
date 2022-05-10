from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from pydantic import BaseModel
import json

class Reservation(BaseModel):
    name : str
    time: int
    table_number: int
    
client = MongoClient('mongodb://localhost', 27017)

# TODO fill in database name
db = client["restaurants-reservation"]

# TODO fill in collection name
collection = db["reservation"]

app = FastAPI()


# TODO complete all endpoint.
@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    query = collection.find({"name": name}, {"_id":0})
    data = {}
    count = 1
    for i in query:
        data[count] = {}
        data[count]["name"] = i["name"]
        data[count]["time"] = i["time"]
        data[count]["table_number"] = i["table_number"]
        count += 1
    if len(data) == 0:
        raise HTTPException(404, "Can't find anyone who reserved by this name.")
    return {"result": json.dumps(data)}


@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    query =  collection.find({"table_number": table}, {"_id":0})
    data = {}
    count = 1
    for i in query:
        data[count] = {}
        data[count]["name"] = i["name"]
        data[count]["time"] = i["time"]
        data[count]["table_nubmer"] = i["table_number"]
        count += 1
    if len(data) == 0:
        raise HTTPException(404, "No one reserve this table.")
    # print(json.dumps(data, indent=4))
    return {"result": json.dumps(data)}

@app.post("/reservation/")
def reserve(reservation : Reservation):
    query = collection.find({"table_number": reservation.table_number})
    for i in query:
        if i["time"] <= reservation.time < i["time"]+1:
            return {"result": "Already reserved."}
    collection.insert_one(jsonable_encoder(reservation))
    return {"result": "Reservation complete!"}

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass

@app.delete("/reservation/delete/{name}/{table_number}/")
def cancel_reservation(name: str, table_number : int):
    pass

