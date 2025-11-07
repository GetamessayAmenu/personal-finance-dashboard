from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils.jwt_handler import get_current_user_with_db
from typing import List
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def add_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Create a new transaction for the current user"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ensure the transaction belongs to the current user
    new_tx = models.Transaction(
        type=tx.type,
        category=tx.category,
        amount=tx.amount,
        date=tx.date,
        note=tx.note,
        owner_id=user.id
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx

@router.get("/", response_model=List[schemas.Transaction])
def get_transactions(db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Get all transactions for the current user"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(models.Transaction).filter(models.Transaction.owner_id == user.id).all()

@router.get("/{transaction_id}", response_model=schemas.Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Get a specific transaction by ID"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.put("/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(transaction_id: int, tx_update: schemas.TransactionUpdate, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Update a specific transaction"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Update transaction fields
    transaction.type = tx_update.type
    transaction.category = tx_update.category
    transaction.amount = tx_update.amount
    transaction.date = tx_update.date
    transaction.note = tx_update.note

    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Delete a specific transaction"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return {"msg": "Transaction deleted successfully"}

@router.get("/summary/{year}/{month}")
def get_monthly_summary(year: int, month: int, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Get monthly financial summary for the current user"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all transactions for the specified month
    transactions = db.query(models.Transaction).filter(
        models.Transaction.owner_id == user.id,
        models.Transaction.date.between(
            datetime(year, month, 1),
            datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        )
    ).all()

    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expenses = sum(t.amount for t in transactions if t.type == "expense")
    net_amount = total_income - total_expenses

    # Get category breakdown for expenses
    expense_categories = {}
    for t in transactions:
        if t.type == "expense":
            expense_categories[t.category] = expense_categories.get(t.category, 0) + t.amount

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_amount": net_amount,
        "transaction_count": len(transactions),
        "expense_categories": expense_categories
    }

@router.get("/categories/all")
def get_all_categories(db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Get all unique transaction categories for the current user"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get unique categories from user's transactions
    categories = db.query(models.Transaction.category).filter(
        models.Transaction.owner_id == user.id
    ).distinct().all()

    return {"categories": [cat[0] for cat in categories if cat[0]]}

@router.get("/dashboard/overview")
def get_dashboard_overview(db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Get dashboard overview data for the current user"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    from datetime import datetime
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    # Get current month transactions
    current_month_transactions = db.query(models.Transaction).filter(
        models.Transaction.owner_id == user.id,
        models.Transaction.date.between(
            datetime(current_year, current_month, 1),
            datetime(current_year, current_month + 1, 1) if current_month < 12 else datetime(current_year + 1, 1, 1)
        )
    ).all()

    # Calculate current month totals
    current_income = sum(t.amount for t in current_month_transactions if t.type == "income")
    current_expenses = sum(t.amount for t in current_month_transactions if t.type == "expense")

    # Get all-time totals
    all_transactions = db.query(models.Transaction).filter(models.Transaction.owner_id == user.id).all()
    total_income = sum(t.amount for t in all_transactions if t.type == "income")
    total_expenses = sum(t.amount for t in all_transactions if t.type == "expense")

    # Get transaction counts
    total_transactions = len(all_transactions)
    current_month_count = len(current_month_transactions)

    # Get recent transactions (last 5)
    recent_transactions = db.query(models.Transaction).filter(
        models.Transaction.owner_id == user.id
    ).order_by(models.Transaction.date.desc()).limit(5).all()

    # Get top expense categories this month
    expense_categories = {}
    for t in current_month_transactions:
        if t.type == "expense":
            expense_categories[t.category] = expense_categories.get(t.category, 0) + t.amount

    # Sort categories by amount and get top 5
    top_categories = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "current_month": {
            "income": current_income,
            "expenses": current_expenses,
            "net": current_income - current_expenses,
            "transaction_count": current_month_count
        },
        "all_time": {
            "income": total_income,
            "expenses": total_expenses,
            "net": total_income - total_expenses,
            "transaction_count": total_transactions
        },
        "recent_transactions": [
            {
                "id": t.id,
                "type": t.type,
                "category": t.category,
                "amount": t.amount,
                "date": t.date.isoformat(),
                "note": t.note
            } for t in recent_transactions
        ],
        "top_expense_categories": [
            {"category": cat, "amount": amount} for cat, amount in top_categories
        ]
    }