from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.expense import Base, ExpenseDB, ExpenseSchema
from models.user import UserDB, RefreshTokenDB
from models.telegram_link_code import TelegramLinkCodeDB
from models.budget import BudgetDB
from typing import List, Optional
from loguru import logger
import hashlib
import string
import secrets
from datetime import datetime, timedelta


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

    def get_user_expenses_paginated(
        self, 
        user_id: str, 
        page: int = 1, 
        per_page: int = 20,
        category: str = None,
        transaction_type: str = None,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> dict:
        """
        Obtiene los gastos de un usuario con paginación y filtros opcionales
        
        Args:
            user_id: ID del usuario
            page: Número de página (1-based)
            per_page: Items por página
            category: Filtrar por categoría (opcional)
            transaction_type: Filtrar por tipo (expense/income)
            start_date: Fecha inicial (opcional)
            end_date: Fecha final (opcional)
            
        Returns:
            dict con items, total, page, per_page, total_pages, has_next, has_prev
        """
        session = self.get_session()
        try:
            from sqlalchemy import func
            
            # Query base
            query = session.query(ExpenseDB).filter(ExpenseDB.user_id == user_id)
            
            # Aplicar filtros
            if category:
                query = query.filter(ExpenseDB.category == category)
            if transaction_type:
                query = query.filter(ExpenseDB.transaction_type == transaction_type)
            if start_date:
                query = query.filter(ExpenseDB.date >= start_date)
            if end_date:
                query = query.filter(ExpenseDB.date <= end_date)
            
            # Contar total
            total = query.count()
            
            # Calcular offset y total de páginas
            offset = (page - 1) * per_page
            total_pages = (total + per_page - 1) // per_page  # Ceiling division
            
            # Obtener items paginados
            expenses = (
                query
                .order_by(ExpenseDB.date.desc())
                .offset(offset)
                .limit(per_page)
                .all()
            )
            
            return {
                "items": expenses,
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }

        except Exception as e:
            logger.error(f"Error obteniendo gastos paginados: {e}")
            return {
                "items": [],
                "total": 0,
                "page": page,
                "per_page": per_page,
                "total_pages": 0,
                "has_next": False,
                "has_prev": False
            }
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

    def update_expense(self, expense_id: int, **kwargs) -> Optional[ExpenseDB]:
        """
        Actualiza un gasto existente
        
        Args:
            expense_id: ID del gasto
            **kwargs: Campos a actualizar (amount, description, category, transaction_type, date)
            
        Returns:
            ExpenseDB actualizado o None si no existe
        """
        session = self.get_session()
        try:
            expense = session.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
            
            if not expense:
                return None
            
            # Actualizar campos permitidos
            allowed_fields = ['amount', 'description', 'category', 'transaction_type', 'date']
            for key, value in kwargs.items():
                if key in allowed_fields and hasattr(expense, key):
                    setattr(expense, key, value)
            
            session.commit()
            session.refresh(expense)
            logger.info(f"Gasto actualizado: ID={expense_id}")
            return expense
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error actualizando gasto: {e}")
            return None
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

    def get_monthly_stats(self, user_id: str, year: int, month: int) -> dict:
        """
        Obtiene estadísticas para un mes específico de un usuario
        """
        session = self.get_session()
        try:
            from sqlalchemy import func, extract, and_

            # Filtros base incluyendo user_id
            month_filter = and_(
                ExpenseDB.user_id == user_id,
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

    def get_category_stats(self, user_id: str, year: int, month: int) -> List[dict]:
        """
        Obtiene desglose de gastos por categoría para un mes de un usuario
        """
        session = self.get_session()
        try:
            from sqlalchemy import func, extract, and_

            month_filter = and_(
                ExpenseDB.user_id == user_id,
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

    def get_six_month_history(self, user_id: str) -> dict:
        """
        Obtiene historial de los últimos 6 meses para gráficos de un usuario
        """
        session = self.get_session()
        try:
            from sqlalchemy import func, extract, and_
            from datetime import datetime, timedelta
            from calendar import month_abbr

            today = datetime.now()
            six_months_ago = today - timedelta(days=180)
            
            # Single query for expenses filtered by user_id
            expense_query = (
                session.query(
                    extract('year', ExpenseDB.date).label('year'),
                    extract('month', ExpenseDB.date).label('month'),
                    func.sum(ExpenseDB.amount).label('total')
                )
                .filter(ExpenseDB.user_id == user_id)
                .filter(ExpenseDB.date >= six_months_ago)
                .filter(ExpenseDB.transaction_type == "expense")
                .group_by(extract('year', ExpenseDB.date), extract('month', ExpenseDB.date))
                .all()
            )
            
            # Single query for income filtered by user_id
            income_query = (
                session.query(
                    extract('year', ExpenseDB.date).label('year'),
                    extract('month', ExpenseDB.date).label('month'),
                    func.sum(ExpenseDB.amount).label('total')
                )
                .filter(ExpenseDB.user_id == user_id)
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

    # ==================== USER MANAGEMENT ====================

    def create_user(self, username: str, hashed_password: str, email: str = None, telegram_id: str = None, full_name: str = None) -> UserDB:
        """
        Create a new user
        """
        session = self.get_session()
        try:
            db_user = UserDB(
                username=username,
                hashed_password=hashed_password,
                email=email,
                telegram_id=telegram_id,
                full_name=full_name
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            logger.info(f"Usuario creado: ID={db_user.id}, Username={username}")
            return db_user
        except Exception as e:
            session.rollback()
            logger.error(f"Error creando usuario: {e}")
            raise
        finally:
            session.close()

    def get_user_by_username(self, username: str) -> Optional[UserDB]:
        """
        Get user by username
        """
        session = self.get_session()
        try:
            user = session.query(UserDB).filter(UserDB.username == username).first()
            if user:
                session.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Error obteniendo usuario por username: {e}")
            return None
        finally:
            session.close()

    def get_user_by_id(self, user_id: int) -> Optional[UserDB]:
        """
        Get user by ID
        """
        session = self.get_session()
        try:
            user = session.query(UserDB).filter(UserDB.id == user_id).first()
            if user:
                session.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Error obteniendo usuario por ID: {e}")
            return None
        finally:
            session.close()

    def get_user_by_telegram_id(self, telegram_id: str) -> Optional[UserDB]:
        """
        Get user by Telegram ID
        """
        session = self.get_session()
        try:
            user = session.query(UserDB).filter(UserDB.telegram_id == telegram_id).first()
            if user:
                session.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Error obteniendo usuario por telegram_id: {e}")
            return None
        finally:
            session.close()

    def update_user(self, user_id: int, **kwargs) -> Optional[UserDB]:
        """
        Update user fields
        """
        session = self.get_session()
        try:
            user = session.query(UserDB).filter(UserDB.id == user_id).first()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key) and value is not None:
                        setattr(user, key, value)
                session.commit()
                session.refresh(user)
                logger.info(f"Usuario actualizado: ID={user_id}")
            return user
        except Exception as e:
            session.rollback()
            logger.error(f"Error actualizando usuario: {e}")
            return None
        finally:
            session.close()

    def increment_interaction_count(self, telegram_id: str) -> int:
        """
        Increment interaction count for a telegram user (for free trial tracking)
        Returns the new interaction count
        """
        session = self.get_session()
        try:
            user = session.query(UserDB).filter(UserDB.telegram_id == telegram_id).first()
            if user:
                user.interaction_count = (user.interaction_count or 0) + 1
                session.commit()
                return user.interaction_count
            else:
                # Create a temporary user entry for tracking
                temp_user = UserDB(
                    username=f"telegram_{telegram_id}",
                    hashed_password="",  # No password for telegram-only users
                    telegram_id=telegram_id,
                    interaction_count=1
                )
                session.add(temp_user)
                session.commit()
                return 1
        except Exception as e:
            session.rollback()
            logger.error(f"Error incrementando interaction_count: {e}")
            return 0
        finally:
            session.close()

    def get_interaction_count(self, telegram_id: str) -> int:
        """
        Get interaction count for a telegram user
        """
        session = self.get_session()
        try:
            user = session.query(UserDB).filter(UserDB.telegram_id == telegram_id).first()
            return user.interaction_count if user else 0
        except Exception as e:
            logger.error(f"Error obteniendo interaction_count: {e}")
            return 0
        finally:
            session.close()

    # ==================== EMAIL VERIFICATION ====================

    def get_user_by_email(self, email: str) -> Optional[UserDB]:
        """
        Get user by email address
        """
        session = self.get_session()
        try:
            user = session.query(UserDB).filter(UserDB.email == email).first()
            if user:
                session.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Error obteniendo usuario por email: {e}")
            return None
        finally:
            session.close()

    def set_email_verification_token(self, user_id: int, token: str) -> bool:
        """
        Set email verification token for a user
        
        Args:
            user_id: User ID
            token: Verification token
            
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            from datetime import datetime
            user = session.query(UserDB).filter(UserDB.id == user_id).first()
            if user:
                user.email_verification_token = token
                user.email_verification_sent_at = datetime.utcnow()
                session.commit()
                logger.info(f"Verification token set for user ID={user_id}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error setting verification token: {e}")
            return False
        finally:
            session.close()

    def verify_user_email(self, user_id: int) -> bool:
        """
        Mark user's email as verified
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            user = session.query(UserDB).filter(UserDB.id == user_id).first()
            if user:
                user.email_verified = True
                user.email_verification_token = None
                user.email_verification_sent_at = None
                session.commit()
                logger.info(f"Email verified for user ID={user_id}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error verifying email: {e}")
            return False
        finally:
            session.close()

    def update_user_email(self, user_id: int, new_email: str) -> Optional[UserDB]:
        """
        Update user's email and reset verification status
        
        Args:
            user_id: User ID
            new_email: New email address
            
        Returns:
            Updated user object if successful, None otherwise
        """
        session = self.get_session()
        try:
            user = session.query(UserDB).filter(UserDB.id == user_id).first()
            if user:
                user.email = new_email
                user.email_verified = False
                user.email_verification_token = None
                user.email_verification_sent_at = None
                session.commit()
                session.refresh(user)
                logger.info(f"Email updated for user ID={user_id}")
                return user
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating email: {e}")
            return None
        finally:
            session.close()



    # ==================== REFRESH TOKEN MANAGEMENT ====================

    def create_refresh_token(self, user_id: int, token: str, expires_at: datetime) -> Optional[RefreshTokenDB]:
        """
        Store a refresh token in the database
        
        Args:
            user_id: User ID
            token: Refresh token (will be hashed)
            expires_at: Token expiration datetime
            
        Returns:
            RefreshTokenDB object if successful, None otherwise
        """
        session = self.get_session()
        try:
            # Hash the token before storing
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            
            db_token = RefreshTokenDB(
                user_id=user_id,
                token_hash=token_hash,
                expires_at=expires_at
            )
            session.add(db_token)
            session.commit()
            session.refresh(db_token)
            logger.info(f"Refresh token created for user ID={user_id}")
            return db_token
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating refresh token: {e}")
            return None
        finally:
            session.close()

    def get_refresh_token(self, token: str) -> Optional[RefreshTokenDB]:
        """
        Get refresh token by token value
        
        Args:
            token: Refresh token to look up
            
        Returns:
            RefreshTokenDB object if found and valid, None otherwise
        """
        session = self.get_session()
        try:
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            db_token = session.query(RefreshTokenDB).filter(
                RefreshTokenDB.token_hash == token_hash,
                RefreshTokenDB.revoked == False,
                RefreshTokenDB.expires_at > datetime.utcnow()
            ).first()
            return db_token
        except Exception as e:
            logger.error(f"Error getting refresh token: {e}")
            return None
        finally:
            session.close()

    def revoke_refresh_token(self, token: str) -> bool:
        """
        Revoke a refresh token
        
        Args:
            token: Refresh token to revoke
            
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            db_token = session.query(RefreshTokenDB).filter(
                RefreshTokenDB.token_hash == token_hash
            ).first()
            
            if db_token:
                db_token.revoked = True
                session.commit()
                logger.info(f"Refresh token revoked for user ID={db_token.user_id}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error revoking refresh token: {e}")
            return False
        finally:
            session.close()

    def revoke_all_user_tokens(self, user_id: int) -> bool:
        """
        Revoke all refresh tokens for a user (logout from all devices)
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            session.query(RefreshTokenDB).filter(
                RefreshTokenDB.user_id == user_id,
                RefreshTokenDB.revoked == False
            ).update({"revoked": True})
            session.commit()
            logger.info(f"All refresh tokens revoked for user ID={user_id}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error revoking all tokens: {e}")
            return False
        finally:
            session.close()

    def cleanup_expired_tokens(self) -> int:
        """
        Delete expired refresh tokens from database
        
        Returns:
            Number of tokens deleted
        """
        session = self.get_session()
        try:
            result = session.query(RefreshTokenDB).filter(
                RefreshTokenDB.expires_at < datetime.utcnow()
            ).delete()
            session.commit()
            logger.info(f"Cleaned up {result} expired refresh tokens")
            return result
        except Exception as e:
            session.rollback()
            logger.error(f"Error cleaning up expired tokens: {e}")
            return 0
        finally:
            session.close()

    # ==================== TELEGRAM LINK CODES ====================

    def create_link_code(self, user_id: int) -> Optional[TelegramLinkCodeDB]:
        """
        Generate a unique link code for Telegram account linking
        
        Args:
            user_id: User ID to create link code for
            
        Returns:
            TelegramLinkCodeDB object if successful, None otherwise
        """
        session = self.get_session()
        try:
            # Invalidate any existing unused codes for this user
            existing_codes = session.query(TelegramLinkCodeDB).filter(
                TelegramLinkCodeDB.user_id == user_id,
                TelegramLinkCodeDB.used == False
            ).all()
            
            for code in existing_codes:
                code.used = True  # Mark as used to invalidate
                logger.info(f"Invalidated old link code {code.code} for user {user_id}")
            
            if existing_codes:
                session.commit()
            
            # Generate a unique 6-character code
            code = self._generate_unique_code(session)
            
            # Set expiration to 10 minutes from now
            expires_at = datetime.utcnow() + timedelta(minutes=10)
            
            # Create link code
            link_code = TelegramLinkCodeDB(
                user_id=user_id,
                code=code,
                expires_at=expires_at
            )
            
            session.add(link_code)
            session.commit()
            session.refresh(link_code)
            
            logger.info(f"Link code created for user {user_id}: {code}, expires_at={expires_at}")
            return link_code
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating link code: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
        finally:
            session.close()
    
    def _generate_unique_code(self, session: Session, length: int = 6) -> str:
        """
        Generate a unique alphanumeric code
        
        Args:
            session: Database session
            length: Length of the code (default 6)
            
        Returns:
            Unique code string
        """
        # Use uppercase letters and digits for readability
        characters = string.ascii_uppercase + string.digits
        
        # Try up to 10 times to generate a unique code
        for _ in range(10):
            code = ''.join(secrets.choice(characters) for _ in range(length))
            
            # Check if code already exists
            existing = session.query(TelegramLinkCodeDB).filter(
                TelegramLinkCodeDB.code == code
            ).first()
            
            if not existing:
                return code
        
        # If we couldn't generate a unique code after 10 tries, raise an error
        raise Exception("Failed to generate unique link code")
    
    def get_link_code(self, code: str) -> Optional[TelegramLinkCodeDB]:
        """
        Get a link code by its code string
        
        Args:
            code: The link code string
            
        Returns:
            TelegramLinkCodeDB object if found, None otherwise
        """
        session = self.get_session()
        try:
            link_code = session.query(TelegramLinkCodeDB).filter(
                TelegramLinkCodeDB.code == code
            ).first()
            return link_code
        except Exception as e:
            logger.error(f"Error getting link code: {e}")
            return None
        finally:
            session.close()
    
    def use_link_code(self, code: str, telegram_id: str) -> bool:
        """
        Mark a link code as used and link the telegram_id to the user
        
        Args:
            code: The link code string
            telegram_id: Telegram ID to link
            
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            # Get the link code (with lock to prevent race conditions)
            link_code = session.query(TelegramLinkCodeDB).filter(
                TelegramLinkCodeDB.code == code
            ).with_for_update().first()
            
            if not link_code:
                logger.warning(f"Link code not found: {code}")
                return False
            
            # Check if code is valid (not used and not expired)
            if not link_code.is_valid():
                logger.warning(f"Link code invalid or expired: {code}, used={link_code.used}, expired={link_code.is_expired()}")
                return False
            
            # Check if telegram_id is already linked to another user
            existing_user = session.query(UserDB).filter(
                UserDB.telegram_id == telegram_id
            ).first()
            
            if existing_user and existing_user.id != link_code.user_id:
                logger.warning(f"Telegram ID {telegram_id} already linked to user {existing_user.id}")
                return False
            
            # Check if target user already has a different telegram_id
            target_user = session.query(UserDB).filter(UserDB.id == link_code.user_id).first()
            if target_user and target_user.telegram_id and target_user.telegram_id != telegram_id:
                logger.warning(f"User {target_user.id} already has telegram_id {target_user.telegram_id}")
                return False
            
            # Mark code as used
            link_code.used = True
            link_code.telegram_id = telegram_id
            
            # Update user's telegram_id
            if target_user:
                target_user.telegram_id = telegram_id
                session.commit()
                logger.info(f"Telegram ID {telegram_id} linked to user {target_user.id}")
                return True
            
            return False
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error using link code: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
        finally:
            session.close()
    
    def cleanup_expired_link_codes(self) -> int:
        """
        Delete expired link codes from database
        
        Returns:
            Number of codes deleted
        """
        session = self.get_session()
        try:
            result = session.query(TelegramLinkCodeDB).filter(
                TelegramLinkCodeDB.expires_at < datetime.utcnow()
            ).delete()
            session.commit()
            logger.info(f"Cleaned up {result} expired link codes")
            return result
        except Exception as e:
            session.rollback()
            logger.error(f"Error cleaning up expired link codes: {e}")
            return 0
        finally:
            session.close()

    # ==================== BUDGET MANAGEMENT ====================

    def create_budget(self, user_id: str, category: str, amount: float, alert_threshold: float = 0.8) -> Optional[BudgetDB]:
        """
        Create a new budget for a user
        
        Args:
            user_id: User ID
            category: Category name
            amount: Monthly budget amount
            alert_threshold: Percentage at which to trigger alert (0.0 - 1.0)
            
        Returns:
            BudgetDB object if successful, None otherwise
        """
        session = self.get_session()
        try:
            # Check if budget already exists for this category
            existing = session.query(BudgetDB).filter(
                BudgetDB.user_id == user_id,
                BudgetDB.category == category,
                BudgetDB.is_active == True
            ).first()
            
            if existing:
                logger.warning(f"Budget already exists for user {user_id}, category {category}")
                return None
            
            budget = BudgetDB(
                user_id=user_id,
                category=category,
                amount=amount,
                alert_threshold=alert_threshold,
                is_active=True
            )
            session.add(budget)
            session.commit()
            session.refresh(budget)
            logger.info(f"Budget created: ID={budget.id}, User={user_id}, Category={category}")
            return budget
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating budget: {e}")
            return None
        finally:
            session.close()

    def get_user_budgets(self, user_id: str) -> List[BudgetDB]:
        """
        Get all active budgets for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of BudgetDB objects
        """
        session = self.get_session()
        try:
            budgets = session.query(BudgetDB).filter(
                BudgetDB.user_id == user_id,
                BudgetDB.is_active == True
            ).all()
            return budgets
        except Exception as e:
            logger.error(f"Error getting user budgets: {e}")
            return []
        finally:
            session.close()

    def get_budget_by_id(self, budget_id: int) -> Optional[BudgetDB]:
        """
        Get budget by ID
        
        Args:
            budget_id: Budget ID
            
        Returns:
            BudgetDB object if found, None otherwise
        """
        session = self.get_session()
        try:
            budget = session.query(BudgetDB).filter(BudgetDB.id == budget_id).first()
            return budget
        except Exception as e:
            logger.error(f"Error getting budget: {e}")
            return None
        finally:
            session.close()

    def update_budget(self, budget_id: int, **kwargs) -> Optional[BudgetDB]:
        """
        Update budget fields
        
        Args:
            budget_id: Budget ID
            **kwargs: Fields to update (amount, alert_threshold, is_active)
            
        Returns:
            Updated BudgetDB object if successful, None otherwise
        """
        session = self.get_session()
        try:
            budget = session.query(BudgetDB).filter(BudgetDB.id == budget_id).first()
            if budget:
                for key, value in kwargs.items():
                    if hasattr(budget, key) and value is not None:
                        setattr(budget, key, value)
                budget.updated_at = datetime.utcnow()
                session.commit()
                session.refresh(budget)
                logger.info(f"Budget updated: ID={budget_id}")
            return budget
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating budget: {e}")
            return None
        finally:
            session.close()

    def delete_budget(self, budget_id: int) -> bool:
        """
        Soft delete a budget (mark as inactive)
        
        Args:
            budget_id: Budget ID
            
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            budget = session.query(BudgetDB).filter(BudgetDB.id == budget_id).first()
            if budget:
                budget.is_active = False
                budget.updated_at = datetime.utcnow()
                session.commit()
                logger.info(f"Budget deleted: ID={budget_id}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting budget: {e}")
            return False
        finally:
            session.close()

    def get_budget_progress(self, user_id: str, year: int = None, month: int = None) -> List[dict]:
        """
        Get budget progress for all user budgets with current month spending
        
        Args:
            user_id: User ID
            year: Year to check (default: current year)
            month: Month to check (default: current month)
            
        Returns:
            List of dicts with budget info and spending progress
        """
        from sqlalchemy import func, extract, and_
        from calendar import monthrange
        
        session = self.get_session()
        try:
            now = datetime.now()
            year = year or now.year
            month = month or now.month
            
            # Get days in month for calculating days remaining
            _, days_in_month = monthrange(year, month)
            days_remaining = days_in_month - now.day
            
            # Get all active budgets for user
            budgets = session.query(BudgetDB).filter(
                BudgetDB.user_id == user_id,
                BudgetDB.is_active == True
            ).all()
            
            results = []
            
            for budget in budgets:
                # Get spending for this category in the specified month
                month_filter = and_(
                    ExpenseDB.user_id == user_id,
                    ExpenseDB.category == budget.category,
                    ExpenseDB.transaction_type == "expense",
                    extract('year', ExpenseDB.date) == year,
                    extract('month', ExpenseDB.date) == month
                )
                
                spent = (
                    session.query(func.sum(ExpenseDB.amount))
                    .filter(month_filter)
                    .scalar()
                    or 0
                )
                
                percentage_used = (spent / budget.amount) if budget.amount > 0 else 0
                alert_triggered = percentage_used >= budget.alert_threshold
                
                results.append({
                    "id": budget.id,
                    "category": budget.category,
                    "budget_amount": budget.amount,
                    "alert_threshold": budget.alert_threshold,
                    "spent": float(spent),
                    "remaining": float(budget.amount - spent),
                    "percentage_used": round(percentage_used * 100, 2),
                    "alert_triggered": alert_triggered,
                    "days_remaining": days_remaining
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting budget progress: {e}")
            return []
        finally:
            session.close()

    def get_budget_alerts(self, user_id: str) -> List[dict]:
        """
        Get active budget alerts for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of budget alerts that have triggered
        """
        progress = self.get_budget_progress(user_id)
        alerts = []
        
        for p in progress:
            if p["alert_triggered"]:
                if p["percentage_used"] >= 100:
                    severity = "danger"
                    message = f"⚠️ Has excedido tu presupuesto de {p['category']}: {p['percentage_used']:.0f}% usado"
                else:
                    severity = "warning"
                    message = f"📊 Estás cerca de tu límite en {p['category']}: {p['percentage_used']:.0f}% usado"
                
                alerts.append({
                    "budget_id": p["id"],
                    "category": p["category"],
                    "budget_amount": p["budget_amount"],
                    "spent": p["spent"],
                    "percentage_used": p["percentage_used"],
                    "message": message,
                    "severity": severity
                })
        
        return alerts
