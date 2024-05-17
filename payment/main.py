from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv
from fastapi.background import BackgroundTasks
from starlette.requests import Request
import requests, time, os

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS"),
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    password=os.environ.get("REDIS_PASSWORD"),
    decode_responses=True,
)

class Order(HashModel):
  product_id: str
  price: float
  fee: float
  total: float
  quantity: int
  status: str

  class Meta:
    database=redis

@app.get('/orders/{pk}')
def get(pk: str):
  return Order.get(pk)

