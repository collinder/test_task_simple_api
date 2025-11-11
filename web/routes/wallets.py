from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import func, select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Transaction
from sqlalchemy import text
from config.db import get_db
from schemas.schemas import *
import uuid
wallet_router = APIRouter()


@wallet_router.get("/{wallet_uuid}", response_model=wallet_model, status_code=status.HTTP_200_OK, summary="Get amount by wallet id")
async def get_wallet(wallet_uuid: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text(f"SELECT amount from wallets where id = '{str(wallet_uuid)}'"))
    amount = result.scalar_one_or_none()
    if amount is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={}
        )
    else:
        return {"id": str(wallet_uuid), "amount": amount}
        return JSONResponse(
            status_code=status.status.HTTP_200_OK,
            content={
                "id": str(wallet_uuid),
                "amount": amount
            }
        )


@wallet_router.post("/create_wallet/create_wallet", response_model=wallet_model, summary="Create wallet", status_code=status.HTTP_201_CREATED)
async def create_wallet(cm: create_model, db: AsyncSession = Depends(get_db)):

    wallet_uuid = uuid.uuid4()
    result = await db.execute(text(f"INSERT INTO wallets (id, amount) VALUES ('{str(wallet_uuid)}', {cm.amount})"))

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "id": str(wallet_uuid),
            "amount": cm.amount
        }
    )


@wallet_router.post("/{wallet_uuid}/operation", response_model=UUID_model, status_code=status.HTTP_200_OK, summary="Update wallet")
async def create_wallet(wallet_uuid: uuid.UUID, omo: operation_model, db: AsyncSession = Depends(get_db)):

    result = await db.execute(text(f"SELECT amount from wallets where id = '{str(wallet_uuid)}'"))
    amount = result.scalar_one_or_none()

    if amount is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={}
        )
    elif omo.amount > amount and omo.operation_type == "WITHDRAW":
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            content={
                "id": str(wallet_uuid),
                "amount": int(amount)
            }
        )
    else:
        if omo.operation_type == "WITHDRAW":
            target_amount = amount - omo.amount
        else:
            target_amount = amount + omo.amount
        result = await db.execute(text(f"UPDATE wallets SET amount = {target_amount} WHERE id = '{str(wallet_uuid)}'"))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "id": str(wallet_uuid),
                "amount": int(target_amount)
            }
        )


@wallet_router.delete("/{wallet_uuid}", response_model=UUID_model, status_code=status.HTTP_200_OK, summary="Delete wallet")
async def delete_wallet(wallet_uuid: uuid.UUID, db: AsyncSession = Depends(get_db)):

    result = await db.execute(text(f"DELETE from wallets where id = '{str(wallet_uuid)}'"))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={}
    )


@wallet_router.get("/get/get/get", status_code=status.HTTP_200_OK,)
async def check():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={}
    )
