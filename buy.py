import config as config
import time

def buyTokens(params):

   symbol = params.get("symbol")
   web3 = params.get("web3")
   wallet_address = params.get("wallet_address")
   contract_pancake = params.get("contract_pancake")
   token_to_buy_address = params.get("token_to_buy_address")
   WBNB_Address = params.get("WBNB_Address")
   contract_wbnb = params.get("contract_wbnb")
   BNB_amount = params.get("BNB_amount")
   private_key = params.get("private_key")
   BNB_amount_in_wei = web3.to_wei(BNB_amount, 'ether')
   pancake_router_address = config.PANCAKE_ROUTER_ADDRESS

   gas_limit = 200000
   gas_price = 1000000000


   #  contract_wbnb = web3.eth.contract(address = WBNB_Address, abi = ERC20ABI)
   wbnb_allowance = contract_wbnb.functions.allowance(wallet_address, pancake_router_address).call()
   print("wbnb allowance =====>", wbnb_allowance)
   if wbnb_allowance < BNB_amount_in_wei:
      approve_txn = contract_wbnb.functions.approve(pancake_router_address, web3.to_wei(100000, "ether")).build_transaction({
         "chainId": 56,   # BSC Mainnet Chain ID
         "gas": 100000,
         "gasPrice": web3.to_wei(gas_price, "gwei"),
         "nonce": web3.eth.get_transaction_count(wallet_address)
      })
      signed_approve_txn = web3.eth.account.sign_transaction(approve_txn, private_key = private_key)
      web3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)
   else:
      print("exceeded amount!!!!")
   print("here is buytoken==================>", params)
   pancakeSwap_txn = contract_pancake.functions.swapExactETHForTokens(
      0,
      [WBNB_Address, token_to_buy_address],
      wallet_address,
      (int(time.time() + 10000))).build_transaction({
         "from": wallet_address,
         "value": BNB_amount,
         "gas": 160000,
         "gasPrice": web3.to_wei('5', 'gwei'),
         "nonce": web3.eth.get_transaction_count(wallet_address)
      })
   
   signed_txn = web3.eth.account.sign_transaction(pancakeSwap_txn, private_key)
   try:
      tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
      result = [web3.toHex(tx_token), f"Bought {web3.fromWei(BNB_amount, 'ether')} BNB of {symbol}"]
      return result
   except ValueError as e:
      if e.args[0].get("message") in "intrinsic gas too low":
         result = ["Failed", f"ERROR: {e.args[0].get('message')}"]
      else:
         result = ["Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"]
      return result


# from web3 import Web3
# from web3.middleware import geth_poa_middleware
# from wev3.exceptions import TransactionNotFound

# #Initialize Web3 with BSC RPC endpoint
# bsc_rpc_ednpoint = "https://bsc-dataseed.binance.org/"
# web3 = Web3(Web3.HTTPProvider(bsc_rpc_ednpoint))
# web3.middleware_onion.inject(geth_poa_middleware, layer = 0)

# #Define contract addresses and ABIs for PancakeSwap Router and ERC20 token
# pancake_router_address = config.PANCAKE_ROUTER_ADDRESS
# pancake_router_abi = []
# erc20_abi = []

#Define wallet address and private key

