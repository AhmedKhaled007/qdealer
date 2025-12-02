# CarMarket



A FastAPI-based application for buying and selling cars. It allows users to post car advertisements with images, details (brand, model, year, price, kilometers), and manage their listings.

## Features
- **Car Ads Management**: Users can post, list, and filter car advertisements.
- **Image Upload**: Supports uploading multiple images for each car ad (stored via AWS S3).
- **FastAPI Framework**: High-performance API.
- **Database**: PostgreSQL with SQLAlchemy ORM.
- **Migrations**: Database migrations using Alembic.
- **Dockerized**: Fully containerized setup with Docker Compose.



## Getting Started

### Prerequisites
- Docker & Docker Compose

### Installation & Running
1.  Clone the repository.
2.  Start the application using Docker Compose:
    ```bash
    docker compose up --build
    ```
3.  Access the application:
    -   **API**: `http://localhost:9011`
    -   **Documentation**: `http://localhost:9011/docs`

### Manual Setup (Without Docker)
1.  Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  Configure environment variables (see `docker-compose.yaml` for reference).
3.  Run migrations:
    ```bash
    alembic upgrade head
    ```
4.  Start the server:
    ```bash
    uvicorn qdealer.main:app --reload
    ```
