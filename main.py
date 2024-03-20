import logging
from typing import Dict
import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Chain", "TokenOutAddress"],
    ["BNB", "Private Key"],
    ["Add comments"],
    ["OK", "Cancel"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for the data."""
    await update.message.reply_text(
        "Hello! I am ArchieBot. Please input the token data for buying or selling",
        reply_markup=markup,
    )

    return CHOOSING

async def select_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for the Chain that they want"""
    text = update.message.text
    context.user_data["choice"] = text

    reply_chains = [
        ["BSC"],
        ["Avalanche"],
    ]
    chain_type = ReplyKeyboardMarkup(reply_chains, one_time_keyboard=True)

    await update.message.reply_text(
        "Please choose the chain you want",
        reply_markup=chain_type
    )

    return TYPING_REPLY

async def select_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for the Chain that they want"""
    text = update.message.text
    print(text)
    category = user_data["chain"]
    user_data[category] = text

    return CHOOSING

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the data that the user input"""
    text = update.message.text
    print("regular choice ----",text)
    context.user_data["choice"] = text

    if text == "Private Key":
        await update.message.reply_text("Please enter your private key")
    else:
        await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")

    return TYPING_REPLY
# async def cancel_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """If the user click the cancel button, then the bot will redirect the first paeg"""

#     text = update.message.text
#     print("cancel ------",text)
#     context.user_data['choice'] = text
#     # if text
async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "MEMO" or "I have sell some tokens because of the price change."'
    )

    return TYPING_CHOICE


# Function to validate the private key
def is_valid_private_key(private_key: str) -> bool:
    private_key = private_key.strip()

    # if len(private_key) != 64:
    #     print('Length here=-----------')
    #     return False

    if not re.match('^[0-9a-fA-F]+$', private_key):
        print('here=-----------')
        return False

    return True

# Canccel the conversation and clear user data.
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    user_data.clear()
    await update.message.reply_text(
        "Transaction canceled. You can start a new transaction by typing /start.",
        reply_markup=ReplyKeyboardRemove(),        
    )
    return ConversationHandler.END

# Update the received_information function to include private key validation
async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]

    if category == "BNB":
        if not text.isdigit():
            await update.message.reply_text("Please enter the amount of BNB!")
            return TYPING_REPLY
        
        if category == "TokenOutAddress":
            if not isinstance(text, str):
                await update.message.reply_text("Please enter valide token address as string")
                return TYPING_REPLY

    if category == "Private Key":
        if not is_valid_private_key(text):
            await update.message.reply_text("Please enter a valid private key.")
            return TYPING_REPLY

        # Mask the private key before displaying it
        masked_private_key = text[:3] + "..." + text[-3:]
        user_data[category] = masked_private_key
    else:
        user_data[category] = text

    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " add comments",
        reply_markup=markup,
    )

    return CHOOSING

async def OK(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]
    if user_data == {}:
        await update.message.reply_text(
            "Please input correctly",
            reply_markup=ReplyKeyboardRemove()
        )

    await update.message.reply_text(
        f"Your input data: {facts_to_str(user_data)} Just a minute!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END

# async def Cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """"If the user click the cancel button, the bot will redirect to the first page."""
#     user_data = context.user_data
#     if "choice" in user_data:


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7071537775:AAFD479QCXCFL6DB8A3cQkFALRznXsAUG44").build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^Chain$"), select_choice
                ),
                MessageHandler(filters.Regex("^BSC"), select_chain),
                MessageHandler(filters.Regex("^Avalanche"), select_chain),
                MessageHandler(
                    filters.Regex("^(TokenOutAddress|BNB|Private Key)$"), regular_choice
                ),
                MessageHandler(filters.Regex("^Something else...$"), custom_choice),
                MessageHandler(filters.Regex("^Cancel$"), cancel)
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^OK$")), regular_choice
                ),
                # MessageHandler(
                #     filters.TEXT & ~(filters.COMMAND | filters.Regex("^Cancel$")), cancel_choice
                # )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^OK$")),
                    received_information,
                )
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex("^OK$"), OK),
            MessageHandler(filters.Regex("^Cancel$"), cancel),
            ],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()