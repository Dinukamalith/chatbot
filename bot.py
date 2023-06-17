import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables from .env file
load_dotenv()

# Telegram Bot token from BotFather
TOKEN = os.getenv("TELEGRAM_TOKEN")

# ChatGPT API token from OpenAI
GPT_API_KEY = os.getenv("GPT_API_KEY")
GPT_API_URL = "https://api.openai.com/v1/chat/completions"

# Speech generation API endpoint
TTS_API_URL = "https://text-to-speech-api-provider.com/api"

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    """Handler for the /start command."""
    update.message.reply_text("Hello! I'm your ChatGPT bot. Send me a message and I'll respond.")

def echo(update: Update, context: CallbackContext) -> None:
    """Handler for all text messages."""
    message = update.message.text
    response = chat_with_gpt(message)
    speech_url = generate_speech(response)
    update.message.reply_audio(speech_url)

def chat_with_gpt(message: str) -> str:
    """Send the user's message to ChatGPT and get a response."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_API_KEY}"
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are ChatGPT."},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(GPT_API_URL, headers=headers, json=payload)
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"]

def generate_speech(text: str) -> str:
    """Generate speech from the provided text using the TTS API."""
    response = requests.post(TTS_API_URL, json={"text": text})
    response_json = response.json()
    return response_json["audio_url"]

def main() -> None:
    """Main function to start the bot."""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the bot
    updater.start_polling()
    logging.info("Bot started!")

    # Run the bot until Ctrl-C is pressed
    updater.idle()

if __name__ == "__main__":
    main()
