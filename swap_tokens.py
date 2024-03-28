# import time
# import winsound
from os import system

from bs4 import BeautifulSoup as bsp
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from web3 import Web3 
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# from buy import buyTokens
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
# WBNB_Address = web3.toChecksumAddress(config.WBNB_ADDRESS)
pancakeRouterAddress = web3.to_checksum_address(config.PANCAKE_ROUTER_ADDRESS)
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
    # global TokenToSellAddress
    global TradingTokenDecimal
    print("user_data in swap_tokens",user_data)
    chain = user_data.get("Chain")
    bnb = user_data.get("BNB")
    token_to_buy_address = user_data.get("TokenToBuyAddress")
    wallet_address = user_data.get("Wallet Address")
    private_key = user_data.get("Private Key")
    # if "Add Comments" in user_data:
    #     comments = user_data.get("Add Comments")
    # print("comments on swap function",comments)    


    # Getting ABI
    buy_token_abi = tokenAbi(token_to_buy_address, driver)
    pancakeAbi = tokenAbi(pancakeRouterAddress, driver)
    print("selltoken_abi ----------------->",buy_token_abi)
    # Enter your wallet Public Address
    BNB_balance = web3.eth.get_balance(wallet_address)
    BNB_balance = web3.from_wei(BNB_balance, "ether")

    # # Create a contract for both PancakeRoute and Token to Sell
    contractPancake = web3.eth.contract(address = pancakeRouterAddress, abi = pancakeAbi)
    contractSellToken = web3.eth.contract(token_to_buy_address, abi = buy_token_abi)

    # if TradingTokenDecimal is None:
    #     TradingTokenDecimal = contractSellToken.functions.decimals().call()
    #     TradingTokenDecimal = getTokenDecimal(TradingTokenDecimal)

    # # Get current available amount of tokens from the wallet
    # NoOftokens = contractSellToken.functions.balanceOf(walletAddress).call()
    # NoOftokens = web3.fromWei(NoOftokens, TradingTokenDecimal)
    # symbol = contractSellToken.functions.symbol().call()
    # # params = {
    # #     "symbol": symbol,
    # #     ""
    # # }