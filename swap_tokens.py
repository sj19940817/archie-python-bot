# import time
from os import system

from bs4 import BeautifulSoup as bsp
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from web3 import Web3 
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from buy import buyTokens
# from sell import sellTokens
import config as config
# from ThreadingWithReturn import ThreadWithResult
from abi import tokenAbi
from decimal_data import getTokenDecimal

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
# if web3.isConnected(): 
#     print("Connected to BSC")

# User Input Address for Token
# if bool(config.TRADE_TOKEN_ADDRESS):
#     address = config.TRADE_TOKEN_ADDRESS
# else: 
#     address = input("Enter token address:")

# Important Addresses
# TokenToSellAddress = web3.toChecksumAddress(address)
# WBNB_Address = web3.to_checksum_address(config.WBNB_ADDRESS)
pancake_router_address = web3.to_checksum_address(config.PANCAKE_ROUTER_ADDRESS)
# walletAddress = config.walletAddress
TradingTokenDecimal = None

# to clear command line
# clear = lambda: system("cls") 
# options = Options()
# options.headless = True

#options.add_argument
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options = options)
driver = webdriver.Chrome()

# def showTx(url):
#     webdriver.Chrome(executable_apth = ChromeDriverManager().install()).get(url)

def initializeTrade(user_data):

    global driver
    global TradingTokenDecimal
    print("user_data in swap_tokens",user_data)
    chain = user_data.get("Chain")
    WBNB_Address = user_data.get("BNB")
    token_to_buy_address = user_data.get("TokenToBuyAddress")
    # WBNB_Address = web3.toChecksumAddress(WBNB_Address)
    # token_to_buy_address = web3.toChecksumAddress(token_to_buy_address)
    wallet_address = user_data.get("Wallet Address")
    private_key = user_data.get("Private Key")
    # if "Add Comments" in user_data:
    #     comments = user_data.get("Add Comments")
    # print("comments on swap function",comments)    

    # Getting ABI
    buy_token_abi = tokenAbi(token_to_buy_address, driver)
    pancake_abi = tokenAbi(pancake_router_address, driver)

    # Enter your wallet Public Address
    BNB_balance = web3.eth.get_balance(wallet_address)
    BNB_balance = web3.from_wei(BNB_balance, "ether")

    # Create a contract for both PancakeRoute and Token to Sell
    contract_pancake = web3.eth.contract(address = pancake_router_address, abi = pancake_abi)
    contract_buy_token = web3.eth.contract(token_to_buy_address, abi = buy_token_abi)

    if TradingTokenDecimal is None:
        TradingTokenDecimal = contract_buy_token.functions.decimals().call()
        TradingTokenDecimal = getTokenDecimal(TradingTokenDecimal)

    # Get current avaliable amount of tokens from the wallet
    NoOfTokens = contract_buy_token.functions.balanceOf(wallet_address).call()
    NoOfTokens = web3.from_wei(NoOfTokens, TradingTokenDecimal)
    print("NoOfTokens ====================>", NoOfTokens)
    symbol = contract_buy_token.functions.symbol().call()
    
    params = {
        "symbol": symbol,
        "web3": web3,
        "wallet_address": wallet_address,
        "contract_buy_token": contract_buy_token,
        "contract_pancake": contract_pancake,
        "pancake_router_address": pancake_router_address,
        "token_to_buy_address": token_to_buy_address,
        "WBNB_Address": WBNB_Address,
        "trading_token_decimal": TradingTokenDecimal 
    } 
    
    buyTokens(params)
    # return BNB_balance, symbol, NoOfTokens, params