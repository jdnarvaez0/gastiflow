"""
Script para listar todos los modelos de Gemini disponibles
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY no encontrado")
    exit(1)

print("🔍 Listando modelos de Gemini disponibles...\n")

genai.configure(api_key=api_key)

try:
    models = genai.list_models()

    print("📋 Modelos disponibles para generateContent:\n")

    for model in models:
        # Filtrar solo modelos que soporten generateContent
        if "generateContent" in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Nombre para usar: {model.name.replace('models/', '')}")
            print(f"   Descripción: {model.display_name}")
            print()

except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Posible solución: Verifica tu API Key en .env")
