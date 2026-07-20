import logging
import os
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from prompt_cleaner import clean_prompt
from config import TELEGRAM_TOKEN
from ai_client import ask_ai
from image_gen import generate_image
from database import init_db, add_user, increase_messages, get_stats
from vision_client import analyze_image
from image_edit import save_user_image, edit_image

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# In-memory storage
chat_history = {}
user_modes = {}
user_edit_images = {}
user_languages = {}

def tr(user_id, fa, en):
    if user_languages.get(user_id, "English") == "Persian":
        return fa
    return en

MENU = [
    ["💬 AI Chat", "🎨 Create Image"],
    ["🖼 Analyze Image", "✨ Edit Image"],
    ["✍️ Write Text", "🧠 Brainstorm"],
    ["🧾 Create Prompt", "⚙️ Settings"],
    ["🧹 Clear Memory"]
]

def get_menu(user_id):
    if user_languages.get(user_id, "English") == "Persian":
        return [
            ["💬 چت هوش مصنوعی", "🎨 ساخت تصویر"],
            ["🖼 تحلیل تصویر", "✨ ویرایش تصویر"],
            ["✍️ نوشتن متن", "🧠 ایده‌پردازی"],
            ["🧾 ساخت پرامپت", "⚙️ تنظیمات"],
            ["🧹 پاک کردن حافظه"]
        ]
    return MENU

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)
    
    user_modes[user_id] = "chat"
    chat_history[user_id] = []
    
    from telegram import ReplyKeyboardMarkup
    keyboard = ReplyKeyboardMarkup(
        get_menu(user_id),
        resize_keyboard=True
    )
    
    await update.message.reply_text(
        "Hello 🤖\n\n"
        "Welcome to PromptBot.\n"
        "Choose an option:",
        reply_markup=keyboard
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users, messages = get_stats()
    
    await update.message.reply_text(
        "📊 PromptBot Statistics\n\n"
        f"👥 Users: {users}\n"
        f"💬 Messages: {messages}\n"
        "🟢 Status: Online"
    )

async def clear_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_history[user_id] = []
    
    await update.message.reply_text(
        "🧹 Memory cleared."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_modes.get(user_id) == "waiting_edit_prompt":
        image_path = f"user_{user_id}.png"
        
        await update.message.reply_text(
            "🎨 Editing image... Please wait."
        )
        
        result = edit_image(image_path, text)
        
        if result:
            await update.message.reply_photo(photo=result)
        else:
            await update.message.reply_text(
                "❌ Image editing failed."
            )
        
        user_modes[user_id] = "chat"
        return
    
    if user_id not in chat_history:
        chat_history[user_id] = []
        user_modes[user_id] = "chat"
    
    if text == "💬 AI Chat" or text == "💬 چت هوش مصنوعی":
        user_modes[user_id] = "chat"
        await update.message.reply_text(
            "💬 AI Chat mode activated."
        )
        return
    
    if text == "🎨 Create Image" or text == "🎨 ساخت تصویر":
        user_modes[user_id] = "image"
        await update.message.reply_text(
            "🎨 Send me an image description."
        )
        return
    
    if text == "🖼 Analyze Image" or text == "🖼 تحلیل تصویر":
        user_modes[user_id] = "analyze_image"
        await update.message.reply_text(
            "🖼 Send me an image. I will create a detailed AI prompt from it."
        )
        return
    
    if text == "✨ Edit Image" or text == "✨ ویرایش تصویر":
        user_modes[user_id] = "edit_image"
        await update.message.reply_text(
            "✨ Send me the image you want to edit."
        )
        return
    
    if text == "✍️ Write Text" or text == "✍️ نوشتن متن":
        user_modes[user_id] = "writing"
        await update.message.reply_text(
            "✍️ Tell me what text you need."
        )
        return
    
    if text == "🧠 Brainstorm" or text == "🧠 ایده‌پردازی":
        user_modes[user_id] = "ideas"
        await update.message.reply_text(
            "🧠 Tell me your idea."
        )
        return
    
    if text == "🧾 Create Prompt" or text == "🧾 ساخت پرامپت":
        user_modes[user_id] = "prompt"
        await update.message.reply_text(
            "🧾 Send your topic."
        )
        return
    
    if text == "🧹 Clear Memory" or text == "🧹 پاک کردن حافظه":
        chat_history[user_id] = []
        await update.message.reply_text(
            "🧹 Memory cleared."
        )
        return
    
    # Settings
    if text == "⚙️ Settings" or text == "⚙️ تنظیمات":
        from telegram import ReplyKeyboardMarkup
        keyboard = ReplyKeyboardMarkup(
            [
                ["🌐 Language", "🎨 Image Settings"],
                ["⬅️ Back"]
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "⚙️ Settings Menu:",
            reply_markup=keyboard
        )
        return
    
    if text == "🎨 Image Settings":
        from telegram import ReplyKeyboardMarkup
        keyboard = ReplyKeyboardMarkup(
            [
                ["📐 Image Size"],
                ["🎭 Style"],
                ["⬅️ Back"]
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "🎨 Image Settings:",
            reply_markup=keyboard
        )
        return
    
    if text == "📐 Image Size":
        from telegram import ReplyKeyboardMarkup
        keyboard = ReplyKeyboardMarkup(
            [
                ["512x512", "1024x1024"],
                ["1792x1024"],
                ["⬅️ Back"]
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "📐 Choose image size:",
            reply_markup=keyboard
        )
        return
    
    if text == "🎭 Style":
        from telegram import ReplyKeyboardMarkup
        keyboard = ReplyKeyboardMarkup(
            [
                ["Realistic", "Anime"],
                ["Cinematic", "Fantasy"],
                ["3D Render", "Digital Art"],
                ["Oil Painting", "Watercolor"],
                ["Cyberpunk", "Sci-Fi"],
                ["Portrait", "Minimal"],
                ["⬅️ Back"]
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "🎭 Choose image style:",
            reply_markup=keyboard
        )
        return
    
    if text == "🌐 Language" or text == "🌐 زبان":
        from telegram import ReplyKeyboardMarkup
        keyboard = ReplyKeyboardMarkup(
            [
                ["🇬🇧 English", "🇮🇷 فارسی"],
                ["⬅️ Back"]
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(
            "🌐 Choose language:",
            reply_markup=keyboard
        )
        return
    
    if text == "🇮🇷 فارسی":
        user_languages[user_id] = "Persian"
        await update.message.reply_text(
            "✅ زبان روی فارسی تنظیم شد."
        )
        return
    
    if text == "🇬🇧 English":
        user_languages[user_id] = "English"
        await update.message.reply_text(
            "✅ Language set to English."
        )
        return
    
    if text == "⬅️ Back":
        from telegram import ReplyKeyboardMarkup
        keyboard = ReplyKeyboardMarkup(
            get_menu(user_id),
            resize_keyboard=True
        )
        await update.message.reply_text(
            "Main menu:",
            reply_markup=keyboard
        )
        return
    
    # Image generation
    if user_modes.get(user_id) == "image":
        await update.message.reply_text("🎨 Generating image... Please wait.")
        image = generate_image(text)
        
        if image:
            await update.message.reply_photo(
                photo=image,
                caption="✅ Image created!"
            )
        else:
            await update.message.reply_text(
                "❌ Image generation failed."
            )
        
        user_modes[user_id] = "chat"
        return
    
    # AI Chat
    chat_history[user_id].append({
        "role": "user",
        "content": text
    })
    increase_messages(user_id)
    
    answer = ask_ai(chat_history[user_id])
    
    chat_history[user_id].append({
        "role": "assistant",
        "content": answer
    })
    
    await update.message.reply_text(answer)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_modes.get(user_id) == "edit_image":
        photo = update.message.photo[-1]
        file = await photo.get_file()
        image_bytes = await file.download_as_bytearray()
        
        save_user_image(user_id, image_bytes)
        
        await update.message.reply_text(
            "✏️ Great! Now tell me what you want to change in the image."
        )
        user_modes[user_id] = "waiting_edit_prompt"
        return
    
    if user_modes.get(user_id) != "analyze_image":
        await update.message.reply_text(
            "Please choose 🖼 Analyze Image first."
        )
        return
    
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_bytes = await file.download_as_bytearray()
    
    await update.message.reply_text("🔍 Analyzing image...")
    
    prompt = analyze_image(image_bytes)
    prompt = clean_prompt(prompt)
    
    prompt = ask_ai([
        {
            "role": "system",
            "content": "Convert this image analysis into one professional AI image generation prompt. Return only the final prompt."
        },
        {
            "role": "user",
            "content": prompt
        }
    ])
    
    await update.message.reply_text(
        "🎨 Generated Prompt:\n\n" + prompt
    )
    
    user_modes[user_id] = "chat"

def main():
    init_db()
    
    # Flask app for keep-alive
    flask_app = Flask(__name__)
    
    @flask_app.route("/", methods=["GET"])
    def health_check():
        return "PromptBot is running! 🤖", 200
    
    # Telegram app
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .build()
    )
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear_memory))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    ))
    
    logger.info("PromptBot started 🤖 (Polling Mode)")
    
    # Start polling in a non-blocking way
    port = int(os.getenv("PORT", 5000))
    
    # Start Flask in background
    from threading import Thread
    flask_thread = Thread(target=lambda: flask_app.run(host="0.0.0.0", port=port, debug=False))
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run polling (blocking)
    app.run_polling()

if __name__ == "__main__":
    main()
