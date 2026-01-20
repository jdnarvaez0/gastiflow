"""
Expenses router for Gastiflow Web API.
Handles expense CRUD operations and dashboard data.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..dependencies import get_db_service, get_current_user, require_auth
from services.database_service import DatabaseService
from models.expense import ExpenseSchema

router = APIRouter(prefix="/api", tags=["Expenses"])


class ExpenseCreate(BaseModel):
    """Request model for creating an expense."""
    amount: float
    description: str
    category: str
    transaction_type: str
    date: str


@router.get("/dashboard")
def api_dashboard(
    user = Depends(get_current_user),
    db: DatabaseService = Depends(get_db_service)
):
    """Get dashboard data - works for both authenticated and unauthenticated users"""
    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # If user is authenticated, get their data only
    if user:
        user_id = str(user.id)
        monthly_stats = db.get_monthly_stats(user_id, current_year, current_month)
        category_stats = db.get_category_stats(user_id, current_year, current_month)
        history_stats = db.get_six_month_history(user_id)
        recent_expenses = db.get_user_expenses(user_id, limit=5)
    else:
        # For unauthenticated users, return empty data
        monthly_stats = {"income": 0, "expenses": 0, "balance": 0, "savings": 0}
        category_stats = []
        history_stats = {"labels": [], "income": [], "expenses": []}
        recent_expenses = []
    
    return {
        "stats": monthly_stats,
        "categories": category_stats,
        "history": history_stats,
        "expenses": recent_expenses,
        "current_date": now,
        "is_authenticated": user is not None
    }


@router.post("/expenses")
def api_add_expense(
    expense: ExpenseCreate,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """Add expense - requires authentication"""
    user_id = str(user.id)
    
    try:
        # Parse date
        parsed_date = datetime.strptime(expense.date, "%Y-%m-%d")
        
        # Create schema
        expense_data = ExpenseSchema(
            amount=expense.amount,
            description=expense.description,
            category=expense.category,
            transaction_type=expense.transaction_type,
            date=parsed_date
        )
        
        db.create_expense(user_id, expense_data)
        
        return {"message": "Expense added successfully"}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
