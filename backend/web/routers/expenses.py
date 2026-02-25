"""
Expenses router for Gastiflow Web API.
Handles expense CRUD operations and dashboard data.
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from ..dependencies import get_db_service, get_current_user, require_auth
from services.database_service import DatabaseService
from models.expense import ExpenseSchema, ExpenseResponse, PaginatedResponse

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


@router.get("/expenses", response_model=PaginatedResponse[ExpenseResponse])
def api_get_expenses(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    transaction_type: Optional[str] = Query(None, description="Filter by type: expense or income"),
    start_date: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Get user expenses with pagination and optional filters.
    
    - **page**: Page number (starts at 1)
    - **per_page**: Number of items per page (1-100, default 20)
    - **category**: Filter by category name
    - **transaction_type**: Filter by 'expense' or 'income'
    - **start_date**: Filter expenses from this date (YYYY-MM-DD)
    - **end_date**: Filter expenses until this date (YYYY-MM-DD)
    """
    user_id = str(user.id)
    
    # Parse dates if provided
    parsed_start = None
    parsed_end = None
    
    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD")
    
    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, "%Y-%m-%d")
            # Set to end of day
            parsed_end = parsed_end.replace(hour=23, minute=59, second=59)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD")
    
    # Get paginated results
    result = db.get_user_expenses_paginated(
        user_id=user_id,
        page=page,
        per_page=per_page,
        category=category,
        transaction_type=transaction_type,
        start_date=parsed_start,
        end_date=parsed_end
    )
    
    # Convert SQLAlchemy objects to Pydantic models
    expense_responses = [
        ExpenseResponse.model_validate(expense) for expense in result["items"]
    ]
    
    return PaginatedResponse[ExpenseResponse](
        items=expense_responses,
        total=result["total"],
        page=result["page"],
        per_page=result["per_page"],
        total_pages=result["total_pages"],
        has_next=result["has_next"],
        has_prev=result["has_prev"]
    )


# Legacy endpoint for backward compatibility (returns all expenses)
@router.get("/expenses/all")
def api_get_all_expenses(
    limit: int = Query(100, ge=1, le=500),
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """Get all user expenses (limited) - for backward compatibility"""
    from loguru import logger
    
    user_id = str(user.id)
    logger.info(f"Fetching all expenses for user {user_id}, limit={limit}")
    
    expenses = db.get_user_expenses(user_id, limit=limit)
    logger.info(f"Found {len(expenses)} expenses for user {user_id}")
    
    return expenses


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


@router.delete("/expenses/{expense_id}")
def api_delete_expense(
    expense_id: int,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """Delete an expense by ID"""
    user_id = str(user.id)
    
    # Get expense to verify ownership
    expense = db.get_expense_by_id(expense_id)
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    if str(expense.user_id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this expense")
    
    success = db.delete_expense(expense_id)
    
    if success:
        return {"message": "Expense deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete expense")


@router.put("/expenses/{expense_id}")
def api_update_expense(
    expense_id: int,
    expense: ExpenseCreate,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """Update an expense by ID"""
    from loguru import logger
    
    user_id = str(user.id)
    logger.info(f"Updating expense {expense_id} for user {user_id}")
    
    # Get expense to verify ownership
    existing_expense = db.get_expense_by_id(expense_id)
    
    if not existing_expense:
        logger.warning(f"Expense {expense_id} not found")
        raise HTTPException(status_code=404, detail="Expense not found")
    
    if str(existing_expense.user_id) != user_id:
        logger.warning(f"User {user_id} not authorized to update expense {expense_id}")
        raise HTTPException(status_code=403, detail="Not authorized to update this expense")
    
    try:
        # Parse date (expecting YYYY-MM-DD format)
        logger.info(f"Parsing date: {expense.date}")
        parsed_date = datetime.strptime(expense.date, "%Y-%m-%d")
        
        # Update expense
        updated = db.update_expense(
            expense_id=expense_id,
            amount=expense.amount,
            description=expense.description,
            category=expense.category,
            transaction_type=expense.transaction_type,
            date=parsed_date
        )
        
        if updated:
            logger.info(f"Expense {expense_id} updated successfully")
            return {"message": "Expense updated successfully"}
        else:
            logger.error(f"Failed to update expense {expense_id}")
            raise HTTPException(status_code=500, detail="Failed to update expense")
        
    except ValueError as e:
        logger.error(f"Invalid data for expense update: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        logger.error(f"Server error updating expense: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
