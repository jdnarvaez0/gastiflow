from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
import enum

Base = declarative_base()


class TransactionType(str, enum.Enum):
    EXPENSE = "expense"
    INCOME = "income"


class Category(str, enum.Enum):
    SUPERMERCADO = "Supermercado"
    TRANSPORTE = "Transporte"
    RESTAURANTE = "Restaurante"
    ENTRETENIMIENTO = "Entretenimiento"
    SALUD = "Salud"
    SERVICIOS = "Servicios"
    EDUCACION = "Educación"
    ROPA = "Ropa"
    TECNOLOGIA = "Tecnología"
    OTROS = "Otros"


# Modelo SQLAlchemy para PostgreSQL
class ExpenseDB(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="ARS")
    category = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Expense(id={self.id}, description={self.description}, amount={self.amount})>"


# Modelo Pydantic para validación
class ExpenseSchema(BaseModel):
    description: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="ARS")
    category: Category
    transaction_type: TransactionType = Field(default=TransactionType.EXPENSE)
    date: Optional[datetime] = Field(default_factory=datetime.now)

    @field_validator('date', mode='before')
    @classmethod
    def set_default_date(cls, v):
        """Asigna la fecha actual si el campo date es None"""
        if v is None:
            return datetime.now()
        return v

    class Config:
        use_enum_values = True

    def format_message(self) -> str:
        """Formatea el mensaje para enviar a Telegram"""
        emoji_type = "💸" if self.transaction_type == "expense" else "💰"
        type_text = "Gasto" if self.transaction_type == "expense" else "Ingreso"

        return f"""✅ Transacción Registrada
📝 Descripción: {self.description}
💰 Monto: ${self.amount} {self.currency}
🏷️ Categoría: {self.category}
📅 Fecha: {self.date.isoformat()}
📊 Tipo: {type_text} ({self.transaction_type})"""
