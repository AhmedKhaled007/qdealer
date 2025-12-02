from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from fastapi import Query
from carmarket.models import CarAd


class CarAdFilter(Filter):
    search: Optional[str] = Field(Query(None, description="search for this word in title, brand, model"))

    year__gt: Optional[int]
    year__lt: Optional[int]

    kilometers__gt: Optional[int]
    kilometers__lt: Optional[int]

    price__gt: Optional[float]
    price__lt: Optional[float]

    class Constants(Filter.Constants):
        model = CarAd
        search_model_fields = ["title", "brand", "model"]
