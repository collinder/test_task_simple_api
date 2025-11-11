from fastapi import APIRouter, FastAPI
from aiohttp import web
from routes.wallets import wallet_router
import os


app = FastAPI()

router = APIRouter(prefix="/api/v1")

router.include_router(wallet_router, prefix="/wallets")

app.include_router(router)
