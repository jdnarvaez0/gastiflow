"""
Script simple para iniciar el bot sin verificaciones
Usa run_bot.py si quieres verificaciones completas
"""

from bot.main import main

if __name__ == "__main__":
    try:
        print("🤖 Iniciando bot de gastos...")
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Revisa bot_logs.log para más detalles")
