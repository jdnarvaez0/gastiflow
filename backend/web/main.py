import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from services.database_service import DatabaseService
from models.expense import ExpenseSchema, Category, TransactionType

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Gastiflow Web")

# Mount static files
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Templates
templates = Jinja2Templates(directory="web/templates")

# Database Service Dependency
def get_db_service():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Fallback for local development if not in env
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        db = os.getenv("POSTGRES_DB", "gastiflow")
        port = os.getenv("POSTGRES_PORT", "5432")
        host = os.getenv("POSTGRES_HOST", "localhost")
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    return DatabaseService(db_url)

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: DatabaseService = Depends(get_db_service)):
    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # Fetch data
    monthly_stats = db.get_monthly_stats(current_year, current_month)
    category_stats = db.get_category_stats(current_year, current_month)
    history_stats = db.get_six_month_history()
    recent_expenses = db.get_all_expenses(limit=5) # Reduced to 5 for the "Recent" table
    
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

@app.get("/add", response_class=HTMLResponse)
def add_expense_form(request: Request):
    return templates.TemplateResponse("add_expense.html", {"request": request})

@app.post("/add")
def add_expense(
    amount: float = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    transaction_type: str = Form(...),
    date: str = Form(...),
    db: DatabaseService = Depends(get_db_service)
):
    user_id = "web_user"
    
    try:
        # Parse date
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        
        # Create schema
        expense_data = ExpenseSchema(
            amount=amount,
            description=description,
            category=category, # Pydantic will validate against Enum
            transaction_type=transaction_type,
            date=parsed_date
        )
        
        db.create_expense(user_id, expense_data)
        
        return RedirectResponse(url="/", status_code=303)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# --- API Endpoints for Nuxt Frontend ---

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add CORS middleware to allow requests from the Nuxt frontend (usually running on port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In production, specify the frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dashboard")
def api_dashboard(db: DatabaseService = Depends(get_db_service)):
    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # Fetch data
    monthly_stats = db.get_monthly_stats(current_year, current_month)
    category_stats = db.get_category_stats(current_year, current_month)
    history_stats = db.get_six_month_history()
    recent_expenses = db.get_all_expenses(limit=5)
    
    return {
        "stats": monthly_stats,
        "categories": category_stats,
        "history": history_stats,
        "expenses": recent_expenses,
        "current_date": now
    }

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    category: str
    transaction_type: str
    date: str

@app.post("/api/expenses")
def api_add_expense(expense: ExpenseCreate, db: DatabaseService = Depends(get_db_service)):
    user_id = "web_user"
    
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
