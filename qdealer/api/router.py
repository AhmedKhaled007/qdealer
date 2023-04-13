from fastapi import APIRouter

from qdealer.api.endpoints import car_ads, login

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(car_ads.router, tags=["ads"])
