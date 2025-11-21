from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.expense import Base, ExpenseDB, ExpenseSchema
from typing import List, Optional
from loguru import logger


class DatabaseService:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        # Crear tablas si no existen
        Base.metadata.create_all(bind=self.engine)
        logger.info("Base de datos inicializada")

    def get_session(self) -> Session:
        """Retorna una nueva sesión de base de datos"""
        return self.SessionLocal()

    def create_expense(self, user_id: str, expense: ExpenseSchema) -> ExpenseDB:
        """
        Crea un nuevo registro de gasto en la base de datos
        """
        session = self.get_session()
        try:
            db_expense = ExpenseDB(
                user_id=user_id,
                description=expense.description,
                amount=expense.amount,
                currency=expense.currency,
                category=expense.category,
                transaction_type=expense.transaction_type,
                date=expense.date,
            )

            session.add(db_expense)
            session.commit()
            session.refresh(db_expense)

            logger.info(f"Gasto creado: ID={db_expense.id}, Usuario={user_id}")
            return db_expense

        except Exception as e:
            session.rollback()
            logger.error(f"Error creando gasto: {e}")
            raise
        finally:
            session.close()

    def get_user_expenses(self, user_id: str, limit: int = 10) -> List[ExpenseDB]:
        """
        Obtiene los últimos gastos de un usuario
        """
        session = self.get_session()
        try:
            expenses = (
                session.query(ExpenseDB)
                .filter(ExpenseDB.user_id == user_id)
                .order_by(ExpenseDB.date.desc())
                .limit(limit)
                .all()
            )

            return expenses

        except Exception as e:
            logger.error(f"Error obteniendo gastos: {e}")
            return []
        finally:
            session.close()

    def get_all_expenses(self, limit: int = 50) -> List[ExpenseDB]:
        """
        Obtiene los últimos gastos de todos los usuarios
        """
        session = self.get_session()
        try:
            expenses = (
                session.query(ExpenseDB)
                .order_by(ExpenseDB.date.desc())
                .limit(limit)
                .all()
            )

            return expenses

        except Exception as e:
            logger.error(f"Error obteniendo todos los gastos: {e}")
            return []
        finally:
            session.close()

    def get_expense_by_id(self, expense_id: int) -> Optional[ExpenseDB]:
        """
        Obtiene un gasto por su ID
        """
        session = self.get_session()
        try:
            expense = (
                session.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
            )

            return expense

        except Exception as e:
            logger.error(f"Error obteniendo gasto: {e}")
            return None
        finally:
            session.close()

    def delete_expense(self, expense_id: int) -> bool:
        """
        Elimina un gasto
        """
        session = self.get_session()
        try:
            expense = (
                session.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
            )

            if expense:
                session.delete(expense)
                session.commit()
                logger.info(f"Gasto eliminado: ID={expense_id}")
                return True

            return False

        except Exception as e:
            session.rollback()
            logger.error(f"Error eliminando gasto: {e}")
            return False
        finally:
            session.close()

    def get_user_stats(self, user_id: str) -> dict:
        """
        Obtiene estadísticas de gastos del usuario
        """
        session = self.get_session()
        try:
            from sqlalchemy import func

            # Total de gastos
            total_expenses = (
                session.query(func.sum(ExpenseDB.amount))
                .filter(ExpenseDB.user_id == user_id)
                .filter(ExpenseDB.transaction_type == "expense")
                .scalar()
                or 0
            )

            # Total de ingresos
            total_income = (
                session.query(func.sum(ExpenseDB.amount))
                .filter(ExpenseDB.user_id == user_id)
                .filter(ExpenseDB.transaction_type == "income")
                .scalar()
                or 0
            )

            # Cantidad de transacciones
            count = (
                session.query(func.count(ExpenseDB.id))
                .filter(ExpenseDB.user_id == user_id)
                .scalar()
                or 0
            )

            return {
                "total_expenses": float(total_expenses),
                "total_income": float(total_income),
                "balance": float(total_income - total_expenses),
                "transaction_count": count,
            }

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
        finally:
            session.close()

    def get_all_stats(self) -> dict:
        """
        Obtiene estadísticas de gastos de todos los usuarios
        """
        session = self.get_session()
        try:
            from sqlalchemy import func

            # Total de gastos
            total_expenses = (
                session.query(func.sum(ExpenseDB.amount))
                .filter(ExpenseDB.transaction_type == "expense")
                .scalar()
                or 0
            )

            # Total de ingresos
            total_income = (
                session.query(func.sum(ExpenseDB.amount))
                .filter(ExpenseDB.transaction_type == "income")
                .scalar()
                or 0
            )

            # Cantidad de transacciones
            count = (
                session.query(func.count(ExpenseDB.id))
                .scalar()
                or 0
            )

            return {
                "total_expenses": float(total_expenses),
                "total_income": float(total_income),
                "balance": float(total_income - total_expenses),
                "transaction_count": count,
            }

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas globales: {e}")
            return {}
        finally:
            session.close()

    def get_monthly_stats(self, year: int, month: int) -> dict:
        """
        Obtiene estadísticas para un mes específico
        """
        session = self.get_session()
        try:
            from sqlalchemy import func, extract, and_

            # Filtros base
            month_filter = and_(
                extract('year', ExpenseDB.date) == year,
                extract('month', ExpenseDB.date) == month
            )

            # Total de gastos del mes
            total_expenses = (
                session.query(func.sum(ExpenseDB.amount))
                .filter(month_filter)
                .filter(ExpenseDB.transaction_type == "expense")
                .scalar()
                or 0
            )

            # Total de ingresos del mes
            total_income = (
                session.query(func.sum(ExpenseDB.amount))
                .filter(month_filter)
                .filter(ExpenseDB.transaction_type == "income")
                .scalar()
                or 0
            )
            
            # Ahorro (Income - Expense)
            balance = float(total_income) - float(total_expenses)

            return {
                "income": float(total_income),
                "expenses": float(total_expenses),
                "balance": balance,
                "savings": balance
            }

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas mensuales: {e}")
            return {"income": 0, "expenses": 0, "balance": 0, "savings": 0}
        finally:
            session.close()

    def get_category_stats(self, year: int, month: int) -> List[dict]:
        """
        Obtiene desglose de gastos por categoría para un mes
        """
        session = self.get_session()
        try:
            from sqlalchemy import func, extract, and_

            month_filter = and_(
                extract('year', ExpenseDB.date) == year,
                extract('month', ExpenseDB.date) == month,
                ExpenseDB.transaction_type == "expense"
            )

            results = (
                session.query(
                    ExpenseDB.category,
                    func.sum(ExpenseDB.amount).label('total')
                )
                .filter(month_filter)
                .group_by(ExpenseDB.category)
                .order_by(func.sum(ExpenseDB.amount).desc())
                .all()
            )

            return [{"category": r[0], "amount": float(r[1])} for r in results]

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas por categoría: {e}")
            return []
        finally:
            session.close()

    def get_six_month_history(self) -> dict:
        """
        Obtiene historial de los últimos 6 meses para gráficos
        """
        session = self.get_session()
        try:
            from sqlalchemy import func, extract
            from datetime import datetime, timedelta
            from calendar import month_abbr

            today = datetime.now()
            six_months_ago = today - timedelta(days=180)
            
            # Single query for expenses
            expense_query = (
                session.query(
                    extract('year', ExpenseDB.date).label('year'),
                    extract('month', ExpenseDB.date).label('month'),
                    func.sum(ExpenseDB.amount).label('total')
                )
                .filter(ExpenseDB.date >= six_months_ago)
                .filter(ExpenseDB.transaction_type == "expense")
                .group_by(extract('year', ExpenseDB.date), extract('month', ExpenseDB.date))
                .all()
            )
            
            # Single query for income
            income_query = (
                session.query(
                    extract('year', ExpenseDB.date).label('year'),
                    extract('month', ExpenseDB.date).label('month'),
                    func.sum(ExpenseDB.amount).label('total')
                )
                .filter(ExpenseDB.date >= six_months_ago)
                .filter(ExpenseDB.transaction_type == "income")
                .group_by(extract('year', ExpenseDB.date), extract('month', ExpenseDB.date))
                .all()
            )
            
            expenses_by_month = {(int(r[0]), int(r[1])): float(r[2]) for r in expense_query}
            income_by_month = {(int(r[0]), int(r[1])): float(r[2]) for r in income_query}
            
            labels = []
            income_data = []
            expense_data = []
            
            for i in range(5, -1, -1):
                date_cursor = today - timedelta(days=i*30)
                month = date_cursor.month
                year = date_cursor.year
                month_name = month_abbr[month]
                
                labels.append(month_name)
                income_data.append(income_by_month.get((year, month), 0))
                expense_data.append(expenses_by_month.get((year, month), 0))
            
            return {
                "labels": labels,
                "income": income_data,
                "expenses": expense_data
            }

        except Exception as e:
            logger.error(f"Error obteniendo historial: {e}")
            return {"labels": [], "income": [], "expenses": []}
        finally:
            session.close()
