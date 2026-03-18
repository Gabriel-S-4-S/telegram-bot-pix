from flask import Flask
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ===== KEEP ALIVE COM FLASK =====
app = Flask("")

@app.route("/")
def home():
    return "Bot ativo!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# ===== BOT TELEGRAM =====
TOKEN = "8529002340:AAFNgPwyvE2WK3UK8B7zrE2h2rZo7P_x1qw"  # Seu token fornecido
ADMIN_ID = 8768911632
PIX = "11 96105-0894"
LINK_GRUPO = "https://t.me/+NKQd-ePKROBiN2Vh"

# Função /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = f"""
💎 ACESSO VIP 💎

1️⃣ PIX: {PIX}
2️⃣ Envie o comprovante aqui
3️⃣ Aguarde aprovação

Link: {LINK_GRUPO}
"""
    await update.message.reply_text(mensagem)

# Função para receber qualquer mensagem
async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text("📩 Comprovante recebido! Aguarde verificação.")
    # Encaminha mensagem para o admin
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    print(f"Mensagem de {user.username or user.first_name}")

# ===== INICIAR BOT =====
app_bot = ApplicationBuilder().token(TOKEN).build()
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(MessageHandler(filters.ALL, receber_mensagem))

keep_alive()  # inicia Flask para Uptime Robot
app_bot.run_polling()
