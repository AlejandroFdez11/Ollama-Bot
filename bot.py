import logging
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import config, memoria, ollama_client

logging.basicConfig(level=logging.INFO)

def autorizado(update: Update) -> bool:
    return update.effective_user and update.effective_user.id == config.ALLOWED_USER_ID

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update): return
    await update.message.reply_text("Listo. Escríbeme. /reset borra el historial.")

async def reset(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update): return
    memoria.borrar(update.effective_user.id)
    await update.message.reply_text("Historial borrado.")

async def mensaje(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update): return
    uid = update.effective_user.id
    await ctx.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    memoria.añadir(uid, "user", update.message.text)
    try:
        respuesta = await ollama_client.chat(memoria.obtener(uid))
    except Exception as e:
        await update.message.reply_text(f"Error con Ollama: {e}")
        return
    memoria.añadir(uid, "assistant", respuesta)
    for i in range(0, len(respuesta), 4000):  # límite de Telegram: 4096
        await update.message.reply_text(respuesta[i:i+4000])

def main():
    app = ApplicationBuilder().token(config.TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))
    app.run_polling()

if __name__ == "__main__":
    main()