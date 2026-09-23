import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


TOKEN = os.environ["BOT_TOKEN"]
BASE_URL = os.environ["BASE_URL"]
PORT = int(os.environ.get("PORT", "10000"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 لیست قیمت امروز", callback_data="prices")],
        [InlineKeyboardButton("🛍 ثبت سفارش", callback_data="order")],
        [InlineKeyboardButton("🛒 سبد خرید", callback_data="cart")],
        [InlineKeyboardButton("📦 سفارش‌های من", callback_data="orders")],
        [InlineKeyboardButton("🔥 تخفیف‌های ویژه", callback_data="discounts")],
        [InlineKeyboardButton("☎️ ارتباط با فروشنده", callback_data="contact")],
    ]

    await update.message.reply_text(
        "🛒 به سیستم سفارش‌گیری فروش عمده خوش آمدید.\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "prices": "📋 بخش لیست قیمت به‌زودی فعال می‌شود.",
        "order": "🛍 بخش ثبت سفارش به‌زودی فعال می‌شود.",
        "cart": "🛒 سبد خرید شما فعلاً خالی است.",
        "orders": "📦 هنوز سفارشی ثبت نکرده‌اید.",
        "discounts": "🔥 تخفیف‌های ویژه به‌زودی نمایش داده می‌شوند.",
        "contact": "☎️ برای ارتباط با فروشنده با شماره/آیدی اعلام‌شده تماس بگیرید.",
    }

    await query.edit_message_text(
        messages.get(query.data, "گزینه نامعتبر است.")
    )


async def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("OK")


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("health", health))
    application.add_handler(CallbackQueryHandler(button))

    webhook_path = TOKEN
    webhook_url = f"{BASE_URL}/{webhook_path}"

    print("Bot is starting...")
    print(f"Webhook URL: {webhook_url}")

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=webhook_path,
        webhook_url=webhook_url,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
