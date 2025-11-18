import aiohttp
import asyncio
import time
import html
from datetime import datetime, timedelta, date
from threading import Lock
from bs4 import BeautifulSoup
import requests
import tempfile
import subprocess, sys
import re
import random
import json
import os
import threading
import importlib
import sqlite3
import hashlib
import zipfile
import telebot
from gtts import gTTS
from io import BytesIO
from urllib.parse import urljoin, urlparse, urldefrag
from telebot import TeleBot, types  # type: ignore
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import pytz
from datetime import datetime, timedelta
from telebot.types import Message

ALLOWED_GROUP_ID = -1002866157499  # ID BOX
admin_diggory = "quana12999"
name_bot = "Bot Tiện ích"
zalo = "0327893606"
web = "Đang Cập Nhật"
facebook = "Đang Cập Nhật"
allowed_group_id = -5067820626 # ID BOX
users_keys = {}
freeuser = []
auto_spam_active = False
last_sms_time = {}
allowed_users = []
processes = []
ADMIN_ID = 7239343492  # ID ADMIN
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
last_command_time = {}
user_cooldowns = {}
share_count = {}
global_lock = Lock()
admin_mode = False
share_log = [] 

BOT_LINK = 'https://t.me/Test_A12bot/' 
TOKEN = '8404713686:AAF2SmOuGZwu-jcdwNr3ewCTAr-WgCrAbV0'
bot = TeleBot(TOKEN)
ADMIN_ID = 7239343492 # id admin
admins = {7239343492}
bot_admin_list = {}
cooldown_dict = {}
allowed_users = []
muted_users = {}

# ================================
# LỆNH /vidgai — LẤY LOGIC TỪ video_kinh_di.py
# ================================
VIDEO_FILE_GAI = "videos.json"

def load_videos_gai():
    try:
        with open(VIDEO_FILE_GAI, "r") as f:
            return json.load(f)
    except:
        return []

videos_gai = load_videos_gai()

@bot.message_handler(commands=["gaixinh"])
def send_video_gai(message):
    if len(videos_gai) == 0:
        return bot.reply_to(message, "⚠️ Hiện chưa có video nào!")

    file_id = random.choice(videos_gai)
    bot.send_video(
        message.chat.id,
        file_id,
        caption="📌 Video Gái Xinh Nè 😘\n\n⚠️ Nhớ giữ tâm hồn trong sáng!"
    )


def get_time_vietnam():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def check_command_cooldown(user_id, command, cooldown):
    current_time = time.time()

    if user_id in last_command_time and current_time - last_command_time[
            user_id].get(command, 0) < cooldown:
        remaining_time = int(cooldown -
                             (current_time -
                              last_command_time[user_id].get(command, 0)))
        return remaining_time
    else:
        last_command_time.setdefault(user_id, {})[command] = current_time
        return None


cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()


def create_user_table():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    expiration_time TEXT
                )''')
    conn.commit()
    conn.close()


def TimeStamp():
    now = str(date.today())
    return now


def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.now():
            allowed_users.append(user_id)


def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute(
        '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()


###
####
start_time = time.time()
load_users_from_database()


def load_allowed_users():
    try:
        with open('admin_vip.txt', 'r') as file:
            allowed_users = [int(line.strip()) for line in file]
        return set(allowed_users)
    except FileNotFoundError:
        return set()


vip_users = load_allowed_users()


###


@bot.message_handler(commands=['time'])
def handle_time(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    uptime_seconds = int(time.time() - start_time)

    uptime_days, remainder = divmod(uptime_seconds,
                                    86400)  # 1 ngày = 86400 giây
    uptime_hours, remainder = divmod(remainder, 3600)  # 1 giờ = 3600 giây
    uptime_minutes, uptime_seconds = divmod(remainder, 60)  # 1 phút = 60 giây

    bot.reply_to(
        message,
        f'<blockquote>⏰Bot đã hoạt động được: {uptime_days} ngày, {uptime_hours} giờ, {uptime_minutes} phút, {uptime_seconds} giây</blockquote>',
        parse_mode="HTML")


####
#####
video_url = 'https://files.catbox.moe/ivbkxo.MP4'

load_users_from_database()


@bot.message_handler(commands=['add', 'adduser'])
def add_user(message):
    admin_id = message.from_user.id
    auto_react_to_command(message)  # <- Thêm dòng này
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'MÁ CÓ PHẢI ADMIN ĐÂU')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.now() + timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    # Gửi video với tiêu đề
    caption_text = (
        f'<blockquote>NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /spamvip.</blockquote>'
    )
    bot.send_video(message.chat.id,
                   video_url,
                   caption=caption_text,
                   parse_mode="HTML")


def get_user_status(user_id):
    create_user_table()
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=? AND expiration_time > ?",
              (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    row = c.fetchone()
    conn.close()
    return "VIP" if row else "FREE"


@bot.message_handler(commands=["user"])
def check_user(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_status = get_user_status(user_id)
    auto_react_to_command(message)  # <- Thêm dòng này
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.reply_to(
        message,
        f"• User ID: {user_id}\n• Username: @{username}\n• Plan: {user_status}\n• Profile By @{username}\n• Timer : {current_time}"
    )

# --- Cấu hình KEY ---
REQUIRE_KEY = True   # Đặt True nếu muốn bắt buộc user nhập key, False nếu free

# Danh sách user đã dùng key
user_keys = {}

def check_user_key(user_id):
    """
    Kiểm tra key của user. 
    Trả về (ok, info)
    """
    if user_id not in user_keys:
        return False, {}
    
    key_info = user_keys[user_id]
    # Ví dụ: {"key": "abc123", "expiration_date": 1695822000}
    if time.time() > key_info.get("expiration_date", 0):
        return False, {}
    
    return True, key_info
    
@bot.message_handler(commands=['listvip'])
def list_vip_users(message):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    auto_react_to_command(message)  # <- Thêm dòng này

    # Lấy danh sách user VIP còn hạn sử dụng
    cursor.execute("SELECT user_id, expiration_time FROM users")
    vip_users = cursor.fetchall()
    conn.close()

    if not vip_users:
        bot.reply_to(message, "Hiện không có user VIP nào trong danh sách.")
        return

    vip_list = "Danh sách VIP:\n"
    now = datetime.now()

    for user_id, expiration_time in vip_users:
        expiration_time = datetime.strptime(expiration_time,
                                            '%Y-%m-%d %H:%M:%S')
        if expiration_time > now:
            vip_list += f"- ID: {user_id} - Hết hạn: {expiration_time}\n"

    bot.send_message(message.chat.id, vip_list, parse_mode="Markdown")


# Kết nối database
def get_db_connection():
    return sqlite3.connect("user_data.db")


# Lệnh để cộng thêm ngày VIP
@bot.message_handler(commands=['congvip'])
def add_vip_days(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message,
                         "Sai cú pháp! Dùng: /congvip <user_id> <days>",
                         parse_mode="Markdown")
            return

        user_id = int(args[1])
        days_to_add = int(args[2])

        conn = get_db_connection()
        cursor = conn.cursor()

        # Lấy ngày hết hạn hiện tại
        cursor.execute("SELECT expiration_time FROM users WHERE user_id = ?",
                       (user_id, ))
        result = cursor.fetchone()

        if result:
            current_expiration = datetime.strptime(result[0],
                                                   "%Y-%m-%d %H:%M:%S")
        else:
            # Nếu user chưa có, mặc định hết hạn từ hôm nay
            current_expiration = datetime.now()

        # Cộng thêm ngày
        new_expiration = current_expiration + timedelta(days=days_to_add)

        # Cập nhật vào database
        cursor.execute(
            "INSERT OR REPLACE INTO users (user_id, expiration_time) VALUES (?, ?)",
            (user_id, new_expiration.strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        conn.close()

        bot.reply_to(
            message, f"✅ Đã cộng {days_to_add} ngày VIP cho user {user_id}.\n"
            f"📅 Hạn mới: {new_expiration.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")


import time
import random
import string
import requests
import json
import logging
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO)

# Globals
LUUKEY_FILE = "luukey.json"
REQUIRE_KEY = True
verified_users = {}  # { user_id: expires_timestamp }

# ---------- Utils ----------
def load_keys():
    try:
        with open(LUUKEY_FILE, "r") as f:
            data = json.load(f)
            # Loại bỏ các key quá hạn
            now = time.time()
            valid_data = {int(k): v for k, v in data.items() if v.get("expires", 0) > now}
            return valid_data
    except Exception:
        return {}

def save_keys(data):
    try:
        with open(LUUKEY_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logging.error("Lỗi lưu key: %s", e)

stored_keys = load_keys()  # load khi bot start

def generate_key():
    rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"cdanhxconmeo-{rand_str}"

def check_user_key(user_id):
    try:
        uid = int(user_id)
    except:
        return False, {"reason": "user_id không hợp lệ"}

    exp = verified_users.get(uid)
    if not exp:
        return False, {"reason": "User chưa xác thực"}
    if time.time() > exp:
        verified_users.pop(uid, None)
        return False, {"reason": "Key xác thực đã hết hạn"}
    return True, {"reason": "OK", "expires": exp}

# ---------- Handler /getkey ----------
@bot.message_handler(commands=['getkey'])
def laykey(message):
    bot.reply_to(message, text='⏳ VUI LÒNG ĐỢI TRONG GIÂY LÁT!')
    user_id = int(message.from_user.id)
    key = generate_key()
    expires = time.time() + 24*3600  # 24h

    # Lưu vào stored_keys và lưu file
    stored_keys[user_id] = {"key": key, "expires": expires}
    save_keys(stored_keys)

    # Short link (fallback)
    try:
        res = requests.get(
            f'https://link4m.co/api-shorten/v2?api=68baa99bf1942d4d53695d39&url=http://103.157.204.177:5000/?id={key}',
            timeout=5
        ).json()
        url_key = res.get('shortenedUrl') or f'http://103.157.204.177:5000/?id={key}'
    except Exception:
        url_key = f'http://103.157.204.177:5000/?id={key}'

    text = (
        f"🔑 KEY CỦA BẠN {url_key}\n\n"
        f"👉 Vượt key xong dùng lệnh /key <mã-key>\n"
        "⚠️ Key này chỉ dùng để xác thực và hết hạn sau 24 giờ."
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="🔗 Mở Link Key", url=url_key),
        InlineKeyboardButton(text="👨‍💻 Admin", url="https://t.me/quana12999")
    )

    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=keyboard)

    # Thông báo admin
    try:
        bot.send_message(ADMIN_ID, f"🔔 User {user_id} tạo key: {key} (link: {url_key})")
    except:
        pass

    logging.info("Generated key for %s: %s", user_id, stored_keys.get(user_id))

# ---------- Handler /key ----------
@bot.message_handler(commands=['key'])
def key_handler(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, '⚠️ Bạn chưa nhập key!\n👉 Dùng /key <mã-key>')
        return

    user_id = int(message.from_user.id)
    key_input = parts[1].strip()

    entry = stored_keys.get(user_id)
    if not entry:
        bot.reply_to(message, '❌ Bạn chưa lấy key bằng /getkey hoặc key đã bị mất. Hãy /getkey trước.')
        return

    # Kiểm tra hết hạn
    if time.time() > entry.get("expires", 0):
        stored_keys.pop(user_id, None)
        save_keys(stored_keys)
        bot.reply_to(message, '❌ Key đã hết hạn. Vui lòng tạo key mới bằng /getkey.')
        return

    if entry.get("key") == key_input:
        # Xác thực thành công (7 ngày)
        verified_users[user_id] = time.time() + 7*24*3600
        stored_keys.pop(user_id, None)  # xóa key sau khi verify
        save_keys(stored_keys)
        bot.reply_to(message, '✅ KEY ĐÚNG! Bạn đã được xác thực thành công 🎉')
        logging.info("User %s verified until %s", user_id, verified_users[user_id])
    else:
        bot.reply_to(message, '❌ KEY KHÔNG HỢP LỆ! Vui lòng kiểm tra lại mã từ /getkey.')
        logging.info("User %s provided wrong key: %s (expected %s)", user_id, key_input, entry.get("key"))
        
   
# =================== LỆNH /KEY ===================
@bot.message_handler(commands=['off'])
def bot_off(message):
    global bot_active
    if message.from_user.id in admins:
        bot_active = False
        bot.reply_to(message, 'Bot đã được tắt.')
    else:
        bot.reply_to(message, 'Bạn không có quyền thực hiện thao tác này.')


@bot.message_handler(commands=['on'])
def bot_on(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    global bot_active
    if message.from_user.id in admins:
        bot_active = True
        bot.reply_to(message, 'Bot đã được bật.')
    else:
        bot.reply_to(message, 'Bạn không có quyền thực hiện thao tác này.')
        
        
@bot.message_handler(commands=['fb'])
def send_facebook_info(message):
    chat_id = message.chat.id
    message_id = message.message_id

    waiting = bot.reply_to(message, "🔍")
    user_input = message.text.split(maxsplit=1)

    if len(user_input) < 2:
        bot.send_message(chat_id, "❌ Vui lòng nhập UID hoặc Link sau lệnh /fb\n\n💬 Ví Dụ: <code>/fb 61574395204757</code> hoặc <code>/fb https://facebook.com/zuck</code>", parse_mode="HTML")
        bot.delete_message(chat_id, waiting.message_id)
        return

    fb_input = user_input[1].strip()

    if fb_input.isdigit():
        fb_id = fb_input
    else:
        fb_link = fb_input
        if not fb_link.startswith("http"):
            fb_link = "https://" + fb_link

        convert_api = f"https://offvnx.x10.bz/api/convertID.php?url={fb_link}"
        try:
            convert_res = requests.get(convert_api)
            if convert_res.status_code == 200:
                convert_data = convert_res.json()
                fb_id = str(convert_data.get("id", ""))
                if not fb_id.isdigit():
                    bot.send_message(chat_id, "❌ Không thể lấy UID từ link Facebook này! Vui lòng kiểm tra lại.")
                    bot.delete_message(chat_id, waiting.message_id)
                    return
            else:
                bot.send_message(chat_id, "❌ Lỗi khi kết nối API lấy UID.")
                bot.delete_message(chat_id, waiting.message_id)
                return
        except Exception as e:
            bot.send_message(chat_id, f"❌ Lỗi khi lấy UID từ link: {e}")
            bot.delete_message(chat_id, waiting.message_id)
            return

    api_url = f"https://offvnx.x10.bz/api/fb.php?id={fb_id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            data = response.json().get("result", {})

            if not isinstance(data, dict):
                bot.send_message(chat_id, "❌ Vui lòng kiểm tra lại, Có Thể Bạn Đã Nhập Sai Định Dạng")
                bot.delete_message(chat_id, waiting.message_id)
                return

            name = data.get("name", "Không công khai")
            username = data.get("username", "Chưa thiết lập")
            profile_id = data.get("id", "Chưa thiết lập")
            link = data.get("link", "https://www.facebook.com/")
            is_verified = data.get("is_verified", False)
            picture = data.get("picture", {}).get("data", {}).get("url", "")
            is_silhouette = data.get("picture", {}).get("data", {}).get("is_silhouette", True)
            created_time = data.get("created_time", "Không công khai")
            about = data.get("about", "Không công khai")
            locale = data.get("locale", "Không công khai")
            gender = data.get("gender", "Không công khai").capitalize()
            hometown = data.get("hometown", {}).get("name", "Không công khai")
            location = data.get("location", {}).get("name", "Không công khai")
            updated_time = data.get("updated_time", "Không công khai")
            timezone = data.get("timezone", "Không công khai")
            work = data.get("work", [])
            cover_photo = data.get("cover", {}).get("source", "")
            followers = data.get("followers", "Không công khai")
            following = data.get("following", "Không rõ số lượng đang theo dõi")
            relationship = data.get("relationship_status", "Không công khai")
            significant_other = data.get("significant_other", {})
            significant_other_name = significant_other.get("name", "Không công khai")
            significant_other_id = significant_other.get("id", "Không công khai")
            flag = data.get("country_flag", "")
            relationship_icon_text = data.get("relationship_status", "❓ Không công khai")

            work_info = ""
            if work:
                for job in work:
                    position = job.get("position", {}).get("name", "")
                    employer = job.get("employer", {}).get("name", "")
                    work_info += f"\n│ -> Làm việc tại {position} <a href='https://facebook.com/{username}'>{employer}</a>"
            else:
                work_info = "Không công khai"

            education_info = ""
            education = data.get("education", [])
            if education:
                for edu in education:
                    school = edu.get("school", {}).get("name", "Không công khai")
                    education_info += f"\n│ -> Học {edu.get('concentration', [{'name': ''}])[0]['name']} tại <a href='https://facebook.com/{username}'>{school}</a>"
            else:
                education_info = "Không công khai"

            verification_status = "Đã Xác Minh ✅" if is_verified else "Chưa xác minh ❌"

            significant_other_line = ""
            if significant_other_id not in ["Không công khai", "Chưa thiết lập", None, ""]:
                significant_other_line = (
                    f"│ -> 💍 Đã kết hôn với: <a href='https://facebook.com/{significant_other_id}'>{significant_other_name}</a>\n"
                    f"│ -> 🔗 Link UID: <code>https://facebook.com/{significant_other_id}</code>"
                )

            cover_photo_line = f"│ 𝗖𝗼𝘃𝗲𝗿 𝗣𝗵𝗼𝘁𝗼: <a href='{cover_photo}'>Xem ảnh bìa</a>" if cover_photo else "│ 𝗖𝗼𝘃𝗲𝗿 𝗣𝗵𝗼𝘁𝗼: Không có ảnh bìa ❌"
            profile_photo_line = f"│ 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗣𝗵𝗼𝘁𝗼: <a href='{picture}'>Xem ảnh đại diện</a>" if picture and not is_silhouette else "│ 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗣𝗵𝗼𝘁𝗼: Không có ảnh đại diện ❌"

            fb_info = f"""
<blockquote>╭─────────────⭓
│ 𝗡𝗮𝗺𝗲: <a href='{picture}'>{name}</a>
│ 𝗨𝗜𝗗: <a href='https://facebook.com/{profile_id}'>{profile_id}</a>
│ 𝗨𝘀𝗲𝗿 𝗡𝗮𝗺𝗲: <a href='https://facebook.com/{username}'>{username}</a>
{cover_photo_line}
{profile_photo_line}
│ 𝗟𝗶𝗻𝗸: {link}
│ 𝗕𝗶𝗿𝘁𝗵𝗱𝗮𝘆: {data.get("birthday", "Không hiển thị ngày sinh")}
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀: <a href='https://facebook.com/{profile_id}'>{followers}</a> Người theo dõi
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴: {following}
│ 𝗗𝗮𝘁𝗲 𝗖𝗿𝗲𝗮𝘁𝗲𝗱: {created_time}
│ 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻: {verification_status}
│ 𝗦𝘁𝗮𝘁𝘂𝘀: {relationship_icon_text}
{significant_other_line}
│ 𝗕𝗶𝗼: {about}
│ 𝗚𝗲𝗻𝗱𝗲𝗿: {gender}
│ 𝗛𝗼𝗺𝗲𝘁𝗼𝘄𝗻: {hometown}
│ 𝗟𝗼𝗰𝗮𝘁𝗶𝗼𝗻: {location}
│ 𝗪𝗼𝗿𝗸: {work_info}
│ 𝗘𝗱𝘂𝗰𝗮𝘁𝗶𝗼𝗻: {education_info}
│ 𝗔𝗯𝗼𝘂𝘁𝘀: {data.get("quotes", "Không có trích dẫn")}
├─────────────⭔
│ 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲: {flag}
│ 𝗧𝗶𝗺𝗲 𝗨𝗽𝗱𝗮𝘁𝗲: {updated_time}
╰─────────────⭓
</blockquote>
            """
            markup = InlineKeyboardMarkup()
            callback_data = f"delete_{chat_id}_{message.from_user.id}"
            delete_button = InlineKeyboardButton(text="🗑️ Xoá Tin Nhắn", callback_data=callback_data)
            markup.add(delete_button)

            bot.send_message(chat_id, fb_info, parse_mode='HTML', reply_markup=markup)
            bot.delete_message(chat_id, waiting.message_id)

        except Exception as e:
            bot.send_message(chat_id, f"Đã xảy ra lỗi khi xử lý dữ liệu: {str(e)}")
            bot.delete_message(chat_id, waiting.message_id)
    else:
        bot.send_message(chat_id, "❌ Vui lòng kiểm tra lại, Có Thể Bạn Đã Nhập Sai Định Dạng")
        bot.delete_message(chat_id, waiting.message_id)

    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Lỗi xóa lệnh: {e}")

# 👉 Xử lý callback xoá tin nhắn
@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def handle_delete_callback(call):
    try:
        _, msg_chat_id, msg_user_id = call.data.split("_")
        if str(call.from_user.id) != msg_user_id:
            bot.answer_callback_query(call.id, "❌ Bạn không có quyền xoá tin nhắn này.", show_alert=True)
            return
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        bot.answer_callback_query(call.id, f"Lỗi: {e}", show_alert=True)

# ========================
# HÀM DÙNG CHUNG
# ========================
def safe_get(data):
    return data if isinstance(data, dict) else {}

def ts_to_date(ts):
    try:
        if ts is None:
            return ""
        return datetime.fromtimestamp(int(ts)).strftime("%d/%m/%Y %H:%M:%S")
    except:
        return ""

def get_country_flag(region_code):
    try:
        if not region_code:
            return ""
        region_code = region_code.upper().strip()
        country_map = {
            "VN": "Việt Nam 🇻🇳", "SG": "Singapore 🇸🇬", "ID": "Indonesia 🇮🇩",
            "TH": "Thái Lan 🇹🇭", "PH": "Philippines 🇵🇭", "MY": "Malaysia 🇲🇾",
            "KH": "Campuchia 🇰🇭", "LA": "Lào 🇱🇦", "MM": "Myanmar 🇲🇲",
            "IN": "Ấn Độ 🇮🇳", "BD": "Bangladesh 🇧🇩", "BR": "Brazil 🇧🇷",
            "US": "Hoa Kỳ 🇺🇸", "KR": "Hàn Quốc 🇰🇷", "JP": "Nhật Bản 🇯🇵",
            "CN": "Trung Quốc 🇨🇳", "TW": "Đài Loan 🇹🇼", "HK": "Hồng Kông 🇭🇰",
        }
        if region_code in country_map:
            return country_map[region_code]
        if len(region_code) == 2:
            flag = chr(ord(region_code[0]) + 127397) + chr(ord(region_code[1]) + 127397)
            return f"{region_code} {flag}"
        return region_code
    except:
        return region_code

# ========================
import telebot
import requests
from io import BytesIO
from datetime import datetime
from html import escape   # <--- thêm dòng này
import time

OUTFIT_API_URL = "https://ffoutfitapis.vercel.app/outfit-image?uid={uid}&region={region}&key=99day"
PLAYER_INFO_API = "https://ffinfo-mu.vercel.app/player-info?uid={uid}&region={region}"
WISHLIST_API_URL = "https://ffwishlistapis.vercel.app/wish?uid={uid}&region={region}"
EVENTS_API_URL = "https://narayan-event.vercel.app/event?region={region}"
REGION_API_URL = 'https://danger-region-check.vercel.app/region?uid={uid}&key=DANGERxREGION'
BANCHECK_API_URL = 'https://ff.garena.com/api/antihack/check_banned?lang=en&uid={uid}'

# LỆNH /ff
# ========================
from html import escape
from datetime import datetime
import logging

# ================= CONFIG =================
logger = logging.getLogger(__name__)

# ================= HELPER FUNCTIONS =================
VALID_REGIONS = ['vn', 'sg']  # danh sách vùng hợp lệ

def is_valid_uid(uid):
    """Kiểm tra UID hợp lệ (8-11 chữ số)."""
    return uid.isdigit() and 8 <= len(uid) <= 11

def fetch_events(region):
    """Lấy danh sách sự kiện cho vùng (ví dụ tạm)."""
    if region not in VALID_REGIONS:
        return []
    return [
        {
            'Title': 'Sự kiện mẫu',
            'Start': '2025-09-25 10:00',
            'End': '2025-09-26 18:00',
            'Details': 'Chi tiết sự kiện mẫu.',
            'Banner': None,  # hoặc URL ảnh
            'link': 'https://example.com/event'
        }
    ]

def get_region_info(uid):
    """Lấy thông tin vùng từ UID (ví dụ tạm)."""
    if not is_valid_uid(uid):
        return {"error": True}
    return {"error": False, "nickname": "Người chơi mẫu", "region": "ind"}

def check_ban_status(uid, show_nickname=True):
    """Kiểm tra trạng thái ban (ví dụ tạm)."""
    if not is_valid_uid(uid):
        return "UID không hợp lệ."
    return "UID không bị cấm." if show_nickname else "Không bị cấm."

def format_time(dt_str):
    """Định dạng ngày giờ từ string."""
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return dt_str

# ================= BOT COMMANDS =================

@bot.message_handler(commands=['events'])
def events_command(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Cách dùng: /events <vùng>\nVí dụ: /events ind\n\nCác vùng hợp lệ: " + ", ".join(VALID_REGIONS))
            return
            
        region = parts[1].lower()
        
        processing_msg = bot.reply_to(message, f"Đang lấy thông tin sự kiện cho vùng `{region}`...", parse_mode="HTML")
        
        events = fetch_events(region)
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
        if not events:
            bot.reply_to(message, "Không tìm thấy sự kiện nào cho vùng này!", parse_mode="HTML")
            return
            
        for event in events:
            title = event.get('Title', 'N/A')
            start_date = format_time(event.get('Start'))
            end_date = format_time(event.get('End'))
            details = event.get('Details', '').strip()
            banner = event.get('Banner')
            link = event.get('link', '').strip()

            caption = f"🎉 <b>{title}</b> 🎉\n"
            caption += f"📅 <b>Ngày bắt đầu:</b> <code>{start_date}</code>\n"
            caption += f"⏳ <b>Ngày kết thúc:</b> <code>{end_date}</code>\n"
            if details:
                caption += f"📌 <b>Chi tiết:</b> {details}\n"
            if link:
                caption += f"🔗 <a href='{link}'>Liên kết sự kiện</a>"

            try:
                if banner:
                    bot.send_photo(message.chat.id, banner, caption=caption, parse_mode="HTML")
                else:
                    bot.send_message(message.chat.id, caption, parse_mode="HTML")
            except Exception as e:
                logger.error(f"Lỗi khi gửi sự kiện: {e}")
                bot.send_message(message.chat.id, caption, parse_mode="HTML")
                
    except Exception as e:
        bot.reply_to(message, f"❌ LỖI: {str(e)}")


import requests
from html import escape

@bot.message_handler(commands=['region'])
def region_command(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Cách dùng: /region <uid>\nVí dụ: /region 9253336019")
            return
        
        uid = parts[1]
        if not uid.isdigit() or not (8 <= len(uid) <= 11):
            bot.reply_to(message, "❌ UID không hợp lệ! UID phải có 8-11 chữ số.", parse_mode="HTML")
            return
        
        processing_msg = bot.reply_to(message, "⏳ Đang lấy thông tin...", parse_mode="HTML")
        
        # Gọi API lấy thông tin vùng
        url = f"https://danger-region-check.vercel.app/region?uid={uid}&key=DANGERxREGION"
        response = requests.get(url)
        region_info = response.json()
        
        if region_info.get("error"):
            bot.edit_message_text(
                "❌ Lỗi khi lấy thông tin. Vui lòng thử lại.",
                processing_msg.chat.id,
                processing_msg.message_id,
                parse_mode="HTML"
            )
            return
        
        # Chuẩn bị nội dung trả về
        msg = f"""🔍 THÔNG TIN VÙNG
────────────────────
👤 Tên: <code>{escape(region_info.get('nickname', 'N/A'))}</code>
🌎 Vùng: <code>{escape(region_info.get('region', 'N/A'))}</code>
❤️ Likes: <code>{region_info.get('likes', 0)}</code>
💎 Level: <code>{region_info.get('level', 0)}</code>
────────────────────
🔰 Developer: @cdanhdev"""
        
        bot.edit_message_text(
            msg,
            processing_msg.chat.id,
            processing_msg.message_id,
            parse_mode="HTML"
        )
        
    except Exception as e:
        bot.reply_to(message, f"❌ LỖI: {str(e)}")
        

@bot.message_handler(commands=['bancheck'])
def bancheck_command(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Cách dùng: /bancheck <uid>\nVí dụ: /bancheck 12345678")
            return
            
        uid = parts[1]
        if not is_valid_uid(uid):
            bot.reply_to(message, "UID không hợp lệ! UID phải có 8-11 chữ số.", parse_mode="HTML")
            return
            
        processing_msg = bot.reply_to(message, "Đang kiểm tra trạng thái cấm...", parse_mode="HTML")
        
        result = check_ban_status(uid, show_nickname=True)
        formatted_result = f"""────────────────────
{result}
────────────────────
🔰 Developer : @cdanhdev"""
        bot.edit_message_text(
            formatted_result,
            processing_msg.chat.id,
            processing_msg.message_id,
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"❌ LỖI: {str(e)}")


from datetime import datetime
from io import BytesIO
import requests
import time

# Chỉ hỗ trợ 2 region
VALID_REGIONS = ["vn", "sg"]

def convert_timestamp(ts):
    try:
        ts = int(ts)
        # Nếu timestamp > 1e12, coi là mili giây, chia 1000
        if ts > 1e12:
            ts = ts // 1000
        dt = datetime.fromtimestamp(ts)
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S")
        return date_str, time_str
    except:
        return "ɴ/ᴀ", "ɴ/ᴀ"


@bot.message_handler(commands=['infoff'])
def infoff(message):
    try:
        parts = message.text.strip().split()
        if len(parts) == 2:
            region = "vn"  # default là vn
            uid = parts[1]
        elif len(parts) == 3:
            region = parts[1].lower()
            uid = parts[2]
            if region not in VALID_REGIONS:
                bot.reply_to(message, ("❌ ɪɴᴠᴀʟɪᴅ ʀᴇɢɪᴏɴ. ᴠᴀʟɪᴅ ʀᴇɢɪᴏɴs: " + ", ".join(VALID_REGIONS)))
                return
        else:
            bot.reply_to(message, ("❌ ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ!\nᴜsᴀɢᴇ:\n• infoff <ᴜɪᴅ>\n• infoff <ʀᴇɢɪᴏɴ> <ᴜɪᴅ>"))
            return

        reply_to_msg = message.reply_to_message if message.reply_to_message else message

        url = f"https://ffinfo-mu.vercel.app/player-info?uid={uid}&region={region}"
        res = requests.get(url, timeout=15)
        
        if res.status_code != 200:
            res = requests.get(url, timeout=15)
            
        if res.status_code != 200:
            bot.reply_to(message, ("❌ ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴘʟᴀʏᴇʀ ɪɴғᴏ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ."))
            return

        try:
            data = res.json()
        except:
            bot.reply_to(message, ("❌ ɪɴᴠᴀʟɪᴅ ʀᴇsᴘᴏɴsᴇ ғʀᴏᴍ sᴇʀᴠᴇʀ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ."))
            return

        # === Xử lý dữ liệu ===
        if "AccountInfo" in data:
            account = data.get("AccountInfo", {})
            profile = data.get("AccountProfileInfo", {})
            captain = data.get("CaptainInfo", {})
            guild = data.get("GuildInfo", {})
            credit = data.get("CreditScoreInfo", {})
            pet = data.get("PetInfo", {})
            social = data.get("SocialInfo", {})
        elif "player_info" in data:
            player = data.get("player_info", {})
            account = player.get("basicInfo", {})
            profile = player.get("profileInfo", {})
            captain = player.get("captainBasicInfo", {})
            guild = player.get("clanBasicInfo", {})
            credit = data.get("creditScoreInfo", {})
            pet = data.get("petInfo", {})
            social = player.get("socialInfo", {})
        else:
            bot.reply_to(message, ("❌ ᴜɴᴋɴᴏᴡɴ ʀᴇsᴘᴏɴsᴇ ғᴏʀᴍᴀᴛ."))
            return

        # Lấy thông tin chung
        name = account.get("nickname", "ᴜɴᴋɴᴏᴡɴ")
        level = account.get("level", "ɴ/ᴀ")
        exp = account.get("exp", "ɴ/ᴀ")
        region = account.get("region", region.upper())
        liked = account.get("liked", "ɴ/ᴀ")
        title = account.get("title", "ɴ/ᴀ")
        release_version = account.get("releaseVersion", "ɴ/ᴀ")
        max_rank = account.get("maxRank", "ɴ/ᴀ")
        ranking_points = account.get("rankingPoints", "ɴ/ᴀ")
        cs_max_rank = account.get("csMaxRank", "ɴ/ᴀ")
        cs_ranking_points = account.get("csRankingPoints", "ɴ/ᴀ")
        created_at = account.get("createAt", "0")
        last_login_at = account.get("lastLoginAt", "0")
        banner_id = account.get("bannerId", "ɴ/ᴀ")
        badge_id = account.get("badgeId", "ɴ/ᴀ")
        
        avatar_id = profile.get("avatarId", "ɴ/ᴀ")
        clothes = profile.get("clothes", ["ɴ/ᴀ"])
        equiped_skills = profile.get("equipedSkills", ["ɴ/ᴀ"])
        
        pet_id = pet.get("id", "ɴ/ᴀ")
        pet_exp = pet.get("exp", "ɴ/ᴀ")
        pet_level = pet.get("level", "ɴ/ᴀ")
        
        guild_name = guild.get("clanName", "ɴᴏɴᴇ")
        guild_id = guild.get("clanId", "ɴ/ᴀ")
        guild_level = guild.get("clanLevel", "ɴ/ᴀ")
        member_num = guild.get("memberNum", "ɴ/ᴀ")
        
        captain_name = captain.get("nickname", "ɴ/ᴀ")
        captain_uid = captain.get("accountId", "ɴ/ᴀ")
        captain_level = captain.get("level", "ɴ/ᴀ")
        captain_exp = captain.get("exp", "ɴ/ᴀ")
        captain_created_at = captain.get("createAt", "0")
        captain_last_login = captain.get("lastLoginAt", "0")
        captain_title = captain.get("title", "ɴ/ᴀ")
        captain_ranking_points = captain.get("rankingPoints", "ɴ/ᴀ")
        captain_cs_points = captain.get("csRankingPoints", "ɴ/ᴀ")
        
        credit_score = credit.get("creditScore", "ɴ/ᴀ")
        bio = social.get("signature", "ɴᴏ ʙɪᴏ")

        # Convert timestamp
        created_date, created_time = convert_timestamp(created_at)
        login_date, login_time = convert_timestamp(last_login_at)
        captain_created_date, captain_created_time = convert_timestamp(captain_created_at)
        captain_login_date, captain_login_time = convert_timestamp(captain_last_login)

        # Gửi tin nhắn
        processing_msg = ("⏳")
        sent_msg = bot.reply_to(reply_to_msg, processing_msg, parse_mode="HTML")

        time.sleep(2)

        # Info text giữ nguyên
        info = (f"""<b>┌👤 ᴀᴄᴄᴏᴜɴᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
├─ ɴᴀᴍᴇ: {name}
├─ ᴜɪᴅ: {uid}
├─ ʟᴇᴠᴇʟ: {level}
├─ ᴇxᴘ: {exp}
├─ ʀᴇɢɪᴏɴ: {region}
├─ ʟɪᴋᴇs: {liked}
├─ ʜᴏɴᴏʀ sᴄᴏʀᴇ: {credit_score}
├─ ᴛɪᴛʟᴇ: {title}
└─ sɪɢɴᴀᴛᴜʀᴇ: {bio}

<b>➢ 🏆 ᴀᴄᴄᴏᴜɴᴛ sᴛᴀᴛɪsᴛɪᴄs</b>
├─ ɢᴀᴍᴇ ᴠᴇʀsɪᴏɴ: {release_version}
├─ ʙʀ ʀᴀɴᴋ: {ranking_points}
├─ ʙʀ ᴍᴀx ʀᴀɴᴋ:{max_rank}
├─ ᴄs ʀᴀɴᴋ: {cs_ranking_points}
├─ ᴄs ᴍᴀx ʀᴀɴᴋ: {cs_max_rank}
├─ ᴄʀᴇᴀᴛᴇᴅ ᴅᴀᴛᴇ: {created_date}
├─ ᴛɪᴍᴇ: {created_time}
├─ ʟᴀsᴛ ʟᴏɢɪɴ: {login_date}
└─ ᴛɪᴍᴇ: {login_time}

<b>➢ 👕 ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴘᴘᴇᴀʀᴀɴᴄᴇ</b>
├─ ʜᴇᴀᴅ ɪᴅ: {clothes[1] if len(clothes) > 1 else 'ɴ/ᴀ'}
├─ ғᴀᴄᴇ ᴘᴀɪɴᴛ ɪᴅ: {clothes[3] if len(clothes) > 3 else 'ɴ/ᴀ'}
├─ ᴍᴀꜱᴋ ɪᴅ: {clothes[5] if len(clothes) > 5 else 'ɴ/ᴀ'}
├─ ᴛᴏᴘ ɪᴅ: {clothes[2] if len(clothes) > 2 else 'ɴ/ᴀ'}
├─ ʙᴏᴛᴛᴏᴍ ɪᴅ: {clothes[0] if len(clothes) > 0 else 'ɴ/ᴀ'}
├─ sʜᴏᴇ ɪᴅ: {clothes[4] if len(clothes) > 4 else 'ɴ/ᴀ'}
├─ ᴀᴠᴀᴛᴀʀ ɪᴅ: {avatar_id}
├─ ʙᴀɴɴᴇʀ ɪᴅ: {banner_id}
└─ ʙᴀᴅɢᴇ ɪᴅ: {badge_id}

<b>➢ 🐾 ᴘᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
├─ ᴘᴇᴛ ʟᴇᴠᴇʟ: {pet_level}
├─ ᴘᴇᴛ ᴇxᴘ: {pet_exp}
└─ ᴘᴇᴛ ɪᴅ: {pet_id}

<b>➢ 🏰 ɢᴜɪʟᴅ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
├─ ɢᴜɪʟᴅ ɴᴀᴍᴇ: {guild_name}
├─ ɢᴜɪʟᴅ ɪᴅ: {guild_id}
├─ ɢᴜɪʟᴅ ʟᴇᴠᴇʟ: {guild_level}
└─ ᴍᴇᴍʙᴇʀs: {member_num}

<b>➢ 🧑‍✈️ ʟᴇᴀᴅᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
├─ ɴᴀᴍᴇ: {captain_name}
├─ ᴜɪᴅ: {captain_uid}
├─ ʟᴇᴠᴇʟ: {captain_level}
├─ ᴇxᴘ: {captain_exp}
├─ ᴄʀᴇᴀᴛᴇᴅ ᴅᴀᴛᴇ: {captain_created_date}
├─ ᴛɪᴍᴇ: {captain_created_time}
├─ ʟᴀsᴛ ʟᴏɢɪɴ: {captain_login_date}
├─ ᴛɪᴍᴇ: {captain_login_time}
├─ ᴛɪᴛʟᴇ: {captain_title}
├─ ʙʀ ᴘᴏɪɴᴛs: {captain_ranking_points}
└─ ᴄs ᴘᴏɪɴᴛs: {captain_cs_points}

ᴘᴜʙʟɪᴄ ᴄʀᴀꜰᴛʟᴀɴᴅ ᴍᴀᴘꜱ:
┌ 🗺️ ᴘᴜʙʟɪᴄ ᴄʀᴀꜰᴛʟᴀɴᴅ ᴍᴀᴘꜱ
➢ Not Found

🔰 ᴅᴇᴠᴇʟᴏᴘᴇʀ : @quandev
""")
        bot.edit_message_text(info, sent_msg.chat.id, sent_msg.message_id, parse_mode="HTML")

        # Banner & Outfit
        try:
            banner_url = f"https://gmg-avatar-banner.vercel.app/Gmg-avatar-banner?uid={uid}&region={region}&key=IDK"
            banner_res = requests.get(banner_url, timeout=10)
            if banner_res.status_code == 200:
                banner = BytesIO(banner_res.content)
                banner.name = "banner.webp"
                bot.send_sticker(chat_id=message.chat.id, sticker=banner, reply_to_message_id=message.message_id)
        except Exception as e:
            print(f"[banner error] {e}")

        try:
            outfit_url = f"https://ffoutfitapis.vercel.app/outfit-image?uid={uid}&region={region}&key=99day"
            outfit_res = requests.get(outfit_url, timeout=10)
            if outfit_res.status_code == 200:
                outfit = BytesIO(outfit_res.content)
                outfit.name = "outfit.jpg"
                bot.send_photo(chat_id=message.chat.id, photo=outfit, caption=f"👕 {name}'s ᴄʜᴀʀᴀᴄᴛᴇʀ ᴏᴜᴛғɪᴛ", reply_to_message_id=message.message_id)
        except Exception as e:
            print(f"[outfit error] {e}")

    except Exception as e:
        bot.reply_to(message, f"❌ ᴇʀʀᴏʀ: {str(e)}")
        
import json
import base64
import qrcode
import io

@bot.message_handler(commands=['loveqr'])
def create_love_qr(message):
    user_id = message.from_user.id  # thêm user_id để check key

    # 🔑 Kiểm tra key
    if REQUIRE_KEY:
        try:
            ok, info = check_user_key(user_id)
        except Exception:
            ok, info = False, {}
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    # Xử lý text nhập vào
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        return bot.reply_to(
            message,
            "<blockquote>💘 Cách dùng:</blockquote>\n<pre>/loveqr Light Love Suu💖</pre>",
            parse_mode="HTML"
        )

    user_text = args[1].strip()

    # Tạo payload base64
    payload = {
        "t": [user_text],
        "a": "nnca"
    }
    b64_data = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    final_url = f"https://taoanhdep.com/love/?b={b64_data}"

    # Tạo QR
    qr = qrcode.make(final_url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Gửi QR kèm caption
    caption = (
        "<blockquote>"
        f"<code>💗 Success Reg Qrcode Love Text: {user_text}</code>\n\n"
        f"🌐 <a href='{final_url}'> {final_url}</a>"
        "</blockquote>"
    )

    bot.send_photo(message.chat.id, photo=buffer, caption=caption, parse_mode="HTML")


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    chat_id = message.chat.id
    member_count = bot.get_chat_members_count(chat_id)

    for new_member in message.new_chat_members:
        user_id = new_member.id
        username = new_member.username
        first_name = new_member.first_name or "Người dùng"

        # Xử lý hiển thị tên người dùng
        if username:
            requester = f'@{username}'
        else:
            requester = f'<a href="tg://user?id={user_id}">{first_name}</a>'

        # Tin nhắn Welcome
        welcome_text = f"""
❖ 🎉 <b>Welcome</b> 🎉 ❖

<blockquote><b>Xin Chào</b> 👋! {requester}</blockquote>
<blockquote>➩ <b>Đã Tham Gia Nhóm:</b> {html.escape(message.chat.title)}</blockquote>
<blockquote>➩ <b>Số thành viên hiện tại:</b> {member_count}</blockquote>

▣ Dùng <b>/help</b> để xem tất cả lệnh của bot
"""

        # Inline buttons
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("👑 Admin", url="https://t.me/quana12999"),
            
        )
        keyboard.add(
            types.InlineKeyboardButton("💬 Nhóm chat", url="https://t.me/quana12999"),
            # types.InlineKeyboardButton("💥 Thuê bot ff", url="https://t.me/quana12999")
        )

        # Gửi Welcome kèm video
        video_url = "https://i.imgur.com/SRFiXrt.mp4"
        bot.send_video(
            chat_id,
            video_url,
            caption=welcome_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    import pytz
    from datetime import datetime

    user_id = message.from_user.id
    user_name = message.from_user.first_name

    bot.send_message(
        message.chat.id,
       f""" <b>🌌✨ MENU LỆNH HỆ THỐNG ✨🌌</b>

Thời Gian : {datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime('%H:%M:%S')}
Ngày : {datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime('%d/%m/%Y')}
Xin Chào: <a href='tg://user?id={user_id}'>{user_name}</a>

<b>🚀 LỆNH CƠ BẢN</b>
<blockquote>
🟣 /start — Hiển thị menu  
🔮 /getkey — Lấy key  
💎 /key — Nhập key  
📞 /admin — Liên hệ admin  
👤 /info — Thông tin Telegram  
💼 /muaplan — Nâng cấp gói  
🎫 /user — Trạng thái tài khoản  
📘 /cachdung — Hướng dẫn  
🔥 /infoff — Check Free Fire  
💗 /like — Buff like  
📘 /fb — Check Facebook  
📧 /reg — Email ảo  
🌤 /thoitiet — Dự báo thời tiết  
🎵 /tiktok — Tải TikTok  
🍑 /gaixinh — Video gái  
🎭 /nglink — Spam nglink  
🌐 /code — Lấy source Web  
🎙 /voice — Chuyển văn bản thành giọng  
🪪 /cccd — Tạo căn cước  
🌍 /dich — Dịch  
💖 /loveqr — Tạo web tỏ tình  
🎬 /film — Xem phim  
</blockquote>

<b>📨 SPAM SMS + CALL</b>
<blockquote>
⚡ /sms — Spam cơ bản  
🔥 /spam — Spam mạnh  
💥 /spamvip — Spam VIP  
🛑 /stop — Dừng spam  
🛑 /stopvip — Dừng spam VIP  
💰 /muavip — Mua VIP  
</blockquote>

<b>🛠 QUẢN TRỊ VIÊN</b>
<blockquote>
👑 /add — Thêm user  
📵 /bansdt — Ban số  
📢 /thongbao — Gửi broadcast  
💎 /congvip — Cộng VIP  
🏅 /listvip — Danh sách VIP  
🎁 /regcode — Tạo code  
🔧 /baotri — Bảo trì lệnh  
</blockquote>

<b>🔥 FREE FIRE</b>
<blockquote>
/5s — Mời Team 5  
/6s — Mời Team 6  
💸 /giabot — Giá bot  
🤖 /thuebot — Thuê bot  
🌍 /region — Xem region  
🚫 /checkban — Check ban  
✨ /visitff — Visit buff  
</blockquote>

<b>🎲 GAME TAIXIU</b>
<blockquote>
/taixiu — Menu  
/dangky — Đăng ký  
/tk — Nhập tên  
/mk — Tạo mật khẩu  
/dangnhap — Đăng nhập  
/thongtin — Xem tài khoản  
/tangxu — Tặng xu  
/batdau — Bắt đầu  
/top10 — BXH  
/showcode — Code  
/code — Nhập code  
</blockquote>

<b>🎨 TIỆN ÍCH KHÁC</b>
<blockquote>
▶️ /ytb — YouTube  
🖼 /taoanh — Tạo ảnh AI  
🔳 /qr — Mã QR  
🍀 /anhgai — Ảnh API  
⏱ /time — Uptime bot  
</blockquote>

━━━━━━━━━━━━━━━━━━

<b>Thông tin thêm:</b>
<blockquote>
Bot hỗ trợ spam SMS + Call ẩn danh. Tin nhắn sẽ tự động xóa để tránh bị phát hiện.
</blockquote>
""",
    parse_mode="HTML"
)
        
@bot.message_handler(commands=['admin'])
def diggory(message):

    username = message.from_user.username
    bot.reply_to(
        message, f'''
┌───⭓ {name_bot}
│» Xin chào @{username}
│» Bot Spam : Bot By Quân Dev-A12
│» Zalo: {zalo}
│» Website: {web}
│» Telegram: @{admin_diggory}
└──────────────
    ''')

blacklist = {}
last_usage = {}
# Load blacklist từ file JSON
SPAM_PROCESSES = {} 
active_processes = {}  # Lưu PID theo SĐT
def hide_phone_number(phone_number):
    if len(phone_number) <8:  # Kiểm tra số điện thoại có hợp lệ để ẩn hay không
        return phone_number
    return phone_number[:4] + "****" + phone_number[-2:]
@bot.message_handler(commands=['spam'])
def spam(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id

    # Kiểm tra key NGAY LÚC ĐẦU để tránh tốn tài nguyên nếu chưa có key
    if REQUIRE_KEY:
        try:
            ok, info = check_user_key(user_id)
        except Exception:
            ok, info = False, {}
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    # Gọi phản ứng tự động (nếu có)
    try:
        auto_react_to_command(message)
    except Exception:
        pass

    # Xóa tin nhắn lệnh của user (nếu bot có quyền)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass  # Bỏ qua nếu không xóa được

    # --- tiếp tục phần xử lý spam như bạn muốn ---
    # (ví dụ: phân tích args, kiểm tra rate limit, blacklist, chạy subprocess, v.v.)
    # ====== Phần xử lý spam ======
    processing_msg = None
    try:
        processing_msg = bot.send_message(
            chat_id,
            f"⏳ <a href='tg://user?id={user_id}'>{user_name}</a>, đang xử lý SMS...",
            parse_mode="HTML"
        )
    except Exception:
        # Nếu gửi message ban đầu fail thì vẫn tiếp tục, nhưng không thể edit sau này
        processing_msg = None

    # Tạo keyboard
    keyboard = types.InlineKeyboardMarkup()
    url_button1 = types.InlineKeyboardButton("🔥 Buy Vip", url='https://t.me/quana12999')
    keyboard.add(url_button1)

    # Lấy tham số từ message
    params = message.text.split()[1:]
    if len(params) != 2:
        text = "/spam SĐT Số lần\nVD: /spam 0123456789 5"
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id)
        else:
            bot.send_message(chat_id, text)
        return

    sdt, count = params

    if not count.isdigit():
        text = "Số lần spam không hợp lệ. Vui lòng chỉ nhập số."
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id)
        else:
            bot.send_message(chat_id, text)
        return

    count = int(count)

    if count > 5:
        text = "<blockquote>Lệnh này tối đa là 5 lần !!!</blockquote>"
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id, parse_mode="HTML")
        else:
            bot.send_message(chat_id, text, parse_mode="HTML")
        return

    if sdt in blacklist:
        text = f"🚫 Số điện thoại {sdt} đã bị cấm spam."
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id)
        else:
            bot.send_message(chat_id, text)
        return

    current_time = time.time()
    if user_id in last_usage and current_time - last_usage[user_id] < 60:
        wait_time = int(60 - (current_time - last_usage[user_id]))
        text = f"⏳ Vui lòng đợi {wait_time} giây trước khi dùng lệnh lại."
        if processing_msg:
            bot.edit_message_text(text, chat_id, processing_msg.message_id)
        else:
            bot.send_message(chat_id, text)
        return

    last_usage[user_id] = current_time
    hidden_sdt = hide_phone_number(sdt)

    # Gửi video xác nhận spam
    video_url = "https://files.catbox.moe/wri854.mp4"
    try:
        bot.send_video(
            chat_id,
            video_url,
            caption=(
                f"<blockquote><b>┌──⭓ SPAM SMS💳</b>\n"
                f"<b>│</b> 🚀 <b>Attack Sent Successfully</b>\n"
                f"<b>│</b> 💳 <b>Plan Free:</b> Min 1 | Max 5\n"
                f"<b>│</b> 📞 <b>Phone:</b> {hidden_sdt}\n"
                f"<b>│</b> ⚔️ <b>Attack By:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n"
                f"<b>│</b> 🔗 <b>API:</b> 1x\n"
                f"<b>│</b> ⏳ <b>Delay:</b> 20s\n"
                f"<b>│</b> 📎 <b>Vòng Lặp:</b> <code>{count}</code>\n"
                f"<b>└────────────⭓</b></blockquote>"
                f"<pre>Dừng: /stop SĐT\n/stop {sdt}</pre>"
            ),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        # Nếu gửi video thất bại, vẫn tiếp tục chạy script (tùy bạn)
        try:
            bot.send_message(chat_id, f"⚠️ Không thể gửi video xác nhận: {e}")
        except Exception:
            pass

    # --- CHẠY SCRIPT test1.py ---
    script_filename = "test1.py"
    try:
        if not os.path.isfile(script_filename):
            bot.send_message(chat_id, "⚠️ Không tìm thấy file script `test1.py`.")
            return

        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Chạy script với tham số sdt và count
        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        # Lưu PID để dùng /stop
        active_processes[sdt] = process.pid
    except Exception as e:
        bot.send_message(chat_id, f"❌ Lỗi chạy script: {str(e)}")
        


@bot.message_handler(commands=['sms'])
def sms(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id

    # Kiểm tra key NGAY LÚC ĐẦU để tránh tốn tài nguyên
    if REQUIRE_KEY:
        ok, info = check_user_key(user_id)
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    # Phản ứng tự động (nếu có)
    try:
        auto_react_to_command(message)
    except Exception:
        pass

    # Xóa lệnh người dùng (nếu có quyền)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass

    # Thông báo đang xử lý
    processing_msg = bot.send_message(
        chat_id,
        f"⏳ <a href='tg://user?id={user_id}'>{user_name}</a>, đang xử lý SMS...",
        parse_mode="HTML"
    )

    # Inline keyboard (quảng cáo / buy vip)
    keyboard = types.InlineKeyboardMarkup()
    url_button1 = types.InlineKeyboardButton("🔥 Buy Vip", url='https://t.me/quana12999')
    keyboard.add(url_button1)

    # Lấy tham số
    params = message.text.split()[1:]
    if len(params) != 2:
        bot.edit_message_text(
            "/sms SĐT số lần\nVD: /sms 0123456789 5\nSĐT Viết Liền Nhau.",
            chat_id,
            processing_msg.message_id
        )
        return

    sdt, count = params

    if not count.isdigit():
        bot.edit_message_text(
            "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.",
            chat_id,
            processing_msg.message_id
        )
        return

    count = int(count)

    if count > 5:
        bot.edit_message_text(
            "<blockquote>Lệnh này tối đa là 5 lần !!!</blockquote>",
            chat_id,
            processing_msg.message_id,
            parse_mode="HTML"
        )
        return

    if sdt in blacklist:
        bot.edit_message_text(
            f"🚫 Số điện thoại {sdt} đã bị cấm spam.",
            chat_id,
            processing_msg.message_id
        )
        return

    # Rate limit per user (60s)
    current_time = time.time()
    if user_id in last_usage and current_time - last_usage[user_id] < 60:
        wait_time = int(60 - (current_time - last_usage[user_id]))
        bot.edit_message_text(
            f"⏳ Vui lòng đợi {wait_time} giây trước khi dùng lệnh lại.",
            chat_id,
            processing_msg.message_id
        )
        return

    last_usage[user_id] = current_time
    hidden_sdt = hide_phone_number(sdt)

    # Gửi thông báo (video + nội dung)
    video_url = "https://files.catbox.moe/wri854.mp4"
    try:
        sent_video = bot.send_video(
            chat_id,
            video_url,
            caption=(
                f"<blockquote><b>┌──⭓ SPAM SMS FREE💳</b>\n"
                f"<b>│</b> 🚀 <b>Attack Sent Successfully</b>\n"
                f"<b>│</b> 💳 <b>Plan Free:</b> Min 1 | Max 5\n"
                f"<b>│</b> 📞 <b>Phone:</b> {hidden_sdt}\n"
                f"<b>│</b> ⚔️ <b>Attack By:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n"
                f"<b>│</b> 🔗 <b>Api:</b> 1x (MAX)\n"
                f"<b>│</b> ⏳ <b>Delay:</b> 20s\n"
                f"<b>│</b> 📎 <b>Vòng Lặp:</b> <code>{count}</code>\n"
                f"<b>└────────────⭓</b></blockquote>\n"
                f"<pre>Dừng: /stop SĐT\n/stop 0987654321</pre>"
            ),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception:
        # Nếu không gửi được video thì chỉ edit tin nhắn processing
        try:
            bot.edit_message_text(
                f"✅ Đã gửi lệnh spam cho {hidden_sdt} (vòng lặp: {count})",
                chat_id,
                processing_msg.message_id
            )
        except Exception:
            pass

    # Chạy script spam SMS (tạo temp file và chạy subprocess)
    script_filename = "cc.py"
    try:
        if not os.path.isfile(script_filename):
            bot.edit_message_text("Không tìm thấy file script. Vui lòng kiểm tra lại.", chat_id, processing_msg.message_id)
            return

        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Khởi chạy subprocess (không chặn)
        process = subprocess.Popen([sys.executable, temp_file_path, sdt, str(count)])

        # Bạn có thể lưu process.pid nếu cần dừng sau bằng /stop
        running_processes[user_id] = {
            "pid": process.pid,
            "temp_file": temp_file_path,
            "target": sdt
        }

    except FileNotFoundError:
        bot.edit_message_text("Không tìm thấy file.", chat_id, processing_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Lỗi xảy ra: {str(e)}", chat_id, processing_msg.message_id)
        

active_spams = {}

@bot.message_handler(commands=['stop'])
def stop(message):
    params = message.text.split()[1:]
    auto_react_to_command(message)  # <- Thêm dòng này
    if len(params) != 1:
        bot.reply_to(message, "🔴 Dùng lệnh: /stop SĐT\nVD: /stop 0123456789")
        return

    sdt = params[0]

    if sdt not in active_processes:
        bot.reply_to(message, f"❌ Không có tiến trình nào đang chạy cho SĐT {sdt}.")
        return

    try:
        os.kill(active_processes[sdt], 9)  # Dừng process
        del active_processes[sdt]  # Xóa khỏi danh sách
        bot.reply_to(message, f"🛑 Đã dừng spam cho {sdt}.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi khi dừng spam: {e}")





blacklist = ["1",
    "2", "3", "4"
]


# Xử lý lệnh /spamvip
def is_valid_phone(phone):
    return bool(re.fullmatch(r"0\d{9}", phone))
@bot.message_handler(commands=['spamvip'])
def spamvip(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id
    auto_react_to_command(message)  # <- Thêm dòng này

    if user_id not in allowed_users:
        bot.reply_to(message, 'Mua Vip Liên Hệ ADMIN @quana12999')
        return

    # Xóa tin nhắn của user
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

    # Bot gửi thông báo "Đang xử lý..."
    processing_msg = bot.send_message(chat_id, f"⏳ <a href='tg://user?id={user_id}'>{user_name}</a>, đang xử lý SMS...", parse_mode="HTML")

    keyboard = types.InlineKeyboardMarkup()
    url_button1 = types.InlineKeyboardButton("🔥 Buy Vip", url='https://t.me/quana12999')
    keyboard.add(url_button1)


    params = message.text.split()[1:]
    if len(params) != 2:
        bot.edit_message_text("/spamvip SĐT Số_lần\nVD: /spamvip 0123456789 1000", chat_id, processing_msg.message_id)
        return

    sdt, count = params

    if not count.isdigit():
        bot.edit_message_text("Số lần spam không hợp lệ. Vui lòng chỉ nhập số.", chat_id, processing_msg.message_id)
        return

    count = int(count)

    if count > 1000:
        bot.edit_message_text("<blockquote>Lệnh này tối đa là 1000 lần !!!</blockquote>", chat_id, processing_msg.message_id, parse_mode="HTML")
        return

    if sdt in blacklist:
        bot.edit_message_text(f"🚫 Số điện thoại {sdt} đã bị cấm spam.", chat_id, processing_msg.message_id)
        return

    current_time = time.time()
    if user_id in last_usage and current_time - last_usage[user_id] < 20:
        wait_time = int(20 - (current_time - last_usage[user_id]))
        bot.edit_message_text(f"⏳ Vui lòng đợi {wait_time} giây trước khi dùng lệnh lại.", chat_id, processing_msg.message_id)
        return

    last_usage[user_id] = current_time
    hidden_sdt = hide_phone_number(sdt)

    # Cập nhật tin nhắn thành kết quả spam
    video_url = "https://files.catbox.moe/ojg5t7.mp4"
    sent_video = bot.send_video(
        chat_id, 
        video_url, processing_msg.message_id,
        caption=(
            f"<blockquote><b>┌──⭓ SPAM SMS VIP💎🚀</b>\n"
            f"<b>│</b> 🚀 <b>Attack Sent Successfully</b>\n"
            f"<b>│</b> 💳 <b>Plan Vip:</b> Min 1 | Max 1000\n"
            f"<b>│</b> 📞 <b>Phone:</b> {hidden_sdt}\n"
            f"<b>│</b> ⚔️ <b>Attack By:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n"
            f"<b>│</b> 🔗 <b>Api:</b> 10x (MAX)\n"
            f"<b>│</b> ⏳ <b>Delay:</b> 20s\n"
            f"<b>│</b> 📎 <b>Vòng Lặp:</b> <code>{count}</code>\n"
            f"<b>└────────────⭓</b></blockquote>\n"
            f"<pre>Dừng: /stopvip SĐT\n/stopvip 0987654321\nCÁM ƠN MN ỦNG HỘ VIP NHÉ.</pre>"
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )

    # Chạy script spam SMS
    script_filename = "test1.py"
    try:
        if not os.path.isfile(script_filename):
            bot.edit_message_text("Không tìm thấy file script. Vui lòng kiểm tra lại.", chat_id, processing_msg.message_id)
            return

        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        # Lưu PID và user_id vào active_processes
        active_processes[sdt] = {'pid': process.pid, 'user_id': user_id}
    except FileNotFoundError:
        bot.edit_message_text("Không tìm thấy file.", chat_id, processing_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Lỗi: {e}", chat_id, processing_msg.message_id)


active_spams = {}



@bot.message_handler(commands=['stopvip'])
def stopvip(message):
    user_id = message.from_user.id
    auto_react_to_command(message)  # <- Thêm dòng này
    if user_id not in allowed_users:
        bot.reply_to(message, 'Mua Vip Liên Hệ ADMIN @quana12999.')
        return
    params = message.text.split()[1:]
    if len(params) != 1:
        bot.reply_to(message, "🔴 Dùng lệnh: /stopvip SĐT\nVD: /stopvip 0123456789")
        return

    sdt = params[0]
    user_id = message.from_user.id  # Lấy user_id của người gửi lệnh

    # Kiểm tra xem tiến trình cho số điện thoại có tồn tại không
    if sdt not in active_processes:
        bot.reply_to(message, f"❌ Không có tiến trình nào đang chạy cho SĐT {sdt}.")
        return

    # Kiểm tra xem người dừng có phải là người đã kích hoạt spam không
    if active_processes[sdt].get('user_id') != user_id:
        bot.reply_to(message, f"⚠️ Bạn không có quyền dừng tiến trình spam cho {sdt}. Chỉ người khởi tạo mới có thể dừng.")
        return

    try:
        os.kill(active_processes[sdt]['pid'], 9)  # Dừng process
        del active_processes[sdt]  # Xóa khỏi danh sách
        bot.reply_to(message, f"🛑 Đã dừng spam cho {sdt}.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi khi dừng spam: {e}")




# Danh sách blacklist (có thể lưu vào file/database)
BLACKLIST_FILE = "blacklist.json"

# Regex kiểm tra số điện thoại hợp lệ (10 số, bắt đầu bằng 0)
PHONE_REGEX = re.compile(r"^0\d{9}$")

def load_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_blacklist():
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(list(blacklist), f)

blacklist = load_blacklist()

# Lệnh /bansdt <số điện thoại>
@bot.message_handler(commands=['bansdt'])
def add_blacklist(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if message.from_user.id == ADMIN_ID:
        try:
            phone_number = message.text.split()[1]
            if PHONE_REGEX.match(phone_number):
                blacklist.add(phone_number)
                save_blacklist()
                bot.reply_to(message, f"Đã thêm {phone_number} vào blacklist.")
            else:
                bot.reply_to(message, "Số điện thoại không hợp lệ! (Yêu cầu 10 số, bắt đầu bằng 0).")
        except IndexError:
            bot.reply_to(message, "Vui lòng nhập số điện thoại!")
    else:
        bot.reply_to(message, "Ủa Alo Mày Phải Admin Đâu!")

# Lệnh /unbansdt <số điện thoại>
@bot.message_handler(commands=['unbansdt'])
def remove_blacklist(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if message.from_user.id == ADMIN_ID:
        try:
            phone_number = message.text.split()[1]
            if phone_number in blacklist:
                blacklist.remove(phone_number)
                save_blacklist()
                bot.reply_to(message, f"Đã xóa {phone_number} khỏi blacklist.")
            else:
                bot.reply_to(message, f"Số {phone_number} không có trong blacklist.")
        except IndexError:
            bot.reply_to(message, "Vui lòng nhập số điện thoại!")
    else:
        bot.reply_to(message, "Nói Roi Mà Mày Làm Gì Là Admin!")

# Xử lý tin nhắn chứa số điện thoại hợp lệ
@bot.message_handler(func=lambda message: message.text and PHONE_REGEX.match(message.text.strip()))
def check_blacklist(message):
    phone_number = message.text.strip()
    if phone_number in blacklist:
        bot.reply_to(message, "Số điện thoại này đã bị chặn!")


ADMIN_NAME = "quana12999"


@bot.message_handler(commands=['ad'])
def send_admin_info(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    bot.send_message(message.chat.id,
                     f"Only One => Is : {ADMIN_NAME}\nID: `{ADMIN_ID}`",
                     parse_mode='Markdown')

ADMIN_NAME = "quana12999"

@bot.message_handler(commands=['id'])
def get_user_id(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if len(message.text.split()) == 1:
        user_id = message.from_user.id
        bot.reply_to(message,
                     f"ID của bạn là: `{user_id}`",
                     parse_mode='Markdown')
    else:
        username = message.text.split('@')[-1].strip()
        try:
            user = bot.get_chat(
                username)  # Lấy thông tin người dùng từ username
            bot.reply_to(message,
                         f"ID của {user.first_name} là: `{user.id}`",
                         parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, "Không tìm thấy người dùng có username này.")


@bot.message_handler(commands=['info'])
def send_info(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if message.reply_to_message:
        users = [message.reply_to_message.from_user]
    else:
        args = message.text.split()[1:]
        users = [message.from_user]

        if args:
            users = []
            for arg in args:
                try:
                    user_id = int(arg) if arg.isdigit() else arg
                    user = bot.get_chat(user_id)
                    users.append(user)
                except Exception:
                    return

    for user in users:
        try:
            bio = bot.get_chat(user.id).bio if hasattr(bot.get_chat(user.id), 'bio') else "Không có hoặc không thể lấy được"
        except Exception:
            bio = "Không Có hoặc không thể lấy được"


        full_name = f"{user.first_name} {user.last_name or ''}".strip()
        link_name = f'<a href="tg://user?id={user.id}">{full_name}</a>'

        status = "Không xác định"
        if message.chat.type in ['group', 'supergroup']:
            try:
                member = bot.get_chat_member(message.chat.id, user.id)
                status = member.status
                if status == 'creator':
                    status = "Người Tạo Nhóm"
                elif status == 'administrator':
                    status = "Quản Trị Viên"
                elif status == 'member':
                    status = "Thành Viên"
                elif status == 'left':
                    status = "Đã Rời Nhóm"
                elif status == 'kicked':
                    status = "Bị Đuổi Khỏi Nhóm"
            except Exception:
                status = "Không thể xác định trạng thái"

        info_text = (
            f"<b>👤 Thông Tin Người Dùng:</b>\n"
            f"<b>┌ UID:</b> <code>{user.id}</code>\n"
            f"<b>├ Tên:</b> {link_name}\n"
            f"<b>├ Username:</b> @{user.username if user.username else 'Không có'}\n"
            f"<b>├ Ngôn Ngữ:</b> {getattr(user, 'language_code', 'Không xác định')}\n"
            f"<b>├ Trạng Thái:</b> {status}\n"
            f"<b>└ Bio:</b> {bio}\n"
        )

        photos = bot.get_user_profile_photos(user.id, limit=1)
        if photos.photos:
            photo_file_id = photos.photos[0][-1].file_id
            bot.send_photo(message.chat.id, photo_file_id, caption=info_text, parse_mode="HTML",  reply_to_message_id=message.message_id)
        else:
            bot.reply_to(message, info_text, parse_mode="HTML")


@bot.message_handler(commands=['ID'])
def handle_id_command(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    chat_id = message.chat.id
    bot.reply_to(message, f"ID của nhóm này là: {chat_id}")


####################
import time


def restart_program():
    """Khởi động lại script chính và môi trường chạy."""
    python = sys.executable
    script = sys.argv[0]
    # Khởi động lại script chính từ đầu
    try:
        subprocess.Popen([python, script])
    except Exception as e:
        print(f"Khởi động lại không thành công: {e}")
    finally:
        time.sleep(10)  # Đợi một chút để đảm bảo instance cũ đã ngừng hoàn toàn
        sys.exit()


import os
import sys

@bot.message_handler(commands=['rs'])
def restart_bot(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if message.from_user.id == ADMIN_ID:  # Chỉ admin mới được reset
        bot.reply_to(message, "Đang reset bot...")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        bot.reply_to(message, "Bạn không có quyền reset bot.")


@bot.message_handler(commands=['tv'])
def tieng_viet(message):
    chat_id = message.chat.id
    message_id = message.message_id
    auto_react_to_command(message)  # Tự động phản hồi cảm xúc với lệnh

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🇻🇳 Tiếng Việt (Beta)", url='https://t.me/setlanguage/abcxyz'),  # Nếu có mã Beta
        types.InlineKeyboardButton("🇻🇳 Tiếng Việt (Chính thức)", url='https://t.me/setlanguage/vietnamese'),
        types.InlineKeyboardButton("🇺🇸 English", url='https://t.me/setlanguage/en'),
        types.InlineKeyboardButton("🇪🇸 Español", url='https://t.me/setlanguage/es'),
        types.InlineKeyboardButton("🇫🇷 Français", url='https://t.me/setlanguage/fr'),
        types.InlineKeyboardButton("🇷🇺 Русский", url='https://t.me/setlanguage/ru'),
        types.InlineKeyboardButton("🇨🇳 中文", url='https://t.me/setlanguage/zh-hans-raw'),
        types.InlineKeyboardButton("🇰🇷 한국어", url='https://t.me/setlanguage/ko'),
        types.InlineKeyboardButton("🇯🇵 日本語", url='https://t.me/setlanguage/ja'),
    ]


    keyboard.add(*buttons)

    bot.send_message(
        chat_id,
        '🌐 Chọn một ngôn ngữ bạn muốn sử dụng cho Telegram:',
        reply_markup=keyboard,
        parse_mode='HTML'
    )

    # Xóa tin nhắn gốc của người dùng
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        bot.send_message(chat_id,
                         f"⚠️ Không thể xóa tin nhắn: <code>{e}</code>",
                         parse_mode='HTML')



@bot.message_handler(commands=['del', 'deluser'])
def delete_user(message):
    admin_id = message.from_user.id
    auto_react_to_command(message)  # <- Thêm dòng này
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'MÀY CÓ QUYỀN HẢ')
        return

    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG HOẶC UID')
        return

    user_id = int(command_parts[1])
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()

    if len(command_parts) == 2:
        # Xóa hoàn toàn người dùng khỏi danh sách
        if user_id in allowed_users:
            allowed_users.remove(user_id)
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id, ))
            bot.reply_to(
                message,
                f'NGƯỜI DÙNG CÓ ID {user_id} ĐÃ BỊ XÓA KHỎI DANH SÁCH.')
        else:
            bot.reply_to(message,
                         f'ID {user_id} KHÔNG TỒN TẠI TRONG DANH SÁCH.')
    elif len(command_parts) == 3:
        # Xóa thời gian VIP cụ thể
        try:
            time_to_remove = int(command_parts[2])
            cursor.execute(
                "SELECT expiration_time FROM users WHERE user_id = ?",
                (user_id, ))
            row = cursor.fetchone()
            if row:
                current_expiration = datetime.fromisoformat(row[0])
                new_expiration = current_expiration - timedelta(
                    days=time_to_remove)
                if new_expiration < datetime.now():
                    allowed_users.remove(user_id)
                    cursor.execute("DELETE FROM users WHERE user_id = ?",
                                   (user_id, ))
                    bot.reply_to(
                        message,
                        f'THỜI GIAN VIP CỦA ID {user_id} ĐÃ BỊ XÓA. NGƯỜI DÙNG ĐÃ BỊ LOẠI KHỎI DANH SÁCH.'
                    )
                else:
                    cursor.execute(
                        "UPDATE users SET expiration_time = ? WHERE user_id = ?",
                        (new_expiration.isoformat(), user_id))
                    bot.reply_to(
                        message,
                        f'THỜI GIAN VIP CỦA ID {user_id} ĐÃ BỊ GIẢM {time_to_remove} NGÀY.'
                    )
            else:
                bot.reply_to(message,
                             f'KHÔNG TÌM THẤY NGƯỜI DÙNG CÓ ID {user_id}.')
        except ValueError:
            bot.reply_to(
                message,
                'THỜI GIAN XÓA KHÔNG HỢP LỆ. VUI LÒNG NHẬP SỐ NGÀY HỢP LỆ.')

    connection.commit()
    connection.close()


@bot.message_handler(commands=['muaplan'])
def muaplan(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton("🔥 Buy Vip",
                                            url='https://t.me/quana12999')
    keyboard.add(url_button)

    bot.reply_to(
        message, "📑 <b>Mua Plan VIP</b>\n"
        "<blockquote>• 35.000 VND / 30 Ngày (Bank)\n• 40.000 VND / 30 Ngày (Card)\n• 150.000 VND / Vĩnh Viễn</blockquote>\n"
        "Liên hệ admin qua lệnh /admin để mua VIP!",
        parse_mode="HTML",
        reply_markup=keyboard)


@bot.message_handler(commands=['cachdung'])
def hdsd(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    bot.reply_to(message, f"""📑<b>HƯỚNG DẪN SỬ DỤNG</b>\n
<blockquote>┏━━━━━━━━━━━━━━━━━━━┓\n
┣➤ Để Sử Dụng Free Dùng Lệnh\n
┣➤ /sms 0123456789 5\n 
┣➤ /spam 0123456789 5\n
┣➤ 0123456789 là số muốn spam\n
┣➤ còn số 5 là số Lần spam\n
┗━━━━━━━━━━━━━━━━━━━➤\n
┏━━━━━━━━━━━━━━━━━━━┓\n
┣➤ Để Sử Dụng Vip Dùng Lệnh\n 
┣➤ /spamvip 0123456789 1000\n 
┣➤ 0123456789 là số muốn spam\n 
┣➤ còn số 1000 là số Lần spam\n 
┗━━━━━━━━━━━━━━━━━━━➤\n
┏━━━━━━━━━━━━━━━━━━━━┓\n
┣➤ Thông Tin Admin\n
┣➤ Telegram : @quana12999\n
┗━━━━━━━━━━━━━━━━━━━➤ </blockquote>\n""",
                     parse_mode="HTML")

    # Hàm lấy thông tin người chơi từ API






# Hàm gửi yêu cầu đến API kiểm tra trạng thái banned
def check_ban_status(uid):
    api_url = f"https://system.ffgarena.cloud/api/isbanned?id={uid}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json().get("details", {})
        nickname = data.get("PlayerNickname", "Không rõ")
        region = data.get("PlayerRegion", "Không rõ")
        is_banned = "🔴 Bị ban" if data.get("is_banned",
                                           "no") == "yes" else "🟢 Không bị ban"
        banned_period = data.get("banned_period", 0)

        return f"<blockquote>🆔 UID: {uid}\n👤 Tên: {nickname}\n🌍 Khu vực: {region}\n🚫 Trạng thái: {is_banned}\n⏳ Thời gian ban: {banned_period} ngày</blockquote>"

    return "⚠️ Lỗi khi kiểm tra UID. Vui lòng thử lại sau."


# Xử lý lệnh /checkban
@bot.message_handler(commands=['checkban'])
def handle_checkban(message):
    args = message.text.split()  # Tách nội dung lệnh
    auto_react_to_command(message)  # <- Thêm dòng này
    if len(args) < 2:
        bot.reply_to(
            message,
            "⚠️ Vui lòng nhập UID sau lệnh /checkban.\nVí dụ: /checkban 156256275",
            parse_mode="Markdown")
        return

    temp_message = f"👨‍💻"

    # Gửi thông báo tạm thời
    sent_message = bot.reply_to(message, temp_message)

    # Chờ 3 giây
    time.sleep(3)

    # Xóa thông báo tạm thời
    bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)

    uid = args[1]  # Lấy UID từ tin nhắn
    bot_reply = check_ban_status(uid)  # Kiểm tra trạng thái banned
    bot.reply_to(message, bot_reply, parse_mode="HTML")  # Gửi kết quả

@bot.message_handler(commands=['thuebot'])
def bank_info(message):
    # Lấy ID người gõ lệnh
    user_id = message.from_user.id
    
    # Nội dung văn bản cần gửi cùng với ảnh
    thue_bot_text = f'''
<blockquote>
📌 Thông Tin Thanh Toán 🏦
├ Ngân Hàng : VietTinBank
├ STK : 0327893606
├ Chủ TK : Minh Quân
├ Nội Dung : <code>thuebot_{user_id}</code>
├ Số Tiền : [nhập số tiền]
├ Gửi bill cho AD để được duyệt
├ *LƯU Ý* : PHẢI CÓ NỘI DUNG CHUYỂN KHOẢN
└ 💬 Liên Hệ : @quana12999
</blockquote>
'''

    # Gửi ảnh kèm caption
    bot.send_photo(
        chat_id=message.chat.id,
        photo='https://i.imgur.com/jkGOXna.jpeg',
        caption=thue_bot_text,
        parse_mode='HTML'
    )
    

@bot.message_handler(commands=['giabot'])
def giabot_info(message):
    # Lấy ID người gõ lệnh
    user_id = message.from_user.id

    gia_bot_text = '''
<blockquote><b>Giá Bot Free Fire Hiện Tại</b>
├ 1 Ngày 5 Nghìn VND 
├ 1 Tuần 20 Nghìn VND
├ 1 Tháng 120 Nghìn VND
├ 1 Năm 800 Nghìn VND
└ /thuebot : Thuê bot
</blockquote>
'''

    # Tạo bàn phím Inline
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔥 Thuê Bot", callback_data="thuebot")
    )

    # Gửi ảnh kèm caption và nút
    bot.send_photo(
        chat_id=message.chat.id,
        photo='https://i.imgur.com/y2O0gy4.jpeg',
        caption=gia_bot_text,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['muavip'])
def muavip_info(message):
    # Lấy ID người gõ lệnh
    user_id = message.from_user.id
    
    # Nội dung văn bản cần gửi cùng với ảnh
    mua_vip_text = f'''
<blockquote>
<b>📌 Thông Tin Thanh Toán 🏦
├ Ngân Hàng : VietTinBank
├ STK : 0327893606
├ Chủ TK : Minh Quân
├ Nội Dung : <code>thuebot_{user_id}</code>
├ Số Tiền : [nhập số tiền]
├ Gửi bill cho AD để được duyệt
├ *LƯU Ý* : PHẢI CÓ NỘI DUNG CHUYỂN KHOẢN
└ 💬 Liên Hệ : @quana12999
</blockquote>
'''

    # Gửi ảnh kèm caption
    bot.send_photo(
        chat_id=message.chat.id,
        photo='https://i.imgur.com/jkGOXna.jpeg',
        caption=mua_vip_text,
        parse_mode='HTML'
    )
    
    
    
# Hàm gọi API reghotmail.php
import requests


# Hàm gọi API Hotmail
def create_hotmail():
    url = "https://keyherlyswar.x10.mx/Apidocs/reghotmail.php"
    try:
        response = requests.get(url, timeout=15)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Hàm lấy email & password từ JSON API (tự động dò key)
def extract_credentials(data):
    email_keys = ["email", "Email", "mail"]
    pass_keys = ["pass", "password", "Password"]

    # Nếu API trả data nested
    if isinstance(data, dict):
        # thử dò trong các key
        for key in email_keys:
            if key in data:
                email = data[key]
                break
        else:
            # dò trong data nested
            email = None
            for v in data.values():
                if isinstance(v, dict):
                    for key in email_keys:
                        if key in v:
                            email = v[key]
                            break
        for key in pass_keys:
            if key in data:
                password = data[key]
                break
        else:
            password = None
            for v in data.values():
                if isinstance(v, dict):
                    for key in pass_keys:
                        if key in v:
                            password = v[key]
                            break
    else:
        email = None
        password = None

    return email or "Không lấy được", password or "Không lấy được"

# Lệnh /reg
@bot.message_handler(commands=['reg'])
def hotmail(message):
    user_id = message.from_user.id  # Lấy user_id để check key

    # Kiểm tra key nếu đang yêu cầu
    if REQUIRE_KEY:
        ok, info = check_user_key(user_id)
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    msg = bot.send_message(message.chat.id, "⏳ Vui lòng chờ, bot đang tạo tài khoản Hotmail...")
    data = create_hotmail()

    if "error" in data:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                              text=f"❌ Lỗi: {data['error']}")
        return

    email, password = extract_credentials(data)

    result_text = (
        "✅ Tài khoản Hotmail đã tạo thành công!\n\n"
        f"📧 Email: `{email}`\n"
        f"🔑 Mật khẩu: `{password}`\n\n"
        "Admin @quana12999"
    )

    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                          text=result_text, parse_mode="Markdown")



        
import yt_dlp
# Lệnh /ytinfo <link>
@bot.message_handler(commands=['ytb'])
def get_yt_info(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    try:
        # Lấy link từ tin nhắn
        text_split = message.text.split()
        if len(text_split) < 2:
            bot.reply_to(message, "⚠️ Vui lòng nhập link YouTube! Ví dụ:\n/ytb https://youtu.be/dQw4w9WgXcQ")
            return

        url = text_split[1]

        # Sử dụng yt_dlp để lấy thông tin video
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # Lấy các thông tin cần thiết
        title = info.get("title", "Không rõ")
        uploader = info.get("uploader", "Không rõ")
        duration = info.get("duration", 0)
        view_count = info.get("view_count", 0)
        like_count = info.get("like_count", "Không rõ")
        upload_date = info.get("upload_date", "Không rõ")
        thumbnail = info.get("thumbnail", "")

        # Chuyển định dạng ngày từ YYYYMMDD sang DD/MM/YYYY
        if upload_date and len(upload_date) == 8:
            upload_date = f"{upload_date[6:]}/{upload_date[4:6]}/{upload_date[:4]}"

        # Gửi thông tin video
        caption = f"""
🎬 <b>Tiêu đề:</b> {title}
📺 <b>Kênh:</b> {uploader}
⏳ <b>Thời lượng:</b> {duration} giây
👀 <b>Lượt xem:</b> {view_count}
👍 <b>Lượt thích:</b> {like_count}
📅 <b>Ngày đăng:</b> {upload_date}
🔗 <a href="{url}">Xem video</a>
"""
        if thumbnail:
            bot.send_photo(message.chat.id, thumbnail, caption=caption, parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, caption, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"Lỗi khi lấy thông tin video !!!")


def anv(city):
    API_KEY = '1dcdf9b01ee855ab4b7760d43a10f854'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    tna = requests.get(base_url)
    nan = tna.json()

    if nan['cod'] == 200:
        weather_info = nan['weather'][0]['description']
        icon = nan['weather'][0]['main']
        temp_info = nan['main']['temp']
        feels_like = nan['main']['feels_like']
        temp_min = nan['main']['temp_min']
        temp_max = nan['main']['temp_max']
        city = nan['name']
        lat = nan['coord']['lat']
        lon = nan['coord']['lon']
        country = nan['sys']['country']
        all = nan['clouds']['all']
        humidity_info = nan['main']['humidity']
        wind_speed_info = nan['wind']['speed']
        feels_like_info = nan['main']['feels_like']
        gg = f"(https://www.google.com/maps/place/{nan['coord']['lat']},{nan['coord']['lon']})"
        return f'╭─────⭓Thời Tiết\n│🌍 City: {city}\n│🔗 Link map: [{city}]{gg}\n│☁️ Thời tiết: {weather_info}\n│🌡 Nhiệt độ: {temp_info}°C\n│🌡️ Nhiệt độ cảm nhận: {feels_like}°C\n│🌡️ Nhiệt độ tối đa: {temp_max}°C\n│🌡️ Nhiệt độ tối thiểu: {temp_min}°C\n│📡 Tình trạng thời tiết: {icon}\n│🫧 Độ ẩm: {humidity_info}%\n│☁️ Mức độ mây: {all}%\n│🌬️ Tốc độ gió: {wind_speed_info} m/s\n│🌐 Quốc gia: {country}.\n╰─────────────⭓'
    else:
        return 'Lệnh: thoitiet <tên thành phố>'

@bot.message_handler(commands=['thoitiet'])
def weather(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    if len(message.text.split()) == 0:
        bot.reply_to(message, 'Nhập đúng định dạng:\n/thoitiet Hà Nội')
        return
    city = message.text.split()[1:]
    city = ' '.join(city)
    annn = anv(city)
    bot.reply_to(message, f'{annn}', parse_mode='Markdown')


is_bot_active = True

import urllib3

# Tắt cảnh báo SSL không xác thực
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@bot.message_handler(commands=['visitff'])
def visit_ff(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Vui lòng nhập đúng cú pháp: /visitff <uid>")
            return

        uid = args[1]
        total_views = 0
        total_tokens = 0
        total_time = 0.0
        max_views = 100000
        loop_count = 0

        # Gửi thông báo tạm thời
        temp_message = bot.reply_to(message, "Đang thực hiện gửi view, vui lòng đợi...")

        while total_views < max_views:
            url = f"https://scromnyi-visit.vercel.app/send_visit?uid={uid}"
            res = requests.get(url).json()
            loop_count += 1

            if not res.get("player_details", {}).get("success") or not res.get("visit_results", {}).get("success"):
                break

            visit = res["visit_results"]
            total_views += visit["total_views_sent"]
            total_tokens += visit["tokens_used"]
            total_time += visit["total_time_takes"]

            time.sleep(1)  # delay nhẹ giữa các lần gửi để tránh bị khóa IP

            # Dừng nếu API trả về số view bằng 0 (có thể đã cạn token hoặc UID không thể buff thêm)
            if visit["total_views_sent"] == 0:
                break

        bot.delete_message(chat_id=message.chat.id, message_id=temp_message.message_id)

        player = res["player_details"]

        msg = (
            f"[VISIT FREE FIRE - Tổng hợp sau {loop_count} lần]\n"
            f"Tên: {player['name']}\n"
            f"UID: {player['id']}\n"
            f"Cấp: {player['level']}\n"
            f"Server: {player['server']}\n\n"
            f"Tổng lượt view gửi: {total_views}\n"
            f"Tổng token đã dùng: {total_tokens}\n"
            f"Tổng thời gian xử lý: {round(total_time, 2)} giây"
        )

        bot.reply_to(message, msg)

    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}")


import requests
from telebot import types

# ==================== Cấu hình ====================
API_URL_TEMPLATE = "https://api-likes-alliff-v3.vercel.app/like?uid={uid}&server_name={server_name}"

# ==================== Hàm kiểm tra bảo trì ====================
def is_under_maintenance(cmd_name: str) -> bool:
    return False

# ==================== Hàm buff like 1 UID ====================
def buff_like(uid, server_name):
    try:
        url = API_URL_TEMPLATE.format(uid=uid, server_name=server_name)
        r = requests.get(url, timeout=15)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# ==================== Bot command /like ====================
@bot.message_handler(commands=['like'])
def handle_ff(message):
    user_id = message.from_user.id  # Lấy user_id của người dùng

    # Kiểm tra key nếu bật REQUIRE_KEY
    if REQUIRE_KEY:
        ok, info = check_user_key(user_id)
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    if is_under_maintenance("like"):
        bot.reply_to(message, "❌ Lệnh hiện đang được bảo trì, vui lòng thử lại sau.")
        return

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔥 Buy Vip", url='https://t.me/quana12999'))

    args = message.text.split()[1:]

    # Nếu người dùng chỉ nhập 1 tham số, coi là UID, region mặc định vn
    if len(args) == 1:
        region = "vn"
        uid = args[0]
    elif len(args) == 2:
        region, uid = args
    else:
        bot.reply_to(message, "❗ Cú pháp: /like <region> <uid>\nHoặc /like <uid>")
        return

    temp = bot.reply_to(message, "👨‍💻 Đang gửi like...")

    data = buff_like(uid, region)

    if not data or data.get("error"):
        bot.reply_to(message, f"UID {uid} Đã max like", reply_markup=keyboard)
    else:
        sent = data.get("likes_added", 0)
        if sent == 0:
            bot.reply_to(
                message,
                f"⚠️ UID {uid} đã nhận đủ like.\n📈 Like hiện tại: {data.get('likes_after', 0)}",
                reply_markup=keyboard
            )
        else:
            msg = (f"BUFF LIKE THÀNH CÔNG ✅\n"
                   f"<blockquote>╭👤 Name: {data.get('name', 'Không xác định')}\n"
                   f"├🆔 UID : {uid}\n"
                   f"├🌏 Region : {region}\n"
                   f"├📉 Like trước: {data.get('likes_before', 0)}\n"
                   f"├📈 Like sau: {data.get('likes_after', 0)}\n"
                   f"╰👍 Đã gửi: {sent}</blockquote>\n")
            bot.reply_to(message, msg, parse_mode="HTML", reply_markup=keyboard)

    bot.delete_message(message.chat.id, temp.message_id)  
    
import requests
import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

API_URL = "https://info-tiktok-user.vercel.app/tiktok?input="
@bot.message_handler(commands=['tt'])
def tiktok_info(message):
    try:
        user_id = message.from_user.id

        # Kiểm tra key nếu yêu cầu
        if REQUIRE_KEY:
            ok, info = check_user_key(user_id)
            if not ok:
                bot.reply_to(
                    message,
                    "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                    "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                    parse_mode="Markdown"
                )
                return
        else:
            info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

        # Lấy username/link TikTok
        username = message.text.replace("/tt", "").strip()
        if not username:
            bot.reply_to(message, "⚠️ Vui lòng nhập username hoặc link TikTok sau lệnh /tt.")
            return

        username_encoded = urllib.parse.quote(username)
        res = requests.get(API_URL + username_encoded, timeout=10).json()

        if not res.get("success"):
            bot.reply_to(message, "❌ Không tìm thấy thông tin TikTok.")
            return

        user = res["data"]["userInfo"]["user"]
        stats = res["data"]["userInfo"]["statsV2"]

        caption = (
            f"📱 **Thông tin TikTok**\n"
            f"🆔 **ID:** {user.get('id', 'N/A')}\n"
            f"👤 **Nickname:** {user.get('nickname', 'N/A')}\n"
            f"🔗 **Username:** @{user.get('uniqueId', 'N/A')}\n"
            f"📄 **Bio:** {user.get('signature', 'Không có')}\n"
            f"✅ **Verified:** {'Có' if user.get('verified') else 'Không'}\n"
            f"🗣 **Language:** {user.get('language', 'N/A')}\n"
            f"📅 **Ngày tạo:** {user.get('createTime', 'N/A')}\n"
            f"👥 **Follower:** {stats.get('followerCount', '0')}\n"
            f"👤 **Following:** {stats.get('followingCount', '0')}\n"
            f"❤️ **Lượt thích:** {stats.get('heartCount', '0')}\n"
            f"🎥 **Số video:** {stats.get('videoCount', '0')}\n"
            f"👍 **Đã thích:** {stats.get('diggCount', '0')}\n"
            f"🤝 **Bạn bè:** {stats.get('friendCount', '0')}\n\n"
            f"🔑 **Key của bạn:** {info['key']}\n"
            f"⏰ **Hạn sử dụng:** {info['expiration_date']}"
        )

        bot.send_photo(
            chat_id=message.chat.id,
            photo=user.get("avatarLarger", ""),
            caption=caption,
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi: {e}")
 
 
        
@bot.message_handler(commands=['tiktok'])
def get_video(message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        video_url = args[1]
        api_url = f'http://tienich.x10.mx/tiktok.php?url={video_url}'
        
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json().get("data", {})
            
            title = data.get("title", "Không có tiêu đề")
            author = data.get("author", {}).get("nickname", "Không rõ tác giả")
            region = data.get("region", "Không rõ khu vực")
            duration = data.get("duration", 0)
            create_time = data.get("create_time", "Không rõ thời gian")
            play_count = data.get("play_count", "0")
            digg_count = data.get("digg_count", "0")
            comment_count = data.get("comment_count", "0")
            share_count = data.get("share_count", "0")
            download_count = data.get("download_count", "0")
            collect_count = data.get("collect_count", "0")
            music_url = data.get("music_info", {}).get("play", None)
            
            image_urls = data.get("images", [])
            video_url = data.get("play")
            
            message_text = f"""
🎥 {title if video_url else 'None'}

<blockquote>👤 Tác giả: {author}
🌍 Khu Vực: {region}
🎮 Độ Dài Video: {duration} Giây
🗓️ Ngày Đăng: {create_time}
---------------------------------------
▶️ Views: {play_count}
❤️ Likes: {digg_count} like
💬 Comments: {comment_count}
🔄 Shares: {share_count}
⬇️ Downloads: {download_count}
📥 Favorites: {collect_count}</blockquote>
"""
            
            if video_url:
                if image_urls:
                    media_group = [types.InputMediaPhoto(media=url) for url in image_urls if url]
                    if media_group:
                        bot.send_media_group(message.chat.id, media=media_group)
                
                bot.send_video(message.chat.id, video=video_url, caption=message_text, parse_mode='HTML')
            else:
                if image_urls:
                    media_group = [types.InputMediaPhoto(media=url) for url in image_urls if url]
                    if media_group:
                        bot.send_media_group(message.chat.id, media=media_group)
                
                bot.send_message(message.chat.id, message_text, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "Không thể lấy thông tin video.")
    else:
        bot.send_message(message.chat.id, "Vui lòng cung cấp URL video TikTok.")
        
        
# Lệnh /downfb <url>
from urllib.parse import urlparse
from pathlib import Path
@bot.message_handler(commands=['downfb'])
def download_facebook_video(message):
    try:
        parts = message.text.split(" ", 1)
        if len(parts) != 2:
            bot.reply_to(message, "❗ Vui lòng nhập đúng định dạng:\n/downfb <facebook_url>")
            return

        fb_url = parts[1]
        api_url = f"https://api.sumiproject.net/facebook/video?url={fb_url}"
        res = requests.get(api_url)
        data = res.json()

        video_url = data.get("hd") or data.get("sd")
        if not video_url:
            bot.reply_to(message, "❌ Không tìm thấy video.")
            return

        # Tải video về file tạm
        filename = "fb_video.mp4"
        with requests.get(video_url, stream=True) as r:
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        caption = f"🎬 Video Facebook Của Bạn\n📎 Link: {fb_url}"
        with open(filename, "rb") as video:
            bot.send_video(message.chat.id, video, caption=caption, reply_to_message_id=message.message_id)

        os.remove(filename)  # Xóa file sau khi gửi xong

    except Exception as e:
        print("Error:", e)
        bot.reply_to(message, "⚠️ Có lỗi xảy ra khi xử lý video.")

ANHGAI_URL = "https://api.zeidteam.xyz/images/gai"
@bot.message_handler(commands=['anhgai'])
def send_image(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    try:
        response = requests.get(ANHGAI_URL, verify=False)
        if response.status_code == 200:
            data = response.json()
            image_url = data.get("url")
            if image_url:
                bot.send_photo(message.chat.id,
                               image_url,
                               caption=f"Hàng Này Ok Chứ ?", reply_to_message_id=message.message_id)
            else:
                bot.reply_to(message, "Không tìm thấy ảnh.")
        else:
            bot.reply_to(message, "Lỗi khi truy cập API.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi: {e}")

import urllib.parse
url = "https://ngl.link/api/submit"
active_spamsngl = {}  # Lưu trạng thái spam theo user_id


def generate_device_id():
    return (''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=13)) +
            ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=13)))


def send_questions(chat_id, username, question, sl):
    user_id = chat_id
    active_spams[user_id] = True  # Bắt đầu spam

    try:
        for i in range(sl):
            if not active_spams.get(user_id):  # Kiểm tra lệnh dừng
                bot.send_message(chat_id, "🛑 Đã dừng spam.")
                break

            device_id = generate_device_id()

            headers = {
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://ngl.link',
                'referer': f'https://ngl.link/{username}',
                'x-requested-with': 'XMLHttpRequest'
            }

            data = {
                'username': username,
                'question': question,
                'deviceId': device_id,
                'gameSlug': '',
                'referrer': ''
            }

            requests.post(url, headers=headers, data=urllib.parse.urlencode(data))
            time.sleep(0.5)  # Giảm spam tốc độ cao nếu bị chặn

    except Exception as e:
        bot.send_message(chat_id, f"❌ Lỗi khi gửi câu hỏi: {e}")

    finally:
        active_spams.pop(user_id, None)  # Dọn dẹp sau khi kết thúc


@bot.message_handler(commands=['nglink', 'ngl'])
def handle_nglink(message):
    user_id = message.from_user.id
    try:
        args = message.text.split(maxsplit=3)
        if len(args) < 4:
            bot.reply_to(message, "<b>⚠️ Vui Lòng Nhập Đúng Cú Pháp</b> \n\n"
                                  "Ví dụ: \n<code>/nglink username số_lượng câu_hỏi</code>\nVD:/nglink concacc 1000 con cặc", parse_mode="HTML")
            return

        username = args[1]
        try:
            sl = int(args[2])
            if sl <= 0:
                raise ValueError
        except ValueError:
            bot.reply_to(message, "⚠️ Số Lượng Phải Là Số Nguyên Dương!")
            return

        question = args[3]
        waiting_message = bot.reply_to(message, "🐳 Đang gửi...")

        spam_ngl = f"""
╔══════════════════════
║ 🚀 SPAM NGLINK
║ •  Người Dùng : <code>{username}</code>
║ •  Nội Dung : <code>{question}</code>
║ •  Số Lượng : <code>{sl}</code>
╚══════════════════════
Muốn stop dùng /stopngl
"""
        bot.delete_message(message.chat.id, waiting_message.message_id)
        bot.reply_to(message, spam_ngl, parse_mode="HTML")

        # Gọi send_questions bằng Thread để không block bot
        thread = threading.Thread(target=send_questions, args=(user_id, username, question, sl))
        thread.start()

    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi: {e}")


@bot.message_handler(commands=['stopngl'])
def stop_spam(message):
    user_id = message.from_user.id
    if active_spams.get(user_id):
        active_spamsngl[user_id] = False
        bot.reply_to(message, "🛑 Đang dừng spam... vui lòng đợi 1 chút.")
    else:
        bot.reply_to(message, "⚠️ Bạn không có spam nào đang chạy.")


import asyncio
import edge_tts
import os


@bot.message_handler(commands=['voice'])
def text_to_speech(message):
    args = message.text.split(maxsplit=1)
    auto_react_to_command(message)  # <- Thêm dòng này

    if len(args) < 2:
        bot.reply_to(message, "Sai cú pháp! Dùng:\n/voice văn bản", parse_mode="Markdown")
        return

    text = args[1]
    file_path = "output.mp3"
    voice = "vi-VN-NamMinhNeural"  # Giọng nam tiếng Việt

    async def generate_voice():
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(file_path)

            with open(file_path, "rb") as audio:
                bot.send_voice(message.chat.id, audio, reply_to_message_id=message.message_id)

            os.remove(file_path)
        except Exception as e:
            bot.reply_to(message, f"Đã xảy ra lỗi: {str(e)}")

    asyncio.run(generate_voice())


from urllib.parse import urlparse
import zipfile


def sanitize_filename(name):
    return re.sub(r'\W+', '_', name)[:50]

@bot.message_handler(commands=['code'])
def handle_code(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    try:
        args = message.text.split(maxsplit=1)
        if len(args) != 2:
            bot.reply_to(message, "Vui lòng nhập đúng lệnh: /code <url>\nVD: /code https://vlxx.com.mssg.me/")
            return

        url = args[1].strip()
        if not url.startswith("http"):
            url = "http://" + url

        parsed_url = urlparse(url)
        domain = sanitize_filename(parsed_url.netloc)
        zip_filename = f"{domain}_source.zip"

        # Lấy mã HTML
        response = requests.get(url, timeout=15)
        response.encoding = response.apparent_encoding
        html = response.text

        # Phân tích HEAD và BODY
        soup = BeautifulSoup(html, "html.parser")
        head = soup.head.prettify() if soup.head else "Không có thẻ <head>"
        body = soup.body.prettify() if soup.body else "Không có thẻ <body>"

        # Tạo file tạm
        with open("full.html", "w", encoding="utf-8") as f:
            f.write(html)
        with open("head.html", "w", encoding="utf-8") as f:
            f.write(head)
        with open("body.html", "w", encoding="utf-8") as f:
            f.write(body)

        # Nén file ZIP
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write("full.html")
            zipf.write("head.html")
            zipf.write("body.html")

        # Gửi file ZIP
        with open(zip_filename, "rb") as f:
            bot.send_document(message.chat.id, f, caption=f"Toàn bộ mã nguồn từ {url} của bạn yêu cầu.", reply_to_message_id=message.message_id)

        # Xóa file tạm
        for file in ["full.html", "head.html", "body.html", zip_filename]:
            if os.path.exists(file):
                os.remove(file)

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"❌ Không thể truy cập URL: {e}")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Đã xảy ra lỗi: {e}")

from deep_translator import GoogleTranslator
@bot.message_handler(commands=['dich'])
def translate_command(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "Vui lòng nhập từ hoặc câu cần dịch.\nVí dụ: /dich concac lap trinh nhu cac")
        return

    text_to_translate = args[1]
    try:
        translated = GoogleTranslator(source="auto", target="vi").translate(text_to_translate)
        bot.reply_to(message, f"Dịch: {translated}")
    except Exception as e:
        bot.reply_to(message, f"Lỗi dịch: {str(e)}")


TIKTOK_FILE = "tiktok_links.txt"  # File chứa danh sách link TikTok
# Hàm lấy link TikTok ngẫu nhiên
def get_random_tiktok_link():
    try:
        with open(TIKTOK_FILE, "r") as file:
            links = [line.strip() for line in file if line.strip()]
        return random.choice(links) if links else None  # Chọn ngẫu nhiên
    except FileNotFoundError:
        return None


# Hàm tải video TikTok không logo từ API
def get_tiktok_no_watermark(url):
    API_URL = "https://www.tikwm.com/api/"
    params = {"url": url}

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("play")  # Link tải video không logo
    return None


# Lệnh /random để gửi video ngẫu nhiên
@bot.message_handler(commands=['videogai'])
def send_random_video(message):
    auto_react_to_command(message)  # Phản ứng tự động nếu có
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    # --- Kiểm tra key ---
    if REQUIRE_KEY:
        try:
            ok, info = check_user_key(user_id)
        except Exception:
            ok, info = False, {}
        if not ok:
            bot.reply_to(
                message,
                "❌ Bạn chưa nhập key hoặc key đã hết hạn!\n"
                "👉 Lấy key bằng lệnh `/getkey` và nhập `/key <mã_key>`.",
                parse_mode="Markdown"
            )
            return
    else:
        info = {"key": "Không yêu cầu", "expiration_date": "Vô hạn"}

    # --- Lấy link TikTok ---
    tiktok_url = get_random_tiktok_link()
    if not tiktok_url:
        bot.send_message(message.chat.id, "⚠️ Không có link TikTok nào trong danh sách!")
        return

    # --- Tải video không logo ---
    video_url = get_tiktok_no_watermark(tiktok_url)
    if video_url:
        bot.send_video(
            message.chat.id,
            video_url,
            caption=f"🎬 Đã Chưa Nè!!!\nYêu Cầu Của @{username}",
            reply_to_message_id=message.message_id
        )
    else:
        bot.reply_to(message, "❌ Lỗi khi tải video, vui lòng thử lại sau!")
        

import time
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import my_pb2
import output_pb2
import schedule
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

team_lock = threading.Lock()
teambot = {
    "/5s": 5,
    "/6s": 6
}


@bot.message_handler(commands=["5s", "6s"])
def invite_to_team(message):
    user_id = message.from_user.id
    if not team_lock.acquire(blocking=False):
        bot.reply_to(message, "Bot Đang Xử Lý Lệnh Trước Đó, Vui Lòng Chờ Trong Giây Lát!")
        return
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, f"Lệnh Như Này Nè:\n{parts[0].split('@')[0]} [UID]")
            return
        uid = parts[1]
        if not uid.isdigit():
            bot.reply_to(message, "UID Là Số Nha!")
            return
        command = parts[0].split('@')[0]
        soteam = teambot.get(command)
        if soteam is None:
            bot.reply_to(message, "Lệnh Team Không Hợp Lệ!")
            return
        moi = bot.reply_to(message, f"Đang Gửi Lời Mời. Vui Lòng Chấp Nhận Lời Mời Nhanh!!")
        result = subprocess.run(
            ["python3", "team.py", str(uid), str(soteam)],
            capture_output=True
        )
        bot.delete_message(chat_id=message.chat.id, message_id=moi.message_id)
        if result.returncode == 0:
            bot.reply_to(message, f"""<blockquote>Đã Mời Thành Công</blockquote>
<b>UID</b>: <code>{uid}</code>
<b>TEAM</b>: <code>{soteam}</code>""", parse_mode="HTML")
        else:
            bot.reply_to(message, f"<blockquote>Thất Bại Khi Mời, Vui Lòng Thử Lại!</blockquote>", parse_mode="HTML")
    except Exception as e:
        print(f"Lỗi Nữa Nè: {str(e)}")
    finally:
        team_lock.release()


TAOANH_URL = "https://seaart-ai.apis-bj-devs.workers.dev/?Prompt={text}"
@bot.message_handler(commands=['taoanh'])
def tao_anh(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    username = message.from_user.username
    try:
        text = message.text.replace("/taoanh", "").strip()
        if not text:
            bot.reply_to(message, "Vui lòng nhập mô tả ảnh.\n Ví dụ: /taoanh cdanhdev")
            return

        # Gửi tin nhắn thông báo
        status_msg = bot.reply_to(message, "Đang tạo ảnh, vui lòng đợi...")

        response = requests.get(TAOANH_URL.format(text=text)).json()
        if response["status"] == "success":
            images = response["result"]
            for img in images:
                bot.send_photo(message.chat.id, img["url"], caption=f"📸🏞ẢNH BẠN YÊU CẦU @{username}", reply_to_message_id=message.message_id)

        else:
            bot.reply_to(message, "Không thể tạo ảnh, vui lòng thử lại sau!")

        # Xóa tin nhắn "Đang tạo ảnh..."
        time.sleep(2)  # Chờ 2 giây để đảm bảo ảnh đã gửi xong
        bot.delete_message(message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.reply_to(message, f"Lỗi: {str(e)}")

import requests
from telebot.types import InputFile

@bot.message_handler(commands=['qr'])
def generate_qrcode(message):
    auto_react_to_command(message)
    try:
        text = message.text.split(' ', 1)
        if len(text) < 2:
            bot.reply_to(message, "Vui lòng nhập nội dung sau lệnh /qr\nVí dụ: /qr hello")
            return

        user_input = text[1]
        url = f"https://dynamic-qr-code.bjcoderx.workers.dev/?message={user_input}"
        res = requests.get(url)
        if res.status_code != 200:
            bot.reply_to(message, "Lỗi khi tạo mã QR.")
            return

        qr_data = res.json()
        qr_image_url = qr_data.get("qrImageUrl")
        if not qr_image_url:
            bot.reply_to(message, "Không tìm thấy ảnh QR.")
            return

        # Tải ảnh QR về máy chủ
        image_response = requests.get(qr_image_url)
        if image_response.status_code != 200:
            bot.reply_to(message, "Không tải được ảnh QR.")
            return

        with open("qr_temp.png", "wb") as f:
            f.write(image_response.content)

        # Gửi ảnh từ tệp
        with open("qr_temp.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Đây là mã QR của bạn", reply_to_message_id=message.message_id)

    except Exception as e:
        bot.reply_to(message, f"Lỗi")


soundcloud_data = {}
PLATFORM = "soundcloud"
API_BASE = "https://api-v2.soundcloud.com"
CONFIG_PATH = "config.json"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]
ACCEPT_LANGUAGES = ["en-US,en;q=0.9", "fr-FR,fr;q=0.9", "es-ES,es;q=0.9", "de-DE,de;q=0.9", "zh-CN,zh;q=0.9"]

def get_random_element(array):
    return random.choice(array)

def get_headers():
    return {
        "User-Agent": get_random_element(USER_AGENTS),
        "Accept-Language": get_random_element(ACCEPT_LANGUAGES),
        "Referer": "https://soundcloud.com/",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

def get_client_id():
    try:
        import os
        config = {}
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            if config.get('client_id'):
                return config['client_id']

        response = requests.get("https://soundcloud.com/", headers=get_headers())
        response.raise_for_status()
        script_tags = re.findall(r'<script crossorigin src="([^"]+)"', response.text)
        script_urls = [url for url in script_tags if url.startswith("https")]

        if not script_urls:
            raise ValueError("No script URLs found")

        script_response = requests.get(script_urls[-1], headers=get_headers())
        script_response.raise_for_status()
        client_id_match = re.search(r',client_id:"([^"]+)"', script_response.text)
        if not client_id_match:
            raise ValueError("Client ID not found in script")

        client_id = client_id_match.group(1)

        config['client_id'] = client_id
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)

        return client_id
    except Exception as e:
        print(f"Error fetching client ID: {e}")
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            return config.get('client_id', 'BdMz2qskbsp2ee6BlEIBKrV1uuYwc8r1')
        return 'BdMz2qskbsp2ee6BlEIBKrV1uuYwc8r1'

def get_music_info(question, limit=10):
    try:
        client_id = get_client_id()
        response = requests.get(
            f"{API_BASE}/search/tracks",
            params={
                "q": question,
                "variant_ids": "",
                "facet": "genre",
                "client_id": client_id,
                "limit": limit,
                "offset": 0,
                "linked_partitioning": 1,
                "app_locale": "en",
            },
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching music info: {e}")
        return None

def get_music_stream_url(track):
    try:
        client_id = get_client_id()
        api_url = f"{API_BASE}/resolve?url={track['permalink_url']}&client_id={client_id}"
        response = requests.get(api_url, headers=get_headers())
        response.raise_for_status()
        data = response.json()

        progressive_url = next(
            (t['url'] for t in data.get('media', {}).get('transcodings', []) if t['format']['protocol'] == 'progressive'),
            None
        )
        if not progressive_url:
            raise ValueError("No progressive transcoding URL found")

        stream_response = requests.get(
            f"{progressive_url}?client_id={client_id}&track_authorization={data.get('track_authorization', '')}",
            headers=get_headers()
        )
        stream_response.raise_for_status()
        return stream_response.json()['url']
    except Exception as e:
        print(f"Error getting music stream URL: {e}")
        return None

@bot.message_handler(commands=['scl'])
def soundcloud(message):
    auto_react_to_command(message)  # <- Thêm dòng này
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "🚫 Vui lòng nhập tên bài hát muốn tìm kiếm.\nVí dụ: /scl Tên bài hát", parse_mode='HTML')
        return
    keyword = args[1].strip()
    music_info = get_music_info(keyword)
    if not music_info or not music_info.get('collection') or len(music_info['collection']) == 0:
        bot.reply_to(message, "🚫 Không tìm thấy bài hát nào khớp với từ khóa.", parse_mode='HTML')
        return
    tracks = [track for track in music_info['collection'] if track.get('artwork_url')]
    if not tracks:
        bot.reply_to(message, "🚫 Không tìm thấy bài hát nào có hình ảnh.", parse_mode='HTML')
        return
    response_text = "<b>🎵 Kết quả tìm kiếm trên SoundCloud</b>\n\n"
    for i, track in enumerate(tracks):
        response_text += f"<b>{i + 1}. {track['title']}</b>\n"
        response_text += f"👤 Nghệ sĩ: {track['user']['username']}\n"
        response_text += f"📊 Lượt nghe: {track['playback_count']:,} | Thích: {track['likes_count']:,}\n"
        response_text += f"🆔 ID: {track['id']}\n\n"
    response_text += "<b>💡 Trả lời tin nhắn này bằng số từ 1-10 để chọn bài hát!</b>"
    sent = bot.reply_to(message, response_text, parse_mode='HTML')
    soundcloud_data[sent.message_id] = {
        "user_id": message.from_user.id,
        "tracks": tracks
    }

@bot.message_handler(func=lambda msg: msg.reply_to_message and msg.reply_to_message.message_id in soundcloud_data)
def handle_soundcloud_selection(msg):
    reply_id = msg.reply_to_message.message_id
    if reply_id not in soundcloud_data:
        return
    user_id = msg.from_user.id
    data = soundcloud_data[reply_id]
    if user_id != data['user_id']:
        return
    text = msg.text.strip().lower()
    try:
        index = int(text.split()[0]) - 1
        if index < 0 or index >= len(data["tracks"]):
            bot.reply_to(msg, "🚫 Số không hợp lệ. Hãy nhập số từ 1-10.", parse_mode='HTML')
            return
    except (ValueError, IndexError):
        bot.reply_to(msg, "🚫 Vui lòng nhập số từ 1-10.", parse_mode='HTML')
        return
    track = data["tracks"][index]
    bot.reply_to(msg, f"🧭 Đang tải: {track['title']}", parse_mode='HTML')
    audio_url = get_music_stream_url(track)
    thumbnail_url = track.get('artwork_url', '').replace("-large", "-t500x500")
    if not audio_url or not thumbnail_url:
        bot.reply_to(msg, "🚫 Không tìm thấy nguồn audio hoặc thumbnail.", parse_mode='HTML')
        return
    caption = f"<b>🎵 {track['title']}</b>\n"
    caption += f"👤 Nghệ sĩ: {track['user']['username']}\n"
    caption += f"📊 Lượt nghe: {track['playback_count']:,} | Thích: {track['likes_count']:,}\n"
    caption += f"🎧 Nguồn: SoundCloud\n"
    caption += f"🎉 Chúc bạn thưởng thức âm nhạc vui vẻ!"
    try:
        bot.delete_message(msg.chat.id, reply_id)
    except:
        pass
    bot.send_photo(msg.chat.id, thumbnail_url, caption=caption, parse_mode='HTML')
    bot.send_audio(msg.chat.id, audio_url, title=track['title'], performer=track['user']['username'])
    del soundcloud_data[reply_id]


# --- Hàm load danh sách bảo trì từ file ---
def load_maintenance():
    import baotri
    importlib.reload(baotri)  # reload file để cập nhật khi có thay đổi
    return set(baotri.maintenance_commands)

# --- Hàm lưu danh sách bảo trì ra file ---
def save_maintenance(commands):
    with open("baotri.py", "w", encoding="utf-8") as f:
        f.write("# Danh sách lệnh đang bảo trì\n")
        f.write("maintenance_commands = [\n")
        for cmd in commands:
            f.write(f'    "{cmd}",\n')
        f.write("]\n")

# --- Lệnh /baotri <lenh> (bật bảo trì) ---
@bot.message_handler(commands=['baotri'])
def handle_baotri(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ Bạn không có quyền dùng lệnh này.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Dùng: /baotri <lenh>")
        return

    cmd = args[1].lower()
    maintenance = load_maintenance()
    if cmd in maintenance:
        bot.reply_to(message, f"⚠️ Lệnh `{cmd}` đã trong bảo trì rồi.")
    else:
        maintenance.add(cmd)
        save_maintenance(maintenance)
        bot.reply_to(message, f"✅ Đã thêm lệnh `{cmd}` vào bảo trì.")

# --- Lệnh /hoatdong <lenh> (gỡ bảo trì) ---
@bot.message_handler(commands=['hoatdong'])
def handle_hoatdong(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ Bạn không có quyền dùng lệnh này.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Dùng: /hoatdong <lenh>")
        return

    cmd = args[1].lower()
    maintenance = load_maintenance()
    if cmd not in maintenance:
        bot.reply_to(message, f"⚠️ Lệnh `{cmd}` không nằm trong bảo trì.")
    else:
        maintenance.remove(cmd)
        save_maintenance(maintenance)
        bot.reply_to(message, f"✅ Đã gỡ bảo trì lệnh `{cmd}`.")

# --- Lệnh /listbaotri ---
@bot.message_handler(commands=['listbaotri'])
def handle_list_baotri(message):
    maintenance = load_maintenance()
    if not maintenance:
        bot.reply_to(message, "✅ Hiện không có lệnh nào đang bảo trì.")
    else:
        cmds = "\n".join([f"• {cmd}" for cmd in maintenance])
        bot.reply_to(message, f"⚠️ Danh sách lệnh đang bảo trì:\n{cmds}")

# --- Check lệnh có đang bảo trì không ---
def is_under_maintenance(cmd):
    return cmd in load_maintenance()

USERS_FILE = "users.txt"

# --- Lưu user vào file ---
def save_user(user_id):
    user_id = str(user_id)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write("")
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if user_id not in users:
        with open(USERS_FILE, "a") as f:
            f.write(user_id + "\n")

# --- Lấy danh sách user từ file ---
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return f.read().splitlines()

# --- Khi bất kỳ ai nhắn bot thì lưu user ---
@bot.message_handler(func=lambda m: m.text and not m.text.startswith("/"))
def save_all_users(message):
    save_user(message.from_user.id)

# --- Lệnh /thongbao <văn bản> ---
@bot.message_handler(commands=['thongbao'])
def handle_broadcast(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ Bạn không có quyền dùng lệnh này.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Dùng: /thongbao <nội dung>")
        return

    content = args[1]
    users = load_users()

    success = 0
    fail = 0
    for uid in users:
        try:
            bot.send_message(uid, f"📢 Thông báo từ Admin:\n\n{content}")
            success += 1
        except:
            fail += 1

    bot.reply_to(message, f"✅ Đã gửi thông báo đến {success} người dùng.\n❌ Lỗi: {fail}.")


# Tạo thư mục lưu trữ nếu chưa có
import json, os, random
from telebot.types import ReplyKeyboardMarkup

# --- Cấu hình ---
users_file = "users.json"
login_file = "login.json"
code_file = "codes.json"
register_temp = {}
admin_id = [7239343492] # Thay bằng Telegram ID admin

# --- Hàm tiện ích ---
def load_json(file):
    if not os.path.exists(file): open(file, "w").write("{}")
    with open(file) as f: return json.load(f)

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f)

# --- MENU ---
@bot.message_handler(commands=["taixiu"])
def taixiu_menu(message):
    text = (
        "<pre>"
        "╭────[🎮 MENU TAIXIU]─────╮\n"
        "│ /dangky\n"
        "│ /dangnhap\n"
        "│ /thongtin\n"
        "│ /tangxu\n"
        "│ /batdau\n"
        "│ /top10\n"
        "│ /showcode\n"
        "│ /code\n"
        "╰────────────────────╯\n"
        "👉 Gõ lệnh hoặc bấm để chơi 🎲"
        "</pre>"
        "<blockquote>"
        "<code>"
        "🖥️Menu Admin\n"
        " /regcode"
        "</code>"
        "</blockquote>"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# --- Đăng ký ---
@bot.message_handler(commands=["dangky"])
def dangky(message):
    uid = str(message.from_user.id)
    try:
        bot.send_message(uid, "<b>📌 Bắt đầu đăng ký tài khoản</b>\n\n<blockquote>Gửi lệnh: /tk [tên đăng nhập]</blockquote>", parse_mode="HTML")
        register_temp[uid] = {"step": "tk"}
        if message.chat.type != "private":
            bot.reply_to(message, "📩 Mình đã nhắn tin riêng, kiểm tra tin nhắn riêng để tiếp tục đăng ký!")
    except:
        bot.reply_to(message, "⚠️ Vui lòng nhấn /start bot ở tin nhắn riêng trước khi đăng ký!")

@bot.message_handler(commands=["tk"])
def nhap_tk(message):
    uid = str(message.from_user.id)
    if uid in register_temp and register_temp[uid]["step"] == "tk":
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return bot.send_message(uid, "❗ Cú pháp đúng: /tk [tên đăng nhập]")
        ten = parts[1]
        register_temp[uid]["tk"] = ten
        register_temp[uid]["step"] = "mk"
        bot.send_message(uid, "<b>🔒 Nhập mật khẩu:</b>\nGửi lệnh: <blockquote>/mk [mật khẩu]</blockquote>", parse_mode="HTML")

@bot.message_handler(commands=["mk"])
def nhap_mk(message):
    uid = str(message.from_user.id)
    users = load_json(users_file)
    if uid in register_temp and register_temp[uid]["step"] == "mk":
        tk = register_temp[uid]["tk"]
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return bot.send_message(uid, "❗ Cú pháp đúng: /mk [mật khẩu]")
        mk = parts[1]
        if tk in users:
            bot.send_message(uid, "❌ Tài khoản đã tồn tại!")
        else:
            users[tk] = {"matkhau": mk, "xu": 1000, "win": 0, "lose": 0, "cuoc": 0, "uid": uid}
            save_json(users_file, users)
            bot.send_message(uid, f"✅ Đăng ký thành công với tài khoản <code>{tk}</code>!\nBạn có thể đăng nhập bằng lệnh:\n<blockquote>/dangnhap {tk} {mk}</blockquote>", parse_mode="HTML")
        del register_temp[uid]

# --- Đăng nhập ---
@bot.message_handler(commands=["dangnhap"])
def dangnhap(message):
    try:
        _, tk, mk = message.text.split()
        users = load_json(users_file)
        uid = str(message.from_user.id)

        if tk in users and users[tk]["matkhau"] == mk:
            login = load_json(login_file)
            login[uid] = tk
            save_json(login_file, login)

            # Nhắn riêng thông báo đăng nhập
            bot.send_message(uid,
                f"✅ <b>Đăng nhập thành công!</b>\n\n"
                f"<blockquote>👤 Username: <code>{tk}</code>\n💰 Số Dư: <code>{users[tk]['xu']} VND</code></blockquote>",
                parse_mode="HTML")

            # Nếu trong nhóm thì báo thành công
            if message.chat.type != "private":
                bot.reply_to(message, "📩 Đăng nhập thành công! Kiểm tra tin nhắn riêng để bắt đầu chơi 🎮")
        else:
            bot.send_message(uid, "❌ Tài khoản hoặc mật khẩu sai!")
    except:
        try:
            bot.send_message(message.from_user.id, "❗ Dùng đúng cú pháp: <code>/dangnhap tk mk</code>", parse_mode="HTML")
        except:
            bot.reply_to(message, "⚠️ Vui lòng nhấn /start bot trong tin nhắn riêng trước khi đăng nhập!")

# --- Thông tin ---
@bot.message_handler(commands=["thongtin"])
def thongtin(message):
    login = load_json(login_file)
    users = load_json(users_file)
    args = message.text.split()

    if len(args) == 1:
        uid = str(message.from_user.id)
        if uid not in login:
            bot.reply_to(message, "❌ Bạn chưa đăng nhập!")
            return
        username = login[uid]
    else:
        username = args[1]
        if username not in users:
            bot.reply_to(message, f"❌ Không tìm thấy người dùng \"{username}\"!")
            return

    u = users[username]
    reply = (f"<b>🎭 Thông Tin</b>\n<blockquote>👤 Username: {username}\n💰 Số Dư: {u['xu']}\n💸 Đã Cược: {u['cuoc']}\n🎯Thắng: {u['win']}\n🪦 Thua: {u['lose']}</blockquote>")
    bot.reply_to(message, reply, parse_mode="HTML")

# --- Bắt đầu chơi ---
@bot.message_handler(commands=["batdau"])
def batdau(message):
    uid = str(message.from_user.id)
    login = load_json(login_file)
    if uid not in login:
        return bot.reply_to(message, "❗ Vui lòng /dangnhap trước.")
    bot.send_message(message.chat.id, "<blockquote>💵 Nhập Số Tiền Cược</blockquote>", parse_mode="HTML")
    bot.register_next_step_handler(message, nhan_tien, login[uid])

def nhan_tien(message, tk):
    try:
        tien = int(message.text)
        users = load_json(users_file)
        if tien <= 0 or tien > users[tk]["xu"]:
            return bot.reply_to(message, "❌ Số Tiền Không Hợp Lệ!")
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Tài", "Xỉu")
        bot.send_message(message.chat.id, "<blockquote>🎯 Chọn Tài hoặc Xỉu</blockquote>", reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler_by_chat_id(
            message.chat.id,
            ketqua,
            tk,
            tien
        )
    except:
        bot.reply_to(message, "❗ Xu phải là số!")

def ketqua(message, tk, tien):
    chon = message.text.lower()
    if chon not in ["tài", "xỉu"]:
        return bot.reply_to(message, "❌ Chỉ được chọn Tài hoặc Xỉu!")
    dice = [random.randint(1, 6) for _ in range(3)]
    tong = sum(dice)
    kq = "tài" if tong >= 11 else "xỉu"
    users = load_json(users_file)
    msg = f"🎲 Kết quả: {kq.upper()}\n"
    if chon == kq:
        users[tk]["xu"] += tien
        users[tk]["win"] += 1
        msg += f"🎉 Bạn thắng! +{tien}VND"
    else:
        users[tk]["xu"] -= tien
        users[tk]["lose"] += 1
        msg += f"😥 Bạn thua! -{tien}VND"
    users[tk]["cuoc"] += tien
    save_json(users_file, users)
    bot.send_message(message.chat.id, msg)

# --- Tặng xu ---
@bot.message_handler(commands=["tangxu"])
def tangxu(message):
    login = load_json(login_file)
    users = load_json(users_file)
    uid = str(message.from_user.id)

    if uid not in login:
        return bot.reply_to(message, "❌ Bạn chưa đăng nhập!")

    try:
        _, tk_nhan, so_xu = message.text.split()
        tk_gui = login[uid]
        so_xu = int(so_xu)

        if tk_nhan not in users:
            return bot.reply_to(message, "❗ Người nhận không tồn tại!")

        if users[tk_gui]["xu"] < so_xu:
            return bot.reply_to(message, "❌ Bạn không đủ Tiền để tặng!")

        users[tk_gui]["xu"] -= so_xu
        users[tk_nhan]["xu"] += so_xu
        save_json(users_file, users)

        bot.reply_to(message,
            f"<b>🎁 Tặng Tiền Thành Công</b>\n"
            f"<blockquote>"
            f"👤 Người Gửi: <code>{tk_gui}</code>\n"
            f"👤 Người Nhận: <code>{tk_nhan}</code>\n"
            f"💸 Số Tiền: <code>{so_xu} Vnd</code>"
            f"</blockquote>",
            parse_mode="HTML")
    except:
        bot.reply_to(message, "❗ Cú pháp đúng: <code>/tangxu ten_nguoi_nhan so_tien</code>", parse_mode="HTML")

# --- Code ---
@bot.message_handler(commands=["code"])
def code_nhap(message):
    login = load_json(login_file)
    codes = load_json(code_file)
    uid = str(message.from_user.id)
    if uid not in login:
        return bot.reply_to(message, "❌ Bạn chưa đăng nhập!")
    try:
        _, code = message.text.split()
        tk = login[uid]
        users = load_json(users_file)
        if code in codes:
            xu = codes.pop(code)
            users[tk]["xu"] += xu
            save_json(code_file, codes)
            save_json(users_file, users)
            bot.reply_to(message, f"<blockquote>🎁 Nhập Code Thành Công\n💰 Số Dư: +{xu} Vnd!\n✅ Chúc Mừng Bạn Đã Nhập Code Thành Công, Chúc Bạn Chơi Game Vui Vẻ Và May Mắn!</blockquote>", parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ Code không hợp lệ hoặc đã dùng!")
    except:
        bot.reply_to(message, "❗ Dùng: /code <mã>")

@bot.message_handler(commands=["regcode"])
def regcode(message):
    if message.from_user.id not in admin_id:
        return bot.reply_to(message, "❌ Bạn không phải admin!")
    try:
        _, code, xu = message.text.split()
        codes = load_json(code_file)
        if code in codes:
            return bot.reply_to(message, "⚠️ Code đã tồn tại!")
        codes[code] = int(xu)
        save_json(code_file, codes)

        text = (
            f"✅ Tạo Code Thành Công\n"
            f"🎁 Code: <b>{code}</b>\n"
            f"💰 Giá Trị: <b>{xu} VND</b>\n"
            f"💳 Bạn Là 1 Admin Tốt Bụng, Quản Bot Tốt Nhé"
        )
        bot.reply_to(message, text, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❗ Dùng: /regcode <code> <xu>\nLỗi: {e}")

@bot.message_handler(commands=["showcode"])
def showcode(message):
    codes = load_json(code_file)
    if not codes:
        return bot.reply_to(message, "📭 Hiện Tại File Code Đang Rỗng")
    msg = "<blockquote>"
    for i, (c, x) in enumerate(codes.items(), 1):
        msg += f"{i}. <code>{c}</code>  {x}Vnd\n"
    msg += "</blockquote>"
    bot.reply_to(message, msg, parse_mode="HTML")

# --- Top 10 ---
@bot.message_handler(commands=["top10"])
def top10(message):
    users = load_json(users_file)
    if not users:
        return bot.reply_to(message, "❌ Chưa có người chơi nào!")
    sorted_users = sorted(users.items(), key=lambda x: x[1].get("xu", 0), reverse=True)
    msg = "🏆 <b>Top 10 Con Nghiện</b>\n"
    for i, (tk, data) in enumerate(sorted_users[:10], 1):
        msg += f"<blockquote>{i}. {tk} {data['xu']} xu\n</blockquote>"
    bot.reply_to(message, msg, parse_mode="HTML")



#Hàm Xử Lý Film
API_ENDPOINT = "https://phimmoi.sale/wp-json/dooplay/search/"
NONCE = "ab2604e03e"

@bot.message_handler(commands=['film'])
def search_film(message):
    auto_react_to_command(message)
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "❌ Bạn cần nhập tên phim.\nVí dụ: /film zombie")
        return

    keyword = args[1].strip()
    params = {
        'keyword': keyword,
        'nonce': NONCE
    }

    try:
        response = requests.get(API_ENDPOINT, params=params)
        data = response.json()

        if not data:
            bot.reply_to(message, f"❌ Không tìm thấy phim nào với từ khóa: *{keyword}*", parse_mode="Markdown")
            return

        for movie_id, movie in list(data.items())[:5]:  # Giới hạn 5 kết quả
            title = movie.get("title")
            url = movie.get("url")
            img = movie.get("img")

            caption = f"*{title}*\n👉 [Xem phim tại đây]({url})"
            bot.send_photo(message.chat.id, img, caption=caption, parse_mode="Markdown", reply_to_message_id=message.message_id)

    except Exception as e:
        bot.reply_to(message, "❗ Đã xảy ra lỗi khi kết nối đến server.")
        print(e)


import random
import logging
emoji_list = [
    '👍',  # Like
    '👎',  # Dislike
    '❤️',  # Heart
    '🔥',  # Fire
    '👏',  # Clapping
    '😁',  # Grinning
    '😢',  # Crying
    '😮',  # Surprised
    '😡',  # Angry
    '🤯',  # Mind blown
    '🥳',  # Party
    '🤔',  # Thinking
    '🤡',  # Clown
    '💩',  # Poop
    '🙈',  # See no evil
    '😎',  # Cool
    '💯',  # 100
    '🥴',  # Dizzy
    '😆',  # Laughing hard
    '😐',  # Neutral
    '🤮',  # Vomit
    '🫡',  # Salute (mới hơn)
    '🙃',  # Upside down
    '💋',  # Kiss
    '😈',  # Smiling devil
    '👀',  # Eyes
    '🤗',  # Hug
    '☠️',  # Skull
    '🫶',  # Heart hands
]

# Trạng thái auto reaction cho từng nhóm
react_status = {}

# Kiểm tra admin
def is_user_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except Exception as e:
        print(f"Lỗi kiểm tra admin: {e}")
        return False

# Hàm thả cảm xúc thật
def tha_camxuc(chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{TOKEN}/setMessageReaction"
    data = {
        'chat_id': chat_id,
        'message_id': message_id,
        'reaction': json.dumps([{'type': 'emoji', 'emoji': emoji}])
    }
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"Lỗi khi gọi API thả cảm xúc: {e}")
        return None

# Hàm gọi auto thả cảm xúc
def auto_react_to_command(message):
    chat_id = message.chat.id
    message_id = message.message_id

    if message.from_user.id == bot.get_me().id:
        return

    if not react_status.get(chat_id, True):
        return

    random_emoji = random.choice(emoji_list)
    print(f"Thả cảm xúc {random_emoji} cho lệnh {message.text}")

    result = tha_camxuc(chat_id, message_id, random_emoji)
    if not result or not result.get('ok'):
        print(f"Lỗi thả cảm xúc: {result.get('description') if result else 'Không rõ lỗi'}")
        if random_emoji != "🎉":
            tha_camxuc(chat_id, message_id, "🎉")

# Lệnh /react để bật/tắt auto
@bot.message_handler(commands=['react'], chat_types=['group', 'supergroup'])
def toggle_react(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, "Chỉ admin mới được dùng lệnh này!")
        return

    current_state = react_status.get(chat_id, True)
    state_text = "BẬT" if current_state else "TẮT"

    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Bật tự động", callback_data="react_on"),
        InlineKeyboardButton("Tắt tự động", callback_data="react_off")
    )
    keyboard.row(InlineKeyboardButton("Đóng", callback_data="react_close"))

    bot.send_message(chat_id, f"Chế độ tự động thả cảm xúc hiện đang {state_text}. Chọn tùy chọn:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('react_'))
def handle_react_callback(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    message_id = call.message.message_id
    data = call.data

    if not is_user_admin(chat_id, user_id):
        bot.answer_callback_query(call.id, "Chỉ admin mới được dùng tính năng này!", show_alert=True)
        return

    if data == "react_on":
        react_status[chat_id] = True
        new_text = "✅ Đã bật chế độ tự động thả cảm xúc!"
    elif data == "react_off":
        react_status[chat_id] = False
        new_text = "❌ Đã tắt chế độ tự động thả cảm xúc!"
    elif data == "react_close":
        try:
            bot.delete_message(chat_id, message_id)
        except Exception as e:
            print(f"Lỗi xóa tin nhắn: {e}")
        return

    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Đóng", callback_data="react_close"))

    try:
        bot.edit_message_text(new_text, chat_id, message_id, reply_markup=keyboard)
    except Exception as e:
        print(f"Lỗi khi sửa tin nhắn: {e}")

    bot.answer_callback_query(call.id)

# Xử lý các tin nhắn thường (không phải lệnh)
# ❌ Không thả cảm xúc cho tin nhắn thường
@bot.message_handler(func=lambda m: m.text and not m.text.startswith("/"), chat_types=['group', 'supergroup'])
def ignore_regular_messages(message):
    pass  # Bỏ qua tin nhắn thường

# ✅ Thả cảm xúc cho tất cả các lệnh
@bot.message_handler(func=lambda m: m.text and m.text.startswith("/"), chat_types=['group', 'supergroup'])
def react_to_command(message):
    auto_react_to_command(message)

    
if __name__ == "__main__":
    bot_active = True
    bot.infinity_polling()

