"""
Budget models for Gastiflow.
Manages monthly budgets per category with alerts.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

Base = declarative_base()


# Modelo SQLAlchemy para PostgreSQL
class BudgetDB(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)  # Monthly budget amount
    alert_threshold = Column(Float, default=0.8)  # Alert at 80% by default
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Budget(id={self.id}, category={self.category}, amount={self.amount})>"


# Modelos Pydantic para validación
class BudgetBase(BaseModel):
    """Base budget model"""
    category: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    alert_threshold: float = Field(default=0.8, ge=0.1, le=1.0)


class BudgetCreate(BudgetBase):
    """Request model for creating a budget"""
    pass


class BudgetUpdate(BaseModel):
    """Request model for updating a budget"""
    amount: Optional[float] = Field(None, gt=0)
    alert_threshold: Optional[float] = Field(None, ge=0.1, le=1.0)
    is_active: Optional[bool] = None


class BudgetResponse(BudgetBase):
    """Response model for budget data"""
    id: int
    user_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Campos calculados (se añaden en el servicio)
    spent: float = 0
    remaining: float = 0
    percentage_used: float = 0
    alert_triggered: bool = False

    class Config:
        from_attributes = True


class BudgetProgress(BaseModel):
    """Budget progress for a specific category"""
    category: str
    budget_amount: float
    spent: float
    remaining: float
    percentage_used: float
    alert_triggered: bool
    days_remaining: int


class BudgetAlert(BaseModel):
    """Budget alert notification"""
    budget_id: int
    category: str
    budget_amount: float
    spent: float
    percentage_used: float
    message: str
    severity: str  # 'warning' (80%), 'danger' (100%)
