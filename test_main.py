import logging
from typing import Dict
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
    print("here is start ====>")
    await update.message.reply_text(
        f"Please choose the {emoji.emojize(':link:')} chain you want",
        reply_markup=chain_markup
    )
    return TYPING_REPLY

async def select_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = update.message.text
    print("user_data ===============>suer_data", user_data)
    if user_data == "BSC":
        await update.message.reply_text(
            f"You selected {emoji.emojize(':link:')} {user_data} chain!!! \nPlease select the option of buy and sell tokens"
        )
        print("here is BSC")
    else:
        await update.message.reply_text(
            f"Sorry. You selected {user_data}. But this chain is not supported yet! \nThank you"
        )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Help command"""
    await update.message.reply_text(
        "To start the transaction please input command /start."
    )

async def quit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Redirect the user when he or she input the command /quit..."""
    await update.message.reply_text(
        "Transaction cancelled. You can start a new transaction by typing /start.",
    )
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(Bot_Token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("help", help)],
        states={
            TYPING_REPLY: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^OK$")), select_chain)],
        },
        fallbacks=[
                   CommandHandler("help", help), CommandHandler("quit", quit)
                   ]
    )

    application.add_handler(conv_handler)

    """Run the bot until the user press Ctrl-C"""
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()