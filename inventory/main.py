from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

redis = get_redis_connection(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    password=os.environ.get("REDIS_PASSWORD"),
    decode_responses=True,
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get('/products')
def all():
    return Product.all_pks()

