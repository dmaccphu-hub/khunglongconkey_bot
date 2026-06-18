import logging
import urllib.parse
import urllib.request
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# === CẤU HÌNH THÔNG TIN ĐÃ ĐƯỢC LẮP SẴN ===
BOT_TOKEN = "8903651068:AAGKtA6hqtk-zUmM8YcxsKDU79NPSfi1SEk"
API_URL_WEB_1 = "https://link4m.co/api-v2?api=688d0212c6e84d0e055ba168&url="
API_URL_WEB_2 = "https://link4m.co/api-v2?api=688d0212c6e84d0e055ba168&url="
BASE_KEY = "khunglongkey1"
# ==========================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_daily_key():
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    today_day = datetime.now(tz).strftime("%d")
    return f"{BASE_KEY}-{today_day}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f"Chào {user.first_name}!, bấm /getkey để lấy Key hôm nay.")

async def getkey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    daily_key = get_daily_key()
    final_destination_url = f"https://google.com/search?q=Key+Cua+Ban+Hom+Nay+La:+{daily_key}"
    
    try:
        encoded_final_url = urllib.parse.quote(final_destination_url)
        api_call_2 = f"{API_URL_WEB_2}{encoded_final_url}"
        short_url_2 = urllib.request.urlopen(api_call_2).read().decode('utf-8').strip()
        
        encoded_short_url_2 = urllib.parse.quote(short_url_2)
        api_call_1 = f"{API_URL_WEB_1}{encoded_short_url_2}"
        short_url_1 = urllib.request.urlopen(api_call_1).read().decode('utf-8').strip()
        
        keyboard = [[InlineKeyboardButton("🔗 BẤM VÀO ĐÂY ĐỂ VƯỢT LINK LẤY KEY", url=short_url_1)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("HỆ THỐNG ĐÃ TẠO LINK VƯỢT 2 BƯỚC. Vui lòng hoàn thành vượt link để nhận Key hôm nay (Key tự đổi sau 12h đêm)!", reply_markup=reply_markup)
        print(f"User {update.effective_user.username} đã lấy link.")
        
    except Exception as e:
        await update.message.reply_text("Có lỗi xảy ra khi kết nối với hệ thống Link4M. Vui lòng thử lại sau!")
        print(f"Lỗi API Link4M: {e}")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getkey", getkey))
    application.run_polling()

if __name__ == '__main__':
    main()
def getkey(update: Update, context: CallbackContext) -> None:
    daily_key = get_daily_key()
    
    # 1. Tạo Link đích cuối cùng (Trang hiển thị Key sau khi vượt hết 2 link)
    final_destination_url = f"https://google.com/search?q=Key+Hom+Nay+La:+{daily_key}"
    
    try:
        # 2. Bọc tầng thứ 2: Biến link đích thành link rút gọn số 2
        encoded_final_url = urllib.parse.quote(final_destination_url)
        api_call_2 = f"{API_URL_WEB_2}{encoded_final_url}"
        short_url_2 = urllib.request.urlopen(api_call_2).read().decode('utf-8').strip()
        
        # 3. Bọc tầng thứ 1: Biến cái link rút gọn số 2 thành link rút gọn số 1
        encoded_short_url_2 = urllib.parse.quote(short_url_2)
        api_call_1 = f"{API_URL_WEB_1}{encoded_short_url_2}"
        short_url_1 = urllib.request.urlopen(api_call_1).read().decode('utf-8').strip()
        
        # Tạo nút bấm gửi cho người dùng (Nút này chứa link của Tầng 1)
        keyboard = [[InlineKeyboardButton("🔗 BẤM VÀO ĐÂY ĐỂ VƯỢT LINK LẤY KEY", url=short_url_1)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            "Hệ thống đã tạo Link vượt 2 bước.\nVui lòng hoàn thành vượt link để nhận Key của ngày hôm nay!",
            reply_markup=reply_markup
        )
        print(f"User {update.effective_user.username} đã lấy link vượt 2 tầng.")
        
    except Exception as e:
        update.message.reply_text("Có lỗi xảy ra khi tạo link vượt. Vui lòng thử lại sau!")
        print(f"Lỗi API: {e}")

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getkey", getkey))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
            f" HỆ THỐNG ĐÃ TẠO LINK VƯỢT 2 BƯỚC\n\n"
            f"Vui lòng hoàn thành vượt link để nhận Key của ngày hôm nay!\n"
            f"⚡ Lưu ý: Qua 12h đêm key sẽ tự động đổi sang ngày mới.",
            reply_markup=reply_markup
        )
        print(f"User {update.effective_user.username} đã lấy link vượt 2 tầng. Key hôm nay: {daily_key}")
        
    except Exception as e:
        update.message.reply_text("Có lỗi xảy ra khi kết nối với hệ thống Link4M. Vui lòng thử lại sau!")
        print(f"Lỗi API Link4M: {e}")

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getkey", getkey))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
def getkey(update: Update, context: CallbackContext) -> None:
    daily_key = get_daily_key()
    
    # 1. Tạo Link đích cuối cùng (Trang hiển thị Key sau khi vượt hết 2 link)
    final_destination_url = f"https://google.com/search?q=Key+Hom+Nay+La:+{daily_key}"
    
    try:
        # 2. Bọc tầng thứ 2: Biến link đích thành link rút gọn số 2
        encoded_final_url = urllib.parse.quote(final_destination_url)
        api_call_2 = f"{API_URL_WEB_2}{encoded_final_url}"
        short_url_2 = urllib.request.urlopen(api_call_2).read().decode('utf-8').strip()
        
        # 3. Bọc tầng thứ 1: Biến cái link rút gọn số 2 thành link rút gọn số 1
        encoded_short_url_2 = urllib.parse.quote(short_url_2)
        api_call_1 = f"{API_URL_WEB_1}{encoded_short_url_2}"
        short_url_1 = urllib.request.urlopen(api_call_1).read().decode('utf-8').strip()
        
        # Tạo nút bấm gửi cho người dùng (Nút này chứa link của Tầng 1)
        keyboard = [[InlineKeyboardButton("🔗 BẤM VÀO ĐÂY ĐỂ VƯỢT LINK LẤY KEY", url=short_url_1)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            "Hệ thống đã tạo Link vượt 2 bước.\nVui lòng hoàn thành vượt link để nhận Key của ngày hôm nay!",
            reply_markup=reply_markup
        )
        print(f"User {update.effective_user.username} đã lấy link vượt 2 tầng.")
        
    except Exception as e:
        update.message.reply_text("Có lỗi xảy ra khi tạo link vượt. Vui lòng thử lại sau!")
        print(f"Lỗi API: {e}")

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getkey", getkey))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
