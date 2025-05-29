import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from openai import OpenAI # Import the OpenAI library

#Telegram Token 
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Replace YOUR_OPENAI_API_KEY with the key you got from OpenAI
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"


client = OpenAI(api_key=OPENAI_API_KEY)
async def start(update: Update, context):
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! I'm your AI assistant. Ask me anything!")

async def handle_message(update: Update, context):
    """Processes user messages and sends them to OpenAI for a response."""
    user_message = update.message.text
    print(f"User message: {user_message}") # For debugging

    if not user_message:
        await update.message.reply_text("Please send a text message.")
        return

    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the AI's response
        ai_response = completion.choices[0].message.content
        print(f"AI response: {ai_response}") 
        await update.message.reply_text(ai_response)
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        await update.message.reply_text("Sorry, I'm having trouble connecting to the AI right now. Please try again later.")

async def main():
    """Starts the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is polling for updates...You can Close it with Ctrl+C")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
