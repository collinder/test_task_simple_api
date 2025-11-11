from datetime import datetime
from pydantic import BaseModel, Field, validator, PositiveInt
import uuid
from typing import Literal


class UUID_model(BaseModel):
    id: uuid.UUID


class wallet_model(BaseModel):
    id: uuid.UUID
    amount: PositiveInt


class operation_model(BaseModel):
    operation_type: Literal["DEPOSIT", "WITHDRAW"]
    amount: PositiveInt


class create_model(BaseModel):
    amount: PositiveInt
