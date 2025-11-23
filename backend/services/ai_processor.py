
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models.expense import ExpenseSchema
from typing import Optional
import json
import os
import time
from loguru import logger


class AIProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Modelo para visión (fotos)
        self.vision_model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Modelo LangChain para texto estructurado
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
            max_retries=3,  # Reintentos automáticos
            request_timeout=60  # Timeout de 60 segundos
        )
        
        # Parser para salida estructurada
        self.parser = PydanticOutputParser(pydantic_object=ExpenseSchema)
        
        # Control de rate limiting
        self.last_request_time = 0
        self.min_request_interval = 2  # Mínimo 2 segundos entre requests
        
    def _wait_for_rate_limit(self):
        """Espera el tiempo necesario para respetar el rate limit"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            wait_time = self.min_request_interval - time_since_last_request
            logger.info(f"⏳ Esperando {wait_time:.1f}s para respetar rate limit...")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    def process_image(self, image_path: str) -> Optional[ExpenseSchema]:
        """
        Procesa una imagen de factura y extrae información del gasto
        """
        try:
            # Respetar rate limit
            self._wait_for_rate_limit()
            
            # Leer la imagen
            with open(image_path, 'rb') as img_file:
                image_data = img_file.read()
            
            # Prompt para extraer información
            prompt = """Analiza esta factura/recibo y extrae la siguiente información:
            
            1. Descripción del gasto (resumen de lo comprado)
            2. Monto total (solo el número, sin símbolo de moneda)
            3. Moneda (ARS, USD, EUR, etc.)
            4. Categoría (elige una: Supermercado, Transporte, Restaurante, Entretenimiento, 
               Salud, Servicios, Educación, Ropa, Tecnología, Otros)
            5. Tipo de transacción: "expense" (gasto) o "income" (ingreso) - casi siempre es expense
            
            Responde ÚNICAMENTE en formato JSON con esta estructura exacta:
            {
                "description": "descripción del gasto",
                "amount": 100.50,
                "currency": "ARS",
                "category": "Supermercado",
                "transaction_type": "expense"
            }
            
            NO agregues texto adicional, solo el JSON."""
            
            # Generar contenido
            response = self.vision_model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
            
            # Parsear respuesta
            text_response = response.text.strip()
            
            # Limpiar markdown si existe
            if text_response.startswith("```json"):
                text_response = text_response.replace("```json", "").replace("```", "").strip()
            elif text_response.startswith("```"):
                text_response = text_response.replace("```", "").strip()
            
            logger.info(f"Respuesta de Gemini Vision: {text_response}")
            
            # Parsear JSON
            expense_data = json.loads(text_response)
            
            # Validar con Pydantic
            expense = ExpenseSchema(**expense_data)
            return expense
            
        except Exception as e:
            # Manejo específico de error 429
            if "429" in str(e) or "Resource exhausted" in str(e):
                logger.warning("⚠️ Rate limit alcanzado. Esperando 10 segundos...")
                time.sleep(10)
                logger.error(f"Error 429 procesando imagen: {e}")
                return None
            
            logger.error(f"Error procesando imagen: {e}")
            return None
    
    def process_audio_text(self, text: str) -> Optional[ExpenseSchema]:
        """
        Procesa un texto (de audio transcrito o mensaje de texto) y extrae información del gasto
        """
        try:
            # Respetar rate limit
            self._wait_for_rate_limit()
            
            prompt_template = """Eres un asistente que ayuda a registrar gastos. 
            El usuario te describe un gasto y debes extraer la información estructurada.
            
            Texto del usuario: {text}
            
            Extrae la siguiente información:
            1. Descripción del gasto
            2. Monto (solo número)
            3. Moneda (ARS, USD, EUR, etc. - si no se especifica, usa ARS)
            4. Categoría (elige una: Supermercado, Transporte, Restaurante, Entretenimiento, 
               Salud, Servicios, Educación, Ropa, Tecnología, Otros)
            5. Tipo: "expense" (gasto) o "income" (ingreso)
            
            {format_instructions}
            
            Responde ÚNICAMENTE con el JSON, sin texto adicional."""
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["text"],
                partial_variables={"format_instructions": self.parser.get_format_instructions()}
            )
            
            # Generar y parsear
            chain = prompt | self.llm | self.parser
            expense = chain.invoke({"text": text})
            
            logger.info(f"Gasto extraído del texto: {expense}")
            return expense
            
        except Exception as e:
            # Manejo específico de error 429
            if "429" in str(e) or "Resource exhausted" in str(e):
                logger.warning("⚠️ Rate limit alcanzado. Esperando 10 segundos...")
                time.sleep(10)
                logger.error(f"Error 429 procesando texto: {e}")
                return None
            
            logger.error(f"Error procesando texto: {e}")
            return None
    
    def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """
        Transcribe un archivo de audio usando Gemini
        """
        try:
            # Respetar rate limit
            self._wait_for_rate_limit()
            
            # Leer archivo de audio
            with open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            prompt = "Transcribe este audio a texto en español. Responde SOLO con la transcripción, sin texto adicional."
            
            response = self.vision_model.generate_content([
                prompt,
                {"mime_type": "audio/ogg", "data": audio_data}
            ])
            
            transcription = response.text.strip()
            logger.info(f"Audio transcrito: {transcription}")
            
            return transcription
            
        except Exception as e:
            # Manejo específico de error 429
            if "429" in str(e) or "Resource exhausted" in str(e):
                logger.warning("⚠️ Rate limit alcanzado. Esperando 10 segundos...")
                time.sleep(10)
                logger.error(f"Error 429 transcribiendo audio: {e}")
                return None
            
            logger.error(f"Error transcribiendo audio: {e}")
            return None