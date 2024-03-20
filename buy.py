from web3 import Web3
import config
from abis import tier1
from abis import tier2
from abis import tier3
from abis import tier4
from abis import tier5
from abis import tier6

tiers = [tier1, tier2, tier3, tier4, tier5, tier6]
rpc_url = "https://arb1.arbitrum.io/rpc"
web3 = Web3(Web3.HTTPProvider(rpc_url))
account = web3.eth.account.from_key(config.private_key)

def buy(tier):
    obj_tier = tiers[tier -1]
    merkleProof = []
    code = 'node'
    payment_amount = web3.to_wei(obj_tier.price * 2 if tier == 1 else 1, 'ether')
    contrato = web3.eth.contract(address=obj_tier.contract_address, abi=obj_tier.abi)

    while True:
        try:
            nonce = web3.eth.get_transaction_count(account.address)
            transaction = contrato.functions.whitelistedPurchaseWithCode(payment_amount, merkleProof, payment_amount, code).build_transaction({
                "from": account.address,
                "nonce": nonce,
            })

            signed = web3.eth.account.sign_transaction(transaction, account.key)
            tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
            web3.eth.wait_for_transaction_receipt(tx_hash)
            tx = web3.eth.get_transaction(tx_hash)
            print(f'transaction: {tx}')
        except Exception as e:
            if e != 'execution reverted: sale has not begun':
                print(e)
                break

buy(tier=1)
