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
    CallbackContext
)

from config import Token

"""Enable logging"""
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

"""set higher logging level for httpx to avoid all GET and POST requests being logged"""
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

disabled_buttons = set()

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

buy_reply_keyboard = [
    [{"text": "Chain", "request_contact": False},
     {"text": "TokenToBuyAddress", "request_contact": False}],
    [{"text": "BNB", "request_contact": False }, 
     {"text": "Add comments", "request": True}], 
    [{"text": "OK", "request_contact": False},
     {"text": "Exit", "request": False}],
]

sell_reply_keyboard = [
    [{"text": "Chain", "request_contact": False},
     {"text": "TokenToSellAddress", "request_contact": False}],
    [{"text": "AmountOfToken", "request_contact": False }, 
     {"text": "Add comments", "request": True}],
    [{"text": "OK", "request_contact": False},
     {"text": "Exit", "request": False}],
]

buy_markup = ReplyKeyboardMarkup(buy_reply_keyboard, one_time_keyboard=True)
sell_markup = ReplyKeyboardMarkup(sell_reply_keyboard, one_time_keyboard=True)

reply_chains = [
    "BSC",
    "Avax",
    "Solana"
]

async def buy_tokens(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # implement logic to buy tokens on PancakeSwap
    print("Buy tokens using pancakeswap------------------", update, context)
    pass

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [
        f"{emoji.emojize(':link: Chain')} : {value}" if key == 'Chain' else
        f"{emoji.emojize(':money_bag: BNB')} : {value}" if key == "BNB" else
        f"{emoji.emojize(':receipt: TokenToBuyAddress')}: {value}" if key == "TokenToBuyAddress" else
        f"{emoji.emojize(':key: Private Key')} : {value}" if key == 'Private Key' else
        # f"Comments: {value}" if key == "Add comments" else
        f"{key} : {value}"
        for key, value in user_data.items() 
    ]
    return "\n".join(facts).join(["\n", "\n"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for the data."""
    
    buy_sell_keyboard = [
       ["Buy",
        "Sell"]
    ]
    buy_sell_markup = ReplyKeyboardMarkup(buy_sell_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Hello! I am  ** ArchieBot **. Please input the data to buy and sell tokens.",
        reply_markup=buy_sell_markup,
    )

    return CHOOSING

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """buy token with BNB"""
    await update.message.reply_text(
        "Input the token address you want to buy and the amount of BNB.",
        reply_markup=buy_markup,
    )
    
    return CHOOSING 

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """sell token function"""
    print("sell----------------")
    await update.message.reply_text(
        "Input address and the amount of token you want to sell.",
        reply_markup=sell_markup,
    )
    
    return CHOOSING 

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Help command"""
    await update.message.reply_text(
        "1. To start the transaction, please input command /start \n2. To cancel the transcation, please input the command /quit"
    )

async def select_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for the Chain that they want"""
    print(context)
    text = update.message.text
    context.user_data["choice"] = text

    # Definition of  the chains
    reply_chains = [
        ["BSC"],
        ["Avax"],
        ["Solana"],
    ]
    chain_type = ReplyKeyboardMarkup(reply_chains, one_time_keyboard=True)

    await update.message.reply_text(
        f"Please choose the {emoji.emojize(':link:')} chain you want",
        reply_markup=chain_type
    )

    return TYPING_REPLY

async def select_chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for the Chain that they want"""
    text = update.message.text
    category = context.user_data["chain"]
    context.user_data[category] = text

    return CHOOSING

async def update_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Buttons updated.", reply_markup=new_markup)

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the data that the user input"""
    text = update.message.text
    
    context.user_data["choice"] = text
    print("regular_choice----------------", context)
    if text == "Private Key":
        disabled_buttons.add(text) # Add "Private Key" to disabled buttons set
        await update.message.reply_text(f"Please input your {text} {emoji.emojize(':key:')}.")
    if text == "Chain":
        await update.message.reply_text(f"Please select the  {text} {emoji.emojize(':link:')} you want.")
    if text == "BNB":
        await update.message.reply_text(f"Please input the amount of  {text} {emoji.emojize(':money_bag:')} .")
    if text == "TokenToBuyAddress":
        await update.message.reply_text(f"Please intput the {text} {emoji.emojize(':envelope:')}")
    if text == "TokenToSellAddress":
        await update.message.reply_text(f"Please intput the {text} {emoji.emojize(':envelope:')}")

    return TYPING_REPLY

async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Do you want to add comments to this transaction? \nThen please input the comments!!! '
    )
    return TYPING_REPLY

def is_valid_token_address(token_address: str)-> bool:
    """function to validate the TokenToBuyAddress"""
    if len(token_address) != 42 or not token_address.startswith("0x"):
        return False
    
    """Check if the address consists of valid hexadecimal characters"""
    try:
        int(token_address, 16)
        return True
    except ValueError:
        return False

def is_valid_private_key(private_key):
    """Function to validate the private key"""
    print(private_key)
    return bool(re.match(r"^[A-Fa-f0-9]{64}$", private_key))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation and clear user data."""
    user_data = context.user_data
    user_data.clear()
    await update.message.reply_text(
        "Transaction canceled. You can start a new transaction by typing /start.",
        reply_markup=ReplyKeyboardRemove(),        
    )
    return ConversationHandler.END

async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Update the received_information function to include private key validation"""    
    user_data = context.user_data
    text = update.message.text
    category = user_data.get("choice")  # Use get method to avoid KeyError

    if category is None:
        category = f"{emoji.emojize(':pencil: Comments')}"

    if category == "Chain":
        if text not in reply_chains:
            await update.message.reply_text("Please input validate *Chain*!")
            return TYPING_REPLY
            
    if category == "BNB":
        if not text.isdigit():
            await update.message.reply_text("Please enter the amount of BNB!")
            return TYPING_REPLY
        
    if category == "TokenToBuyAddress":
        if not is_valid_token_address(text):
            await update.message.reply_text("Please enter a valid token address.")
            return TYPING_REPLY

        # If the input is valid, add it to user_data
        user_data[category] = text
        
    if category == "TokenToSellAddress":
        if not is_valid_token_address(text):
            await update.message.reply_text("Please enter a valid token address.")
            return TYPING_REPLY
        # If the input is valid, add it to user_data
        user_data[category] = text

    if category == "Private Key":
        print("private key", category)
        if not is_valid_private_key(text):
    
            await update.message.reply_text("Please enter a valid private key.")
            return TYPING_REPLY

        """Mask the private key before displaying it"""
        masked_private_key = text[:3] + "....."
        user_data[category] = masked_private_key

        """Delete the private key message"""
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        
    else:
        user_data[category] = text

    if "choice" in user_data:
        del user_data["choice"]

    print("user data in received info",user_data)
    # Check if both "TokenToSellAddress" and "AmountOfToken" are present with non-empty values
    if user_data.get("TokenToSellAddress") and user_data.get("AmountOfToken"):
        print("here we are")
        await update.message.reply_text(
            "Neat! Just so you know, this is what you already told me:"
            f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
            " add comments",
            reply_markup=sell_markup,
        )
    else:
        await update.message.reply_text(
            "Neat! Just so you know, this is what you already told me:"
            f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
            " add comments",
            reply_markup=buy_markup,
        )

    return CHOOSING

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """confirm user's transaction"""
    print("context user data",context.user_data)

    await update.message.reply_text("Please input your wallet private key!")
    return TYPING_CHOICE
async def private_key_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user to input the private key."""
    user_data = context.user_data
    private_key = update.message.text
    selected_chain = user_data.get("Chain")

    if selected_chain != "Solana":
        if not is_valid_private_key(private_key):
            if "private_key_attempts" not in user_data:
                user_data["private_key_attempts"] = 1
            else:
                user_data["private_key_attempts"] += 1

            if user_data["private_key_attempts"] >= 3:
                # Limiting the number of attempts to 3
                await update.message.reply_text("You've exceeded the maximum number of attempts. Please try again later.")
                return ConversationHandler.END  # End the conversation
            else:
                await update.message.reply_text("Please input a valid private key.")
                return TYPING_CHOICE

        # If the private key is valid, delete the message
        user_data["Private Key"] = private_key
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        
    # Provide feedback that the private key has been received
    await update.message.reply_text("Private key received. Proceeding with the transaction.")
    await buy_tokens(update, context)
    # Continue with the transaction process or other actions

    return CHOOSING  # Move to the next step in the conversation

    
    # call the function that request web3 with {context.user_data}

# async def result_show(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """This will show the transaction result from the web3"""

async def OK(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
    user_data = context.user_data

    if "Chain" in user_data and "TokenToBuyAddress" in user_data and "BNB" in user_data:
        """check if all required inputs have been provided"""
        reply_confirmation = [["Confirm", "Cancel"]]
        confirmation_markup = ReplyKeyboardMarkup(reply_confirmation, one_time_keyboard=True)

        await update.message.reply_text(
            f"Your input data: \n{facts_to_str(user_data)} \n Please confirm your transaction:",
            reply_markup = confirmation_markup
        )
        return CHOOSING
    else: 
        await update.message.reply_text(f"Please provide all required input data before confirming.. \n Your input data: {facts_to_str(user_data)} ", reply_markup = buy_markup)
        return CHOOSING


async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Confirm the transaction exit function"""
    print("exit function")
    user_data = context.user_data
    exit_confirmation = [["Yes", "No"]]
    exit_markup = ReplyKeyboardMarkup(exit_confirmation, one_time_keyboard=True)

    await update.message.reply_text(
        f"Do you really want to cancel the transaction?",
        reply_markup=exit_markup
    )
    return CHOOSING
    
async def confirm_exit_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Exit the transaction"""

    user_data = context.user_data
    user_data.clear()
    await update.message.reply_text(
        "Transaction cancelled. You can start a new transaction by typing /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def confirm_exit_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Return to the transaction"""

    user_data = context.user_data

    print("confirm_exit_no", update )
    user_data.clear()
    await update.message.reply_text(
        "Welcome back",
        reply_markup=markup
    )
    
    return CHOOSING

async def quit_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Redirect the user when he or she input the command /quit..."""
    user_data = context.user_data
    user_data.clear()
    await update.message.reply_text(
        "Transaction cancelled. You can start a new transaction by typing /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def delete_message(update: Update, context: CallbackContext) -> None:
    #Get the chat ID and message ID
    chat_id = update.message.chat_id
    message_id = update.message.message_id

    #Delete the message
    context.bot.delet_message(chat_id = chat_id, message_id = message_id)

def main() -> None:
    """Run the bot."""

    """Create the Application and pass it your bot's token."""
    application = Application.builder().token(Token).build()

    """Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY"""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("help", help)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^Buy"), buy
                ),
                MessageHandler(
                    filters.Regex("^Sell"), sell
                ),
                MessageHandler(
                    filters.Regex("^Chain$"), select_choice
                ),
                MessageHandler(filters.Regex("^BSC"), select_chain),
                MessageHandler(filters.Regex("^Avax"), select_chain),
                MessageHandler(filters.Regex("^Solana"), select_chain),
                MessageHandler(
                    filters.Regex("^(TokenToBuyAddress|BNB|Private Key|TokenToSellAddress|AmountOfToken)$"), regular_choice
                ),
                MessageHandler(filters.Regex("^Add comments$"), custom_choice),
                MessageHandler(filters.Regex("^Exit$"), exit),
                MessageHandler(filters.Regex("^Confirm$"), confirm),
                MessageHandler(filters.Regex("^Yes$"), confirm_exit_yes),
                MessageHandler(filters.Regex("^No"), confirm_exit_no)
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^OK$")), private_key_input
                ),
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
            CommandHandler("quit", quit_order),
            CommandHandler("help", help)
            ],
    )

    application.add_handler(conv_handler)

    """Run the bot until the user press Ctrl-C"""
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()