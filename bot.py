import telebot, time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from database import *
from security import get_password

bot = telebot.TeleBot(BOT_TOKEN)

def is_admin(uid):
    return uid in ADMINS

def joined(chat, uid):
    try:
        s = bot.get_chat_member(chat, uid).status
        return s in ["member","administrator","creator"]
    except:
        return False

def menu(uid):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔑 Get Password", callback_data="pass"),
        InlineKeyboardButton("🆔 My UID", callback_data="uid"),
        InlineKeyboardButton("📜 Status", callback_data="status")
    )
    if is_admin(uid):
        kb.add(
            InlineKeyboardButton("➕ Add UID", callback_data="admin_add"),
            InlineKeyboardButton("➖ Remove UID", callback_data="admin_remove"),
            InlineKeyboardButton("📋 List UID", callback_data="admin_list")
        )
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🔥 Premium Access Bot", reply_markup=menu(m.from_user.id))

@bot.message_handler(commands=['adduid'])
def adduid_command(m):
    if not is_admin(m.from_user.id):
        return bot.reply_to(m, "❌ You are not admin")
    try:
        parts = m.text.split()
        uid = int(parts[1])
        minutes = int(parts[2])
        add_user(uid,"admin",minutes)
        bot.reply_to(m, f"✅ UID {uid} added for {minutes} mins")
    except:
        bot.reply_to(m, "Usage: /adduid <UID> <minutes>")

@bot.message_handler(commands=['removeuid'])
def removeuid_command(m):
    if not is_admin(m.from_user.id):
        return bot.reply_to(m, "❌ You are not admin")
    try:
        uid = int(m.text.split()[1])
        remove_user(uid)
        bot.reply_to(m, f"✅ UID {uid} removed")
    except:
        bot.reply_to(m, "Usage: /removeuid <UID>")

@bot.message_handler(commands=['listuid'])
def listuid_command(m):
    if not is_admin(m.from_user.id):
        return bot.reply_to(m, "❌ You are not admin")
    users = list_users()
    text = "📋 Active Users:\n"
    for u in users:
        text += f"UID: {u[0]}, Expires: {time.ctime(u[2])}\n"
    bot.reply_to(m, text)

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    uid = c.from_user.id
    if c.data == "uid":
        bot.send_message(c.message.chat.id, f"Your UID: `{uid}`", parse_mode="Markdown")
    if c.data == "status":
        u = get_user(uid)
        if not u or u[2] < int(time.time()):
            bot.send_message(c.message.chat.id,"❌ No active access")
        else:
            bot.send_message(c.message.chat.id,"✅ Active access")
    if c.data == "pass":
        if not joined(CHANNEL_USERNAME, uid) or not joined(GROUP_USERNAME, uid):
            bot.send_message(c.message.chat.id,"❌ Join channel & group first")
            return
        u = get_user(uid)
        if not u or u[2] < int(time.time()):
            bot.send_message(c.message.chat.id,"⏳ Access expired")
            return
        bot.send_message(c.message.chat.id, f"🔐 Password: `{get_password()}`", parse_mode="Markdown")

print("Bot running...")
bot.infinity_polling()
