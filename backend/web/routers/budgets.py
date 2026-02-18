"""
Budgets router for Gastiflow Web API.
Handles budget CRUD operations and alerts.
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from ..dependencies import get_db_service, require_auth
from services.database_service import DatabaseService
from models.budget import BudgetCreate, BudgetUpdate, BudgetResponse, BudgetAlert
from models.expense import Category

router = APIRouter(prefix="/api/budgets", tags=["Budgets"])


@router.get("", response_model=List[BudgetResponse])
def get_budgets(
    include_progress: bool = Query(True, description="Include current month spending progress"),
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Get all active budgets for the current user.
    
    - **include_progress**: If true, includes spending data for current month
    """
    user_id = str(user.id)
    
    if include_progress:
        # Get budgets with progress data
        progress_data = db.get_budget_progress(user_id)
        return [
            BudgetResponse(
                id=p["id"],
                user_id=user_id,
                category=p["category"],
                amount=p["budget_amount"],
                alert_threshold=p["alert_threshold"],
                is_active=True,
                created_at=datetime.now(),  # Will be overwritten
                updated_at=datetime.now(),
                spent=p["spent"],
                remaining=p["remaining"],
                percentage_used=p["percentage_used"],
                alert_triggered=p["alert_triggered"]
            )
            for p in progress_data
        ]
    else:
        # Get raw budgets only
        budgets = db.get_user_budgets(user_id)
        return [
            BudgetResponse(
                id=b.id,
                user_id=b.user_id,
                category=b.category,
                amount=b.amount,
                alert_threshold=b.alert_threshold,
                is_active=b.is_active,
                created_at=b.created_at,
                updated_at=b.updated_at
            )
            for b in budgets
        ]


@router.post("", response_model=BudgetResponse, status_code=201)
def create_budget(
    budget: BudgetCreate,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Create a new budget for a category.
    
    - **category**: Category name (must be unique per user)
    - **amount**: Monthly budget amount
    - **alert_threshold**: Alert trigger percentage (0.1 - 1.0, default 0.8)
    """
    user_id = str(user.id)
    
    # Validate category exists
    try:
        Category(budget.category)
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid category. Valid categories: {[c.value for c in Category]}"
        )
    
    # Check if budget already exists for this category
    existing_budgets = db.get_user_budgets(user_id)
    if any(b.category == budget.category for b in existing_budgets):
        raise HTTPException(
            status_code=400,
            detail=f"Budget already exists for category '{budget.category}'. Update existing instead."
        )
    
    # Create budget
    new_budget = db.create_budget(
        user_id=user_id,
        category=budget.category,
        amount=budget.amount,
        alert_threshold=budget.alert_threshold
    )
    
    if not new_budget:
        raise HTTPException(status_code=500, detail="Failed to create budget")
    
    return BudgetResponse(
        id=new_budget.id,
        user_id=new_budget.user_id,
        category=new_budget.category,
        amount=new_budget.amount,
        alert_threshold=new_budget.alert_threshold,
        is_active=new_budget.is_active,
        created_at=new_budget.created_at,
        updated_at=new_budget.updated_at
    )


@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: int,
    budget_update: BudgetUpdate,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Update an existing budget.
    
    - **amount**: New budget amount (optional)
    - **alert_threshold**: New alert threshold (optional)
    - **is_active**: Enable/disable budget (optional)
    """
    user_id = str(user.id)
    
    # Check budget exists and belongs to user
    existing = db.get_budget_by_id(budget_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    if existing.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this budget")
    
    # Update budget
    updated = db.update_budget(
        budget_id=budget_id,
        amount=budget_update.amount,
        alert_threshold=budget_update.alert_threshold,
        is_active=budget_update.is_active
    )
    
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update budget")
    
    return BudgetResponse(
        id=updated.id,
        user_id=updated.user_id,
        category=updated.category,
        amount=updated.amount,
        alert_threshold=updated.alert_threshold,
        is_active=updated.is_active,
        created_at=updated.created_at,
        updated_at=updated.updated_at
    )


@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """Delete (deactivate) a budget."""
    user_id = str(user.id)
    
    # Check budget exists and belongs to user
    existing = db.get_budget_by_id(budget_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    if existing.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this budget")
    
    success = db.delete_budget(budget_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete budget")
    
    return {"message": "Budget deleted successfully"}


@router.get("/alerts", response_model=List[BudgetAlert])
def get_budget_alerts(
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Get active budget alerts for the current user.
    
    Returns alerts for budgets that have exceeded their alert threshold.
    - **severity=warning**: Budget has exceeded alert_threshold (default 80%)
    - **severity=danger**: Budget has exceeded 100%
    """
    user_id = str(user.id)
    alerts = db.get_budget_alerts(user_id)
    
    return [
        BudgetAlert(
            budget_id=a["budget_id"],
            category=a["category"],
            budget_amount=a["budget_amount"],
            spent=a["spent"],
            percentage_used=a["percentage_used"],
            message=a["message"],
            severity=a["severity"]
        )
        for a in alerts
    ]


@router.get("/progress")
def get_budget_progress(
    year: Optional[int] = Query(None, description="Year (default: current)"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Month (1-12, default: current)"),
    user = Depends(require_auth),
    db: DatabaseService = Depends(get_db_service)
):
    """
    Get detailed budget progress for all categories.
    
    Includes spending data, remaining budget, and percentage used.
    """
    user_id = str(user.id)
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    
    progress = db.get_budget_progress(user_id, year, month)
    
    return {
        "year": year,
        "month": month,
        "budgets": progress,
        "total_budget": sum(b["budget_amount"] for b in progress),
        "total_spent": sum(b["spent"] for b in progress),
        "total_remaining": sum(b["remaining"] for b in progress),
        "alerts_count": sum(1 for b in progress if b["alert_triggered"])
    }
