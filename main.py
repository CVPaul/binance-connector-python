from binance.futures import CoinM

# ED25519 Keys
api_key = "v7hcRjC7W6YeYOiY06NcN8KjmsY8GNm56K9KGuMBcVCgsf4EX3FyCz0PYYdWPlvQ"
private_key = "../Private_key.txt"
private_key_pass = ""

with open(private_key, 'rb') as f:
    private_key = f.read()

client = CoinM(
    api_key=api_key,
    private_key=private_key,
    private_key_pass=private_key_pass,
    # base_url="https://dapi.binance.com"
)

# Get server timestamp
print(client.time())