import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from api import cars
from .api.database import database, engine
# from api.models import Car
from .api import carbrands, models, carmodels
from fastapi.staticfiles import StaticFiles
# models.Base.metadata.drop_all(bind=engine,tables=[models.CarBrand, models.CarModel])
# models.Base.metadata._remove_table("carbrands","carbrands")
# models.Base.metadata._remove_table("carmodels", "carmodels")
from fastapi_pagination import Page, add_pagination, paginate
models.Base.metadata.create_all(bind=engine, checkfirst=True)
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/app/api/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:3000",
    "*"
]
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)
#
@app.on_event("startup")
async def startup():
    await database.connect()
    # os.delay(1)
    # print(nam)
    # await database.create_tables([models.Car, models.CarModel])
    # database.db.close()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# app.include_router(ping.router)
app.include_router(carbrands.router, prefix="/carbrands", tags=["carbrands"])
app.include_router(carmodels.router, prefix="/carmodels", tags=["carmodels"])

add_pagination(app)