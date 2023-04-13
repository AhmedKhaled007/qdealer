from typing import List
from sqlalchemy.orm import Session

from qdealer.crud.base import CRUDBase
from qdealer.models import Image
from qdealer.schemas import Image as ImageSchema


class CRUDImage(CRUDBase[Image, ImageSchema]):
    def create_image(
        self, db: Session, *, uuid: str, img_path: str, user_id: int
    ) -> Image:

        db_obj = self.model(uuid=uuid, img_path=img_path, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_list_uuid(
        self, db: Session, *, uuids: List[str],
    ) -> List[Image]:
        return db.query(self.model).filter(Image.uuid.in_(uuids)).all()

    def get_by_uuid(
        self, db: Session, *, uuid: str
    ) -> Image:
        return db.query(self.model).filter(Image.uuid == uuid).one_or_none()


image = CRUDImage(Image)
