# import time
from os import system

from bs4 import BeautifulSoup as bsp
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options

from web3 import Web3 
# from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.chrome import ChromeDriverManager

from decimal_data import getTokenDecimal
from buy import buyTokens
# from sell import sellTokens
import config as config
# from ThreadingWithReturn import ThreadWithResult
from abi import ERC20_ABI, Pancake_Router_ABI

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
pancake_router_address = web3.to_checksum_address(config.PANCAKE_ROUTER_ADDRESS)
# walletAddress = config.walletAddress
TradingTokenDecimal = None

# to clear command line
# clear = lambda: system("cls") 
# options = Options()
# options.headless = True

#options.add_argument
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options = options)
# driver = webdriver.Chrome()

# def showTx(url):
#     webdriver.Chrome(executable_apth = ChromeDriverManager().install()).get(url)

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
    # if "Add Comments" in user_data:
    #     comments = user_data.get("Add Comments")
    # print("comments on swap function",comments)    

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
    
    buyTokens(params)
    # return BNB_balance, symbol, NoOfTokens, params

# from web3 import Web3
# from web3.middleware import geth_poa_middleware
# import abi as ERC20ABI
# import config as config
# from decimal_data import getTokenDecimal
# # from ethers import Wallet

# # Initialize Web3 with BSC RPC endpoint
# bsc_rpc_endpoint = "https://bsc-dataseed.binance.org/"
# web3 = Web3(Web3.HTTPProvider(bsc_rpc_endpoint))
# web3.middleware_onion.inject(geth_poa_middleware, layer = 0)

# def initializeTrade(data):
#     token_to_buy_address = data.get("token_to_buy_address")
#     bnb_amount = data.get("BNB")
#     wallet_address = data.get("wallet_address")
#     private_key = data.get("Private Key")

#     pancake_router_address = config.PANCAKE_ROUTER_ADDRESS
#     wbnb_address = config.WBNB_ADDRESS
#     gas_limit = 200000
#     gas_price = 1000000000
#     amount_in_wei = web3.to_wei(bnb_amount, "ether")
#     pancake_router_abi = [
#         "function getAmountsOut(uint amountIn, address[] memory path) public view returns (uint[] memory amounts)",
#         "function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts)",
#         "function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline) external payable returns (uint[] memory amounts)",
#         "function swapExactETHForTokensSupportingFeeOnTransferTokens(uint amountOutMin,address[] calldata path,address to, uint deadline) external payable",
#         "function swapExactTokensForETH(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external returns (uint[] memory amounts)",
#         "function swapExactTokensForETHSupportingFeeOnTransferTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external",
#         "function swapExactTokensForTokensSupportingFeeOnTransferTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external",
#     ]

#     # if TradingTokenDecimal is None:
#     # TradingTokenDecimal = contract_buy_token.functions.decimals().call()
#     # TradingTokenDecimal = getTokenDecimal(TradingTokenDecimal)

#     # Connect to wallet
#     # ethWallet = Wallet.from_key(private_key)
#     # account = ethWallet.address
#     #Instantiate PancakeSwap Router contract
#     pancake_router_contract = web3.eth.contract(address = pancake_router_address, abi = pancake_router_abi)

#     print("here swap tokens =====================>")
#     # Approve PancakeSwap Router to spend WBNB
#     wbnb_contract = web3.eth.contract(address = wbnb_address, abi = ERC20ABI)
#     wbnb_allowance = wbnb_contract.functions.allowance(wallet_address, pancake_router_address).call()
#     if wbnb_allowance < amount_in_wei:
#         approve_txn = wbnb_contract.functions.approve(pancake_router_address, web3.to_wei(100000, "ether")).buildTransaction({
#             "chainId": 56,   # BSC Mainnet Chain ID
#             "gas": 100000,
#             "gasPrice": web3.to_wei(gas_price, "gwei"),
#             "nonce": web3.eth.get_transaction_count(wallet_address)
#         })
#         signed_approve_txn = web3.eth.account.sign_transaction(approve_txn, private_key = private_key)
#         web3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)

#     txn = pancake_router_contract.functions.swapExactETHForTokens(
#         0,
#         [wbnb_address, token_to_buy_address],
#         wallet_address,
#         int(web3.eth.getBlock("latest")["timestamp"]) + 300, # Deasline (5 min)
#     ).buildTransaction({
#         "chainId": 56,
#         "value": amount_in_wei,
#         "gas": gas_limit,
#         "gasPrice" : web3.to_wei(gas_price, "gwei"),
#         "nonce" : web3.eth.get_transaction_count(wallet_address)
#     })
#     signed_txn = web3.eth.acount.signTransaction(txn, private_key)
#     tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
#     print("here is swap_tokens====================>")
#     return tx_hash.hex()