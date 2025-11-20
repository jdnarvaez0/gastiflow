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
