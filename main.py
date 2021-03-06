from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from pydantic import BaseModel

class Reservation(BaseModel):
    name : Optional[str] = None
    time: Optional[int] = None
    table_number: Optional[int] = None
    
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
        obj = Reservation()
        obj.name = i["name"]
        obj.time = i["time"]
        obj.table_number = i["table_number"]
        data[count] = jsonable_encoder(obj)
        count += 1
    if len(data) == 0:
        raise HTTPException(404, "Can't find anyone who reserved by this name.")
    else:
        return {"result": data}

@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    query =  collection.find({"table_number": table}, {"_id":0})
    data = {}
    count = 1
    for i in query:
        obj = Reservation()
        obj.name = i["name"]
        obj.time = i["time"]
        obj.table_number = i["table_number"]
        data[count] = jsonable_encoder(obj)
        count += 1
    if len(data) == 0:
        raise HTTPException(404, "No one reserve this table.")
    else:
        return {"result": data}

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
    query = collection.find({"table_number": reservation.table_number})
    for i in query:
        if i["time"] <= reservation.time < i["time"]+1:
            return {"result": "The new reservation is not allowed."}
    find_by = {"name": reservation.name, "table_number": reservation.table_number}
    new_value = {"$set": {"time": reservation.time}}
    collection.update_one(find_by, new_value)
    return {"result": "The new reservation is complete!"}

@app.delete("/reservation/delete/{name}/{table_number}/")
def cancel_reservation(name: str, table_number: int):
    query = collection.find_one({"name": name, "table_number": table_number})
    if query is None:
        raise HTTPException(404, "Can't find anyone who reserved by this name and this table.")
    collection.delete_one({"name": name, "table_number": table_number})
    return {"result": "Cancel the reservation complete!"}

