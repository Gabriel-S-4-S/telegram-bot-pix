from flask import Flask
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ===== KEEP ALIVE =====
app = Flask("")

@app.route("/")
def home():
    return "Bot ativo!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# ===== CONFIG =====
TOKEN = "8529002340:AAFNgPwyvE2WK3UK8B7zrE2h2rZo7P_x1qw"
ADMIN_ID = 8117675695
PIX = "11944712407"

# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = f"""
💎 ACESSO VIP 💎

Para entrar no grupo exclusivo:

1️⃣ Faça o pagamento via PIX de 15R$:
🔑 {PIX}

2️⃣ Envie o comprovante aqui no chat 📩

3️⃣ Aguarde aprovação do administrador

⚠️ Sem comprovante, o acesso NÃO será liberado.

🔥 Após aprovação, você receberá o link do grupo.

Qualquer dúvida digite aqui no Chat, logo um atendente irá responde-lo.
"""

    keyboard = [
        [InlineKeyboardButton("📋 Copiar chave PIX", callback_data="copiar_pix")],
        [InlineKeyboardButton("🎬 ANIMES EM CARTAZ", callback_data="animes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(mensagem)
    await update.message.reply_text("👇 Escolha uma opção:", reply_markup=reply_markup)

# ===== BOTÕES =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # botão copiar pix
    if query.data == "copiar_pix":
        await query.message.reply_text(f"🔑 Chave PIX:\n\n{PIX}")

    # botão lista de animes
    elif query.data == "animes":
        lista = """
🎬 ANIMES EM CARTAZ:

• Vigilantes
• Lazarus
• Histórias macabras do Japão
• Jujutsu Kaisen
• O Castelo Animado
• A Viagem de Chihiro
• Serviço de Entregas da Kiki
• Boku no Hero
• Diário de uma apotecária 
• Dandadan
• Spy Family
"""
        await query.message.reply_text(lista)

# ===== RECEBER MENSAGENS =====
async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text("📩 Comprovante recebido! Aguarde verificação.")

    # encaminhar pro admin
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )

    print(f"Mensagem de {user.username or user.first_name}")

# ===== INICIAR =====
keep_alive()

app_bot = ApplicationBuilder().token(TOKEN).build()

app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CallbackQueryHandler(button_handler))
app_bot.add_handler(MessageHandler(filters.ALL, receber_mensagem))

app_bot.run_polling()
