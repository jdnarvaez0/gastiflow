"""
Script para verificar el estado de tu cuota de Gemini API
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os
import time


def check_gemini_quota():
    print("=" * 60)
    print("🔍 VERIFICANDO CUOTA DE GEMINI API")
    print("=" * 60 + "\n")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ GEMINI_API_KEY no encontrado en .env")
        return

    print(f"📍 API Key: {api_key[:15]}...\n")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        print("🧪 Realizando 5 pruebas de requests consecutivos...\n")

        for i in range(1, 6):
            print(f"Request {i}/5...", end=" ")
            start_time = time.time()

            try:
                response = model.generate_content(f"Di solo el número {i}")
                elapsed = time.time() - start_time

                print(f"✅ OK ({elapsed:.2f}s) - Respuesta: {response.text.strip()}")

            except Exception as e:
                if "429" in str(e):
                    print(f"❌ ERROR 429 - Rate limit alcanzado")
                    print(f"\n⚠️  Has alcanzado el límite en el request {i}")
                    print("\n📊 Límites de Gemini (Free tier):")
                    print("   • 15 requests por minuto")
                    print("   • 1,500 requests por día")
                    print("   • 1 millón de tokens por minuto")
                    print("\n💡 Soluciones:")
                    print("   1. Espera 1-2 minutos antes de continuar")
                    print("   2. Reduce la frecuencia de requests")
                    print("   3. Considera usar un API Key diferente para testing")
                    print(
                        "   4. Revisa tu uso en: https://aistudio.google.com/app/apikey"
                    )
                    return
                else:
                    print(f"❌ ERROR: {e}")
                    return

            # Esperar 2 segundos entre requests
            if i < 5:
                time.sleep(2)

        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS PASARON")
        print("=" * 60)
        print("\n📊 Tu API Key está funcionando correctamente")
        print("💡 Recuerda esperar al menos 2 segundos entre requests")

    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        print("\n💡 Verifica:")
        print("   1. Que tu API Key sea válida")
        print("   2. Que tengas internet")
        print("   3. Que Gemini API esté disponible")


def show_gemini_limits():
    print("\n" + "=" * 60)
    print("📚 LÍMITES DE GEMINI API (Free Tier)")
    print("=" * 60 + "\n")

    print("⏱️  **Límites por tiempo:**")
    print("   • 15 requests por minuto")
    print("   • 1,500 requests por día")
    print("   • 1 millón de tokens por minuto\n")

    print("📊 **Límites por modelo:**")
    print("   • gemini-1.5-flash: 15 RPM (requests per minute)")
    print("   • gemini-1.5-pro: 2 RPM\n")

    print("💡 **Recomendaciones:**")
    print(
        "   • Espera 4 segundos entre requests para estar seguro (15/min = 1 cada 4s)"
    )
    print("   • Usa rate limiting en tu código")
    print("   • Monitorea tu uso en Google AI Studio")
    print("   • Considera upgrade si necesitas más\n")

    print("🔗 **Enlaces útiles:**")
    print("   • Dashboard: https://aistudio.google.com/app/apikey")
    print("   • Documentación: https://ai.google.dev/gemini-api/docs/quota")
    print("   • Precios: https://ai.google.dev/pricing\n")


if __name__ == "__main__":
    check_gemini_quota()
    show_gemini_limits()
