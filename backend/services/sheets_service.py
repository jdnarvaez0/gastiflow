import gspread
from google.oauth2.service_account import Credentials
from models.expense import ExpenseSchema
from datetime import datetime
from loguru import logger
from typing import Optional
import os
import json
import base64
import tempfile


class SheetsService:
    def __init__(self, credentials_file: str, sheet_id: str):
        """
        Inicializa el servicio de Google Sheets
        
        Soporta credenciales de dos formas:
        1. Variable de entorno GOOGLE_CREDENTIALS_B64 (Base64 encoded JSON) - para Railway/producción
        2. Archivo de credenciales JSON - para desarrollo local

        Args:
            credentials_file: Ruta al archivo JSON de credenciales (fallback)
            sheet_id: ID de la hoja de Google Sheets
        """
        self.credentials_file = credentials_file
        self.sheet_id = sheet_id

        # Scopes necesarios para Google Sheets
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        try:
            # Intentar cargar credenciales desde variable de entorno (producción)
            credentials_b64 = os.getenv("GOOGLE_CREDENTIALS_B64")
            
            if credentials_b64:
                logger.info("Cargando credenciales de Google desde variable de entorno")
                credentials_json = base64.b64decode(credentials_b64).decode('utf-8')
                credentials_info = json.loads(credentials_json)
                credentials = Credentials.from_service_account_info(
                    credentials_info, scopes=scopes
                )
            else:
                # Fallback: cargar desde archivo (desarrollo local)
                logger.info(f"Cargando credenciales de Google desde archivo: {credentials_file}")
                credentials = Credentials.from_service_account_file(
                    credentials_file, scopes=scopes
                )

            self.client = gspread.authorize(credentials)
            self.spreadsheet = self.client.open_by_key(sheet_id)

            # Inicializar la hoja principal
            self._initialize_sheet()

            logger.info("Google Sheets Service inicializado correctamente")

        except Exception as e:
            logger.error(f"Error inicializando Google Sheets: {e}")
            raise

    def _initialize_sheet(self):
        """
        Inicializa la hoja con los headers si no existen
        """
        try:
            # Intentar obtener la primera hoja
            worksheet = self.spreadsheet.sheet1

            # Verificar si tiene headers
            first_row = worksheet.row_values(1)

            if not first_row or first_row[0] != "ID":
                # Establecer headers
                headers = [
                    "ID",
                    "Usuario ID",
                    "Descripción",
                    "Monto",
                    "Moneda",
                    "Categoría",
                    "Tipo",
                    "Fecha",
                    "Fecha Creación",
                ]
                worksheet.update("A1:I1", [headers])

                # Formatear headers (opcional)
                worksheet.format(
                    "A1:I1",
                    {
                        "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
                        "textFormat": {
                            "bold": True,
                            "foregroundColor": {"red": 1, "green": 1, "blue": 1},
                        },
                    },
                )

                logger.info("Headers inicializados en Google Sheets")

        except Exception as e:
            logger.error(f"Error inicializando sheet: {e}")

    def add_expense(
        self, user_id: str, expense: ExpenseSchema, db_id: Optional[int] = None
    ) -> bool:
        """
        Añade un gasto a Google Sheets

        Args:
            user_id: ID del usuario de Telegram
            expense: Objeto ExpenseSchema con los datos del gasto
            db_id: ID del gasto en la base de datos (opcional)

        Returns:
            bool: True si se añadió correctamente, False en caso contrario
        """
        try:
            worksheet = self.spreadsheet.sheet1

            # Preparar los datos
            row = [
                db_id if db_id else "",
                user_id,
                expense.description,
                expense.amount,
                expense.currency,
                expense.category,
                expense.transaction_type,
                expense.date.isoformat(),
                datetime.now().isoformat(),
            ]

            # Añadir fila
            worksheet.append_row(row, value_input_option="USER_ENTERED")

            logger.info(f"Gasto añadido a Google Sheets: {expense.description}")
            return True

        except Exception as e:
            logger.error(f"Error añadiendo gasto a Sheets: {e}")
            return False

    def get_user_summary(self, user_id: str) -> dict:
        """
        Obtiene un resumen de gastos del usuario desde Google Sheets
        """
        try:
            worksheet = self.spreadsheet.sheet1

            # Obtener todos los valores
            all_values = worksheet.get_all_values()

            # Filtrar por usuario (asumiendo que usuario está en columna B, índice 1)
            user_expenses = [row for row in all_values[1:] if row[1] == user_id]

            if not user_expenses:
                return {"count": 0, "total": 0}

            # Calcular total
            total = sum(float(row[3]) for row in user_expenses if row[3])

            return {"count": len(user_expenses), "total": total}

        except Exception as e:
            logger.error(f"Error obteniendo resumen de Sheets: {e}")
            return {"count": 0, "total": 0}

    def create_user_worksheet(self, user_id: str) -> bool:
        """
        Crea una hoja separada para un usuario específico (opcional)
        """
        try:
            worksheet_name = f"Usuario_{user_id}"

            # Verificar si ya existe
            try:
                self.spreadsheet.worksheet(worksheet_name)
                logger.info(f"Worksheet {worksheet_name} ya existe")
                return True
            except gspread.exceptions.WorksheetNotFound:
                pass

            # Crear nueva worksheet
            worksheet = self.spreadsheet.add_worksheet(
                title=worksheet_name, rows=1000, cols=10
            )

            # Añadir headers
            headers = [
                "ID",
                "Descripción",
                "Monto",
                "Moneda",
                "Categoría",
                "Tipo",
                "Fecha",
                "Fecha Creación",
            ]
            worksheet.update("A1:H1", [headers])

            logger.info(f"Worksheet {worksheet_name} creada exitosamente")
            return True

        except Exception as e:
            logger.error(f"Error creando worksheet: {e}")
            return False
