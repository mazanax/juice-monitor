import os
from dotenv import load_dotenv
from web3 import Web3
import requests

load_dotenv()

RPC_URL = os.getenv("BLAST_RPC", "https://rpc.blast.io")
TOKEN_ADDRESS = Web3.to_checksum_address(os.getenv("TOKEN_ADDRESS", "0x4300000000000000000000000000000000000003"))
WALLET_ADDRESS = Web3.to_checksum_address(os.getenv("WALLET_ADDRESS", "0x4A1d9220e11a47d8Ab22Ccd82DA616740CF0920a"))
THRESHOLD = int(os.getenv("THRESHOLD", int(25300*1e18)))
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

ERC20_ABI = [{
    "constant": True,
    "inputs": [{"name": "_owner", "type": "address"}],
    "name": "balanceOf",
    "outputs": [{"name": "balance", "type": "uint256"}],
    "type": "function"
}]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=ERC20_ABI)

def get_token_balance():
    return contract.functions.balanceOf(WALLET_ADDRESS).call()

def send_telegram_alert(balance):
    message = f"⚠️ Token balance exceeded: {balance} (threshold: {THRESHOLD}), diff: {((THRESHOLD - balance) / 1e18):.2f}"
    if TG_BOT_TOKEN and TG_CHAT_ID:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TG_CHAT_ID,
            "text": message
        }
        requests.post(url, data=data)

def main():
    try:
        balance = get_token_balance()
        print(f"Token balance: {(balance / 1e18):.2f}")

        if balance > THRESHOLD:
            send_telegram_alert(balance)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
