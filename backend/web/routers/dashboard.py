"""
Dashboard router for Gastiflow Web API.
Handles HTML dashboard pages (legacy web interface).
"""
from datetime import datetime
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..dependencies import get_db_service
from services.database_service import DatabaseService
from models.expense import ExpenseSchema

# Templates
templates = Jinja2Templates(directory="web/templates")

router = APIRouter(tags=["Dashboard"])


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: DatabaseService = Depends(get_db_service)):
    """Render HTML dashboard page."""
    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # Fetch data (legacy - not user-specific)
    monthly_stats = db.get_monthly_stats("web_user", current_year, current_month)
    category_stats = db.get_category_stats("web_user", current_year, current_month)
    history_stats = db.get_six_month_history("web_user")
    recent_expenses = db.get_all_expenses(limit=5)
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "stats": monthly_stats, 
            "categories": category_stats,
            "history": history_stats,
            "expenses": recent_expenses,
            "current_date": now
        }
    )


@router.get("/add", response_class=HTMLResponse)
def add_expense_form(request: Request):
    """Render add expense form page."""
    return templates.TemplateResponse("add_expense.html", {"request": request})


@router.post("/add")
def add_expense(
    amount: float = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    transaction_type: str = Form(...),
    date: str = Form(...),
    db: DatabaseService = Depends(get_db_service)
):
    """Process add expense form submission."""
    user_id = "web_user"
    
    try:
        # Parse date
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        
        # Create schema
        expense_data = ExpenseSchema(
            amount=amount,
            description=description,
            category=category,
            transaction_type=transaction_type,
            date=parsed_date
        )
        
        db.create_expense(user_id, expense_data)
        
        return RedirectResponse(url="/", status_code=303)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
