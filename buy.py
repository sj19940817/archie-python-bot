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
   
   pancakeSwap_txn = contract_pancake.functions.swapExactETHForTokens(
      0,
      [WBNB_Address, token_to_buy_address],
      wallet_address,
      (int(time.time() + 10000))).build_transaction({
         "from": wallet_address,
         "value": BNB_amount_in_wei,
         "gas": 160000,
         "gasPrice": web3.to_wei('5', 'gwei'),
         "nonce": web3.eth.get_transaction_count(wallet_address)
      })
   
   try:
      signed_txn = web3.eth.account.sign_transaction(pancakeSwap_txn, private_key)
      tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
      result = [web3.to_hex(tx_token), f"Bought {web3.from_wei(BNB_amount, 'ether')} BNB of {symbol}"]
      print("return in buy =================>",result)
      return result
   except ValueError as e:
      print(e)
      if e.args[0].get("message") in "intrinsic gas too low":
         # result = "Failed", f"ERROR: {e.args[0].get('message')}"
         return "Failed: Try again later"
         print(e.args[0].get("message"))
      else:
         # result = "Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"
         return "Failed: Try again later"
      return result