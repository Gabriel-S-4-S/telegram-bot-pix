from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ===== CONFIG =====
TOKEN = "8529002340:AAFNgPwyvE2WK3UK8B7zrE2h2rZo7P_x1qw"
ADMIN_ID = 8768911632

PIX = "11 96105-0894"
LINK_GRUPO = "https://t.me/+NKQd-ePKROBiN2Vh"
# ==================

# ===== MENSAGEM INICIAL =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = f"""
💎 ACESSO VIP 💎

Para entrar no grupo exclusivo:

1️⃣ Faça o pagamento via PIX:
🔑 {PIX}

2️⃣ Envie o comprovante aqui no chat 📩

3️⃣ Aguarde aprovação do administrador

⚠️ Sem comprovante, o acesso NÃO será liberado.

🔥 Após aprovação, você receberá o link do grupo.
"""
    await update.message.reply_text(mensagem)

# ===== RECEBER MENSAGENS =====
async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Resposta automática
    await update.message.reply_text("📩 Comprovante recebido! Aguarde verificação.")

    # Encaminha para você
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )

    print(f"Mensagem de {user.username or user.first_name}")

# ===== INICIAR BOT =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, receber_mensagem))

app.run_polling()
