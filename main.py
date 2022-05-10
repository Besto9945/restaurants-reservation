from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

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
    query = collection.find({"name": name})
    info = {}
    for i in query:
        info["table "+ str(i["table_number"])] = "time: " + str(i["time"])
    if len(info) == 0:
        return {"result": "No reservation by this name."}
    return {"reservation": info}


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

