from typing import Any, List, Optional
from uuid import uuid4
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from qdealer import crud, models, schemas
from qdealer.api.dependency import get_current_user, get_db
from qdealer.api.filters import CarAdFilter
from qdealer.utils.aws_service import AWSService
from io import BytesIO
from fastapi_filter import FilterDepends

router = APIRouter()


@router.post("/car-ads", response_model=schemas.CarAd)
def create_ad(
    images: list[UploadFile],
    title: str = Form(),
    brand: str = Form(),
    model: str = Form(),
    year: int = Form(),
    kilometers: Optional[int] = Form(None),
    price: float = Form(),
    db: Session = Depends(get_db),

    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Create new car ad.
    """
    ad_info = schemas.CarAdCreate(title=title, brand=brand, model=model, year=year, kilometers=kilometers, price=price)
    imgs = []
    for image in images:
        if not any(t in image.content_type for t in ('png', 'jpeg', 'jpg')):
            raise HTTPException('Only images are allowed')

        # Save image to disk
        try:
            uuid = str(uuid4())
            img_key = f"{uuid}.{image.filename.split('.')[1]}"
            AWSService.upload_file(image.file.read(), img_key)

        except Exception as e:
            raise HTTPException(500, "Failed to save the image")

        img = crud.image.create_image(db=db, uuid=uuid, img_path=img_key, user_id=current_user.id)
        imgs.append(img)

    ad = crud.car_ad.create_with_owner(db=db, obj_info=ad_info, owner_id=current_user.id, images=imgs)

    return schemas.CarAd.from_orm(ad)


@router.get("/car-ads", response_model=List[schemas.CarAd])
def list_ads(
    *, skip: int = 0, limit: int = 20,
    db: Session = Depends(get_db),
    ad_filter: CarAdFilter = FilterDepends(CarAdFilter),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    list all car ads of current user.
    """

    ads = crud.car_ad.get_multi_filtered(db=db, ad_filter=ad_filter, skip=skip, limit=limit)
    return ads


@router.get("/car-ads/images/{image_uuid}")
def read_image(image_uuid: str,
               db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user),
               ) -> StreamingResponse:

    image = crud.image.get_by_uuid(db, uuid=image_uuid)
    img_binary = AWSService.download_file(image.img_path)
    if img_binary is None:
        raise HTTPException(status_code=404, detail="Image not found")

    image_file = BytesIO(img_binary)
    return StreamingResponse(image_file, media_type=f"image/{image.img_path.split('.')[-1]}")
