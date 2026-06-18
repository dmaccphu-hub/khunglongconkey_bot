import logging
import urllib.parse
import urllib.request
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# === CẤU HÌNH THÔNG TIN CHUẨN CỦA BẠN ===
BOT_TOKEN = "8903651068:AAGKtA6hqtk-zUmM8YcxsKDU79NPSfi1SEk"
API_URL_WEB_1 = "https://link4m.co/api-shorten/v2?api=688d0212c6e84d0e055ba168&url="
API_URL_WEB_2 = "https://link4m.co/api-shorten/v2?api=688d0212c6e84d0e055ba168&url="
BASE_KEY = "khunglongkey1"
# ==========================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_daily_key():
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    return f"{BASE_KEY}-{datetime.now(tz).strftime('%d')}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Chào {update.effective_user.first_name}!, bấm /getkey để lấy Key bản quyền hôm nay.")

async def getkey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    daily_key = get_daily_key()
    final_url = f"https://google.com/search?q=Key+Cua+Ban+Hom+Nay+La:+{daily_key}"
    try:
        url2 = urllib.request.urlopen(f"{API_URL_WEB_2}{urllib.parse.quote(final_url)}").read().decode('utf-8').strip()
        url1 = urllib.request.urlopen(f"{API_URL_WEB_1}{urllib.parse.quote(url2)}").read().decode('utf-8').strip()
        await update.message.reply_text("HỆ THỐNG ĐÃ TẠO LINK VƯỢT 2 BƯỚC. Vui lòng hoàn thành vượt link để nhận Key hôm nay!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔗 BẤM VÀO ĐÂY ĐỂ VƯỢT LINK LẤY KEY", url=url1)]]))
    except Exception as e:
        await update.message.reply_text("Có lỗi xảy ra khi kết nối với hệ thống Link4M. Vui lòng thử lại sau!")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getkey", getkey))
    application.run_polling()

if __name__ == '__main__':
    main()
