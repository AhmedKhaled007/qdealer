from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from carmarket.crud.base import CRUDBase
from carmarket.models import CarAd, Image
from carmarket.schemas import CarAdCreate


class CRUDCarAd(CRUDBase[CarAd, CarAdCreate]):
    def create_with_owner(
        self, db: Session, *, obj_info: CarAdCreate, owner_id: int, images: List[Image]
    ) -> CarAd:

        db_obj = self.model(**obj_info.dict(exclude={"images_uuid"}), owner_id=owner_id, images=images)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_filtered(
        self, db: Session, *, ad_filter, skip: int = 0, limit: int = 100
    ) -> List[CarAd]:
        qry = select(self.model)
        qry = ad_filter.filter(qry)
        qry = qry.offset(skip).limit(limit)
        return (
            db.execute(qry).scalars().all()
        )


car_ad = CRUDCarAd(CarAd)
