from carmarket.api.dependency import get_db, get_current_user
from carmarket.app import app
from fastapi.testclient import TestClient
from carmarket.models import User, CarAd
from carmarket.schemas import TokenPayload
import io
client = TestClient(app)


def fake_user_info():
    return TokenPayload(sub=1)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello World!"


def test_create_car_ad__create_ad_and_return_200(monkeypatch, db_dependency, session):
    # SETUP
    session.add(User(id=1, email="test@example.com", hashed_password="password", phone_number="1234567890"))
    session.commit()

    app.dependency_overrides[get_db] = db_dependency
    app.dependency_overrides[get_current_user] = lambda: User(id=1)

    monkeypatch.setattr("carmarket.utils.aws_service.AWSService.upload_file", lambda *args, **kwargs: None)
    image = io.BytesIO(b"some file data")
    image.name = "test.jpg"

    resp = client.post("/car-ads", data={"title": "test", "brand": "test", "model": "test", "year": 1990, "price": 100},
                       files={"images": image})

    assert resp.json()['model'] == "test"
    assert resp.json()['brand'] == "test"
    assert resp.json()['year'] == 1990
    assert resp.json()['title'] == "test"
    assert resp.json()['price'] == 100

    assert resp.status_code == 200

    assert session.query(CarAd).count() == 1

    app.dependency_overrides = {}


def test_list_car_ads__return_200(db_dependency, session):
    session.add(User(id=1, email="test@example.com", hashed_password="password", phone_number="1234567890"))
    session.add(CarAd(id=1, title="test", brand="test", model="test", year=2020, price=100, owner_id=1))
    session.add(CarAd(id=2, title="test1", brand="test1", model="test1", year=2021, price=200, owner_id=1))
    session.commit()

    app.dependency_overrides[get_db] = db_dependency
    app.dependency_overrides[get_current_user] = lambda: User(id=1)

    resp = client.get("/car-ads")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    app.dependency_overrides = {}


def test_create_user_return_200(session, db_dependency):
    app.dependency_overrides[get_db] = db_dependency
    resp = client.post("/register", json={"phone_number": "+201111051876", "password": "test_password"})
    assert resp.status_code == 200
    assert resp.json()['email'] == None
    assert resp.json()['phone_number'] == "+201111051876"

    assert session.query(User).first().hashed_password != "test_password"


def test_login_with_phone_number_return_200(session, db_dependency):
    app.dependency_overrides[get_db] = db_dependency
    client.post("/register", json={"phone_number": "+201111051876", "password": "test_password"})

    resp = client.post("/login", json={"phone_number": "+201111051876", "password": "test_password"})
    assert resp.status_code == 200
    assert resp.json()['access_token'] is not None
