import logging
from typing import Dict
from cryptography.fernet import Fernet
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
    ["Something else..."],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

# Generate a secret key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt the private key
def encrypt_private_key(private_key):
    encrypted_private_key = cipher_suite.encrypt(private_key.encode())
    return encrypted_private_key

# Decrypt the private key
def decrypt_private_key(encrypted_private_key):
    decrypted_private_key = cipher_suite.decrypt(encrypted_private_key).decode()
    return decrypted_private_key

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Hello! I am ArchieBot. Please input the data for buying or selling token!",
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

    category = user_data["chain"]
    user_data[category] = text

    return CHOOSING

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")

    return TYPING_REPLY

async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]

    if category == "Private Key":
        # Encrypt the private key before storing
        encrypted_private_key = encrypt_private_key(text)
        user_data[category] = encrypted_private_key
        
    # Perform validation check for token quantity
    if category == "BNB":
        if not text.isdigit():
            await update.message.reply_text("Please enter a valid numerical value for token quantity.")
            return TYPING_REPLY

    # Perform validation check for token address
    if category == "TokenOutAddress":
        if not isinstance(text, str):
            await update.message.reply_text("Please enter a valid token address as a string.")
            return TYPING_REPLY

    # Store valid user input
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]
    print(user_data)
    if user_data == {}:
        print(user_data)
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
                MessageHandler(
                    filters.Regex("^(TokenOutAddress|BNB|Private Key)$"), regular_choice
                ),
                MessageHandler(filters.Regex("^Something else...$"), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
