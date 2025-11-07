from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TransactionBase(BaseModel):
    type: str
    category: str
    amount: float
    date: datetime
    note: Optional[str] = None

class TransactionCreate(BaseModel):
    type: str
    category: str
    amount: float
    date: datetime
    note: Optional[str] = None

class TransactionUpdate(BaseModel):
    type: str
    category: str
    amount: float
    date: datetime
    note: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    owner_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    category: str
    amount: float
    month: int
    year: int

class BudgetCreate(BaseModel):
    category: str
    amount: float
    month: int
    year: int

class BudgetUpdate(BaseModel):
    category: str
    amount: float

class Budget(BudgetBase):
    id: int
    owner_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True