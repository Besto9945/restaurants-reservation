from fastapi import FastAPI, HTTPException
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
    query =  collection.find({"table_number": table})
    info = {}
    for i in query:
        info[i["name"]] = "time: " + str(i["time"])
    if len(info) == 0:
        return {"result": "No one reserve this table."}
    return {"reservation": info}

@app.post("/reservation")
def reserve(reservation : Reservation):
    pass

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    pass

