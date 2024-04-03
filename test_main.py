import logging
from typing import Dict
import re
import emoji
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import Bot_Token
from  swap_tokens import initialize_buy, initialize_sell

"""Enable logging"""
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

"""set higher logging level for httpx to avoid all GET and POST requests being logged"""
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, TYPING_PRIVATE_KEY, SELL_CHOOSING, SELL_TYPING_REPLY = range(6)

chain_reply_keyboard = [
    [{"text": "BSC", "request_contact": False}],
    [{"text": "Avax", "request_contact": False}],
    [{"text": "Solana", "request_contact": False}]
]

chain_markup = ReplyKeyboardMarkup(chain_reply_keyboard, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Return to the transaction"""
    await update.message.reply_text(
        f"Please choose the {emoji.emojize(':link')} chain you want",
        reply_markup=chain_markup
    )
    return TYPING_REPLY

async def select_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(context)

def main() -> None:
    application = Application.builder().token(Bot_Token).build()

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler("start", start)],
        states = {
            
        }
    )

if __name__ == "__name__":
    main()