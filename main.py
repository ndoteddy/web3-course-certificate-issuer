from web3 import Web3
import json
import config  # Importing the config.py file

# Connect to Sepolia via Infura
web3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

# Check if connected to the network
if web3.is_connected():
    print("Connected to Sepolia Test Network")

# Use contract details from config.py
contract_address = Web3.to_checksum_address(config.CONTRACT_ADDRESS) # Fetching the contract address from config
contract_abi = json.loads(config.CONTRACT_ABI)  # Fetching the contract ABI from config

# Set up the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function to issue a certificate
def issue_certificate(certificate_id, student_name, course_name, issue_date):
    account = config.ACCOUNT_ADDRESS  # Using the account address from config
    private_key = config.PRIVATE_KEY  # Using the private key from config
    transaction = contract.functions.issueCertificate(int(certificate_id), student_name, course_name, issue_date).build_transaction({
        'from': account,
        'gas': 2000000,
        'gasPrice': web3.to_wei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account),
        'chainId': 11155111
    })

   # Correct method to sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the signed transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Certificate issued! Transaction Hash: {txn_hash.hex()}")

# Function to fetch a certificate
def get_certificate(certificate_id):
    certificate = contract.functions.getCertificate(certificate_id).call()
    print(f"Certificate Details: \nStudent: {certificate[0]} \nCourse: {certificate[1]} \nIssued On: {certificate[2]}")

# Example of issuing a certificate
issue_certificate(2, "Nando Teddy", "Lets learn web3", "2025-04-25")

# Example of fetching a certificate
get_certificate(2)
