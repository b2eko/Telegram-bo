from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import asyncio

# تفاصيل اللعبة
PLAYERS = {}
FINISH_LINE = 20  # نقطة النهاية للمضمار
CHARACTERS = {"beko": "ذكر 🧔", "noori": "أنثى 👩"}

# دالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    PLAYERS[chat_id] = {"beko": 0, "noori": 0, "turn": None}
    await update.message.reply_text(
        "مرحباً بكم في لعبة 'نوري'! 🏆\nاختر شخصيتك بكتابة:\n"
        "/choose beko - للعب بشخصية beko 🧔\n"
        "/choose noori - للعب بشخصية noori 👩\n"
        "أول من يصل إلى النهاية يفوز بالجورب الأزرق 🧦."
    )

# دالة اختيار الشخصية
async def choose_character(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id not in PLAYERS:
        await update.message.reply_text("استخدم /start لبدء اللعبة أولاً.")
        return

    if not context.args or context.args[0] not in CHARACTERS:
        await update.message.reply_text("اختر شخصية صالحة:\n/choose beko\n/choose noori")
        return

    character = context.args[0]
    if PLAYERS[chat_id]["turn"] is None:
        PLAYERS[chat_id]["turn"] = character
        await update.message.reply_text(f"اخترت {CHARACTERS[character]}! يمكنك البدء باللعب الآن عبر /play.")
    else:
        await update.message.reply_text("لقد اخترت شخصيتك بالفعل. اكتب /play للبدء.")

# دالة اللعب
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id not in PLAYERS:
        await update.message.reply_text("استخدم /start لبدء اللعبة أولاً.")
        return

    game = PLAYERS[chat_id]
    player = game["turn"]

    if player is None:
        await update.message.reply_text("اختر شخصيتك أولاً باستخدام /choose.")
        return

    opponent = "noori" if player == "beko" else "beko"
    
    # توليد عقبة عشوائية
    obstacle = random.choice([True, False])
    
    if obstacle:
        # إذا اصطدم اللاعب بالعقبة
        await update.message.reply_text(f"{CHARACTERS[player]} اصطدم بالعقبة! الدلو الأزرق 🚧💥.\nانتهت اللعبة!")
        del PLAYERS[chat_id]
    else:
        # تقدم اللاعب خطوة
        game[player] += 1
        await update.message.reply_text(f"{CHARACTERS[player]} تقدم خطوة! 🚶‍♂️✨")

        # تحقق من الفوز
        if game[player] >= FINISH_LINE:
            await update.message.reply_text(f"🎉 {CHARACTERS[player]} فاز بالجورب الأزرق 🧦! مبروك!")
            del PLAYERS[chat_id]
        else:
            # تبديل الدور بين اللاعبين
            game["turn"] = opponent
            await update.message.reply_text(f"الدور الآن لـ {CHARACTERS[opponent]}.")

# دالة رئيسية لتشغيل البوت
def main():
    application = ApplicationBuilder().token("7915948643:AAHnicKuYw_ocUQVffmYGIv-demCParx29Q").build()

    # إضافة المعالجات للأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("choose", choose_character))
    application.add_handler(CommandHandler("play", play))

    # بدء البوت
    application.run_polling()

if name == "main":
    main()