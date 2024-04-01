from web3 import Web3 

from decimal_data import getTokenDecimal
from buy import buyTokens
from sell import sellTokens
import config as config
from abi import ERC20_ABI, Pancake_Router_ABI

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

pancake_router_address = web3.to_checksum_address(config.PANCAKE_ROUTER_ADDRESS)
TradingTokenDecimal = None

def initialize_buy(user_data):

    # global driver
    global TradingTokenDecimal
    chain = user_data.get("Chain")
    BNB_amount = user_data.get("BNB")
    token_to_buy_address = user_data.get("TokenToBuyAddress")
    WBNB_Address = web3.to_checksum_address(config.WBNB_ADDRESS)
    # token_to_buy_address = web3.toChecksumAddress(token_to_buy_address)
    wallet_address = user_data.get("Wallet Address")
    private_key = user_data.get("Private Key")

    if chain == "BSC":            
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

        if TradingTokenDecimal is None:
            TradingTokenDecimal = contract_buy_token.functions.decimals().call()
            TradingTokenDecimal = getTokenDecimal(TradingTokenDecimal)

        # Get current avaliable amount of tokens from the wallet
        NoOfTokens = contract_buy_token.functions.balanceOf(wallet_address).call()
        NoOfTokens = web3.from_wei(NoOfTokens, TradingTokenDecimal)
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
    else:
        return "The chain you selected is not supported yet."

def initialize_sell(user_data):

    # global driver
    global TradingTokenDecimal
    chain = user_data.get("Chain")
    BNB_amount = user_data.get("BNB")
    token_to_buy_address = web3.to_checksum_address(user_data.get("TokenToSellAddress"))
    WBNB_Address = web3.to_checksum_address(config.WBNB_ADDRESS)
    # token_to_buy_address = web3.toChecksumAddress(token_to_buy_address)
    wallet_address = user_data.get("Wallet Address")
    private_key = user_data.get("Private Key")
    sell_token_amount = user_data.get("AmountOfToken")
    # sell_tokne_amount = web3.to_wei(sell_token_amount, TradingTokenDecimal)

    if chain == "BSC":
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

        if TradingTokenDecimal is None:
            TradingTokenDecimal = contract_buy_token.functions.decimals().call()
            TradingTokenDecimal = getTokenDecimal(TradingTokenDecimal)

        # Get current avaliable amount of tokens from the wallet
        NoOfTokens = contract_buy_token.functions.balanceOf(wallet_address).call()
        NoOfTokens = web3.from_wei(NoOfTokens, TradingTokenDecimal)
        symbol = contract_buy_token.functions.symbol().call()
        
        params = {
            "symbol": symbol,
            "web3": web3,
            "wallet_address": wallet_address,
            "contract_sell_token": contract_buy_token,
            "contract_pancake": contract_pancake,
            "pancake_router_address": pancake_router_address,
            "token_to_sell_address": token_to_buy_address,
            "WBNB_Address": WBNB_Address,
            "contract_wbnb": contract_wbnb,
            "trading_token_decimal": TradingTokenDecimal,
            "BNB_amount": BNB_amount,
            "private_key": private_key,
            "sell_token_amount": sell_token_amount
        } 
        
        return sellTokens(params)
        # return BNB_balance, symbol, NoOfTokens, params`
    else:
        return "You selected chain is not supported yet"