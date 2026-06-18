import logging
import urllib.parse
import urllib.request
import hashlib
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

# === CẤU HÌNH THÔNG TIN CỦA BẠN TẠI ĐÂY ===
BOT_TOKEN = "8903651068:AAGKtA6hqtk-zUmM8YcxsKDU79NPSfi1SEk"

# Web vượt tầng 1 (Người dùng sẽ phải vượt qua trang này đầu tiên)
API_URL_WEB_1 = "688d0212c6e84d0e055ba168"

# Web vượt tầng 2 (Sau khi vượt xong tầng 1, họ sẽ bị bắt vượt tiếp trang này)
API_URL_WEB_2 = "688d0212c6e84d0e055ba168"

SECRET_PASSWORD = "khunglongkeyq" 
# ==========================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_daily_key():
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    today_str = datetime.now(tz).strftime("%Y-%m-%d")
    raw_string = f"{today_str}_{SECRET_PASSWORD}"
    encoded_hash = hashlib.md5(raw_string.encode()).hexdigest().upper()
    return f"YONKI-{encoded_hash[:6]}"

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Chào {user.mention_markdown_v2()}\!, bấm /getkey để lấy Key bản quyền hôm nay nhé\.'
    )

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
