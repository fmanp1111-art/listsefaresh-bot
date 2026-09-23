import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]


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
        reply_markup=InlineKeyboardMarkup(keyboard)
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

    await query.edit_message_text(messages.get(query.data, "گزینه نامعتبر است."))


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
