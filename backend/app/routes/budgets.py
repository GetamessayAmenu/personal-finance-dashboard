from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils.jwt_handler import get_current_user_with_db
from datetime import datetime

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.get("/")
def get_budgets(db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Get all budgets for current user"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(models.Budget).filter(models.Budget.owner_id == user.id).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Create a new budget"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if budget already exists for this category and month/year
    existing = db.query(models.Budget).filter(
        models.Budget.owner_id == user.id,
        models.Budget.category == budget.category,
        models.Budget.month == budget.month,
        models.Budget.year == budget.year
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Budget already exists for this category and period")

    new_budget = models.Budget(
        category=budget.category,
        amount=budget.amount,
        month=budget.month,
        year=budget.year,
        owner_id=user.id
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

@router.put("/{budget_id}")
def update_budget(budget_id: int, budget_update: schemas.BudgetUpdate, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Update a budget"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.owner_id == user.id
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    budget.amount = budget_update.amount
    budget.category = budget_update.category

    db.commit()
    db.refresh(budget)
    return budget

@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Delete a budget"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.owner_id == user.id
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()
    return {"msg": "Budget deleted successfully"}

@router.get("/progress/{year}/{month}")
def get_budget_progress(year: int, month: int, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user_with_db)):
    """Get budget progress for a specific month"""
    email = user_data["email"]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get budgets for the month
    budgets = db.query(models.Budget).filter(
        models.Budget.owner_id == user.id,
        models.Budget.year == year,
        models.Budget.month == month
    ).all()

    if not budgets:
        return []

    # Get all transactions for this user and month to calculate spending
    transactions = db.query(models.Transaction).filter(
        models.Transaction.owner_id == user.id,
        models.Transaction.date.between(
            datetime(year, month, 1),
            datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        )
    ).all()

    # Calculate progress for each budget
    budget_progress = []
    for budget in budgets:
        # Get expenses for this category in the specified month/year
        category_expenses = [
            t.amount for t in transactions
            if t.type == 'expense' and
            t.category == budget.category and
            t.date.month == month and  # Use DateTime month attribute
            t.date.year == year        # Use DateTime year attribute
        ]

        spent = sum(category_expenses)
        progress = (spent / budget.amount) * 100 if budget.amount > 0 else 0

        budget_progress.append({
            "id": budget.id,
            "category": budget.category,
            "budget_amount": budget.amount,
            "spent": spent,
            "remaining": budget.amount - spent,
            "progress": min(progress, 100),  # Cap at 100%
            "is_over_budget": spent > budget.amount
        })

    return budget_progress
