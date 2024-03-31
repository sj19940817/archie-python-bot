from os import system

from bs4 import BeautifulSoup as bsp

from web3 import Web3 

from decimal_data import getTokenDecimal
from buy import buyTokens
import config as config
from abi import ERC20_ABI, Pancake_Router_ABI

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

pancake_router_address = web3.to_checksum_address(config.PANCAKE_ROUTER_ADDRESS)
TradingTokenDecimal = None

def initializeTrade(user_data):

    # global driver
    global TradingTokenDecimal

    chain = user_data.get("Chain")
    # print("user_data in swap_tokens",user_data)
    BNB_amount = user_data.get("BNB")
    token_to_buy_address = user_data.get("TokenToBuyAddress")
    WBNB_Address = web3.to_checksum_address(config.WBNB_ADDRESS)
    # token_to_buy_address = web3.toChecksumAddress(token_to_buy_address)
    wallet_address = user_data.get("Wallet Address")
    private_key = user_data.get("Private Key")

    # Getting ABI
    token_abi = ERC20_ABI
    pancake_router_abi = Pancake_Router_ABI
    # Enter your wallet Public Address
    BNB_balance = web3.eth.get_balance(wallet_address)
    BNB_balance = web3.from_wei(BNB_balance, "ether")

    # Create a contract for both PancakeRoute and Token to Sell
    contract_pancake = web3.eth.contract(address = pancake_router_address, abi = pancake_router_abi)
    contract_buy_token = web3.eth.contract(token_to_buy_address, abi = token_abi)
    contract_wbnb = web3.eth.contract(address = WBNB_Address, abi = token_abi)

    print("here is swap tokens =========================>", BNB_balance)
    if TradingTokenDecimal is None:
        TradingTokenDecimal = contract_buy_token.functions.decimals().call()
        TradingTokenDecimal = getTokenDecimal(TradingTokenDecimal)

    # Get current avaliable amount of tokens from the wallet
    NoOfTokens = contract_buy_token.functions.balanceOf(wallet_address).call()
    NoOfTokens = web3.from_wei(NoOfTokens, TradingTokenDecimal)
    # print("NoOfTokens ====================>", NoOfTokens)
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
        "contract_wbnb": contract_wbnb,
        "trading_token_decimal": TradingTokenDecimal,
        "BNB_amount": BNB_amount,
        "private_key": private_key
    } 
    
    return buyTokens(params)
    # return BNB_balance, symbol, NoOfTokens, params