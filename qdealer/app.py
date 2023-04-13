from fastapi import FastAPI
from qdealer.utils.config import settings
from qdealer.api import router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


# # Set all CORS enabled origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return "Hello World!"


app.include_router(router.api_router)
