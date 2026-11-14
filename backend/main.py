from fastapi import FastAPI, Body, Header, HTTPException
from datetime import datetime
from pydantic import BaseModel
import functions

app = FastAPI()

app.add_middleware, CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Newpackage(BaseModel):
    name: str
    destination: str
    weight: float
    arrival_date: datetime
    status: str

class Dispatch(BaseModel):
    destination: str
    vehicle: str
    status: str
    
class Updatepackage(BaseModel):
    name: str
    destination: str
    weight: float 
    arrival_date: datetime 
    status: str


@app.post("/packages")
def register_package(package:Newpackage, token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    result = functions.register_package(name=package.name, destination=package.destination, weight=package.weight, arrival_date=package.arrival_date, status=package.status)
    return result

@app.get("/packages/status")
def get_statistics(token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = functions.get_summary()
    return result

@app.get("/packages/{id}")
def get_package(id: int,token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = functions.get_one_package(id=id)
    return result

@app.patch("/packages/{id}")
def update_package(id: int, package: Updatepackage, token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = functions.update_package(id=id, name=package.name, destination=package.destination, weight=package.weight, arrival_date=package.arrival_date, status=package.status)
    return result

@app.delete("/packages/{id}")
def delete_package(id: int,token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = functions.delete_package(id=id)
    return result

@app.get("/packages")
def search_packages(destination: str = None, status: str = None, arrival_date: str = None, token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = functions.get_all_packages(destination, status, arrival_date)
    return result

@app.get("/dispatch_batches")
def get_dispatch_batches(destination: str = None, vehicle_number: str = None, status: str = None,token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = functions.get_all_dispatches(destination, vehicle_number, status)
    return result


@app.post("/dispatch_batches")
def create_dispatch_batch(package: Dispatch, token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")    
    result = functions.add_dispatch(destination=package.destination, vehicle=package.vehicle, status=package.status)
    return result

@app.post("/login")
def login(username= Body(), password= Body()):
    token = functions.verify_login(username=username, password=password)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return token

@app.post("/refresh")
def refresh_token(refresh_token=Header(None)):
    username=functions.verify_token(token=refresh_token, token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    access_token = functions.create_token(username=username, token_type="access")
    return {"access_token": access_token}


@app.post("/register")
def register_user(username = Body(), password = Body()):
    result = functions.register_user(username=username, password=password)
    if result:
        return {"message": "User registered successfully"}
    raise HTTPException(status_code=400, detail="User already exists")