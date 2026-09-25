import os
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


TOKEN = os.environ["BOT_TOKEN"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]


def get_products():
    url = f"{SUPABASE_URL}/rest/v1/products"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response = requests.get(
        url,
        headers=headers,
        params={
            "select": "name,category,price",
            "available": "eq.true",
            "order": "category,name"
        },
        timeout=15
    )

    response.raise_for_status()
    return response.json()


def format_price(price):
    return f"{price:,}".replace(",", "٬")


def build_price_list(products):
    categories = {}

    for product in products:
        category = product.get("category") or "سایر"
        categories.setdefault(category, []).append(product)

    lines = ["📋 لیست قیمت امروز", ""]

    for category, items in categories.items():
        lines.append(f"🔹 {category}")
        for item in items:
            name = item["name"]
            price = format_price(item["price"])
            lines.append(f"• {name}: {price} تومان")
        lines.append("")

    return "\n".join(lines)


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

    if query.data == "prices":

        try:
            products = get_products()

            if not products:
                await query.edit_message_text(
                    "📋 در حال حاضر محصولی برای نمایش وجود ندارد."
                )
                return

            message = build_price_list(products)

            await query.edit_message_text(message)

        except Exception as e:
            print("Supabase error:", e)

            await query.edit_message_text(
                "❌ خطا در دریافت لیست قیمت.\n"
                "لطفاً کمی بعد دوباره تلاش کنید."
            )

        return

    messages = {
        "order": "🛍 بخش ثبت سفارش به‌زودی فعال می‌شود.",
        "cart": "🛒 سبد خرید شما فعلاً خالی است.",
        "orders": "📦 هنوز سفارشی ثبت نکرده‌اید.",
        "discounts": "🔥 تخفیف‌های ویژه به‌زودی نمایش داده می‌شوند.",
        "contact": "☎️ برای ارتباط با فروشنده با شماره/آیدی اعلام‌شده تماس بگیرید.",
    }

    await query.edit_message_text(
        messages.get(query.data, "گزینه نامعتبر است.")
    )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
