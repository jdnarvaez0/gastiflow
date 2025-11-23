"""
Script de prueba para verificar la API de Gemini
"""

import google.generativeai as genai
from services.ai_processor import AIProcessor
from dotenv import load_dotenv
import os


def test_gemini_basic():
    """Test básico de Gemini API"""
    print("🔍 Probando conexión básica a Gemini API...")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY no encontrado en .env")
        return False

    print(f"📍 API Key: {api_key[:10]}...")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        print("\n🤖 Enviando mensaje de prueba a Gemini...")
        response = model.generate_content(
            "Di 'Todo funciona correctamente!' si puedes leer esto"
        )

        print(f"✅ Respuesta de Gemini: {response.text}")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que tu API Key sea correcta")
        print("   2. Ve a https://aistudio.google.com/apikey para obtener una nueva")
        print("   3. Asegúrate de que no haya espacios extra en el .env")
        return False


def test_ai_processor_text():
    """Test del procesador de texto"""
    print("\n" + "=" * 60)
    print("🔍 Probando AIProcessor con texto...")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    try:
        ai = AIProcessor(api_key)

        print("\n💬 Texto de entrada: 'Compré pan en la panadería por 500 pesos'")

        expense = ai.process_audio_text("Compré pan en la panadería por 500 pesos")

        if expense:
            print("✅ Gasto extraído correctamente:")
            print(f"   • Descripción: {expense.description}")
            print(f"   • Monto: ${expense.amount}")
            print(f"   • Moneda: {expense.currency}")
            print(f"   • Categoría: {expense.category}")
            print(f"   • Tipo: {expense.transaction_type}")
            return True
        else:
            print("❌ No se pudo extraer el gasto del texto")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_ai_processor_variations():
    """Test con diferentes variaciones de texto"""
    print("\n" + "=" * 60)
    print("🔍 Probando con diferentes formatos de texto...")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    test_cases = [
        "Gasté 1500 pesos en el supermercado",
        "Cena en restaurante 3000 ARS",
        "Pagué 50 dólares en Amazon",
        "Uber a casa, 800 pesos",
    ]

    try:
        ai = AIProcessor(api_key)

        for i, text in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: '{text}'")
            expense = ai.process_audio_text(text)

            if expense:
                print(
                    f"   ✅ Extraído: {expense.description} - ${expense.amount} {expense.currency} ({expense.category})"
                )
            else:
                print(f"   ❌ No se pudo procesar")

        print("\n✅ Pruebas de variaciones completadas")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    print("=" * 60)
    print("🧪 SUITE DE PRUEBAS PARA GEMINI API")
    print("=" * 60)

    # Test 1: Conexión básica
    success1 = test_gemini_basic()

    if not success1:
        print("\n⚠️  La prueba básica falló. Corrige el error antes de continuar.")
        return

    # Test 2: Procesador de texto
    success2 = test_ai_processor_text()

    # Test 3: Variaciones de texto
    success3 = test_ai_processor_variations()

    print("\n" + "=" * 60)
    if success1 and success2 and success3:
        print("✅ ¡TODAS LAS PRUEBAS DE GEMINI PASARON EXITOSAMENTE!")
        print("=" * 60)
        print("\n🎉 Tu bot está listo para procesar gastos con IA")
    else:
        print("⚠️  ALGUNAS PRUEBAS FALLARON")
        print("=" * 60)
        print("Revisa los errores arriba y corrígelos")


if __name__ == "__main__":
    main()
