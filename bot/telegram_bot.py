import os
from dotenv import load_dotenv
from core.parser import parse_request, allowed_types_str

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "TripPlannerLite MVP\n"
        "Send request in format:\n"
        "City DD.MM.YYYY-DD.MM.YYYY trip_type\n\n"
        f"Allowed trip types: {allowed_types_str()}\n"
        "Example: Prague 29.03.2025-02.04.2025 mixed"
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()

    try:
        req = parse_request(text)
    except ValueError as e:
        await update.message.reply_text(
            f"❌ Error: {e}\n\n"
            "Format: City DD.MM.YYYY-DD.MM.YYYY trip_type\n"
            f"Allowed trip types: {allowed_types_str()}"
        )
        return

    await update.message.reply_text(
        "✅ Parsed request:\n"
        f"City: {req['city']}\n"
        f"Dates: {req['start_date']} → {req['end_date']} ({req['days']} days)\n"
        f"Trip type: {req['trip_type']}"
    )

def main() -> None:
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Put it into .env")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()


if __name__ == "__main__":
    main()
