from flask import Flask, render_template, request, jsonify
import json
import config
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Initialize Flask app
app = Flask(__name__)

# Connect to Sepolia via Infura
web3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

# Inject the POA middleware (Proof of Authority) using middleware_onion
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Contract setup
contract_address = Web3.to_checksum_address(config.CONTRACT_ADDRESS)
contract_abi = json.loads(config.CONTRACT_ABI)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    return render_template('index.html')  # This will load the HTML page

@app.route('/issue_certificate', methods=['POST'])
def issue_certificate():
    certificate_id = request.form['certificate_id']
    student_name = request.form['student_name']
    course_name = request.form['course_name']
    issue_date = request.form['issue_date']
    
    # Call the smart contract function to issue a certificate (same as before)
    account = config.ACCOUNT_ADDRESS
    private_key = config.PRIVATE_KEY
    txn = contract.functions.issueCertificate(int(certificate_id), student_name, course_name, issue_date).build_transaction({
        'from': account,
        'gas': 2000000,
        'gasPrice': web3.to_wei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account),
        'chainId': 11155111
    })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    return jsonify({'transaction_hash': txn_hash.hex()})

@app.route('/get_certificate', methods=['GET'])
def get_certificate():
    certificate_id = request.args.get('certificate_id')
    certificate = contract.functions.getCertificate(int(certificate_id)).call()
    
    return jsonify({
        'student': certificate[0],
        'course': certificate[1],
        'issued_on': certificate[2]
    })



if __name__ == '__main__':
    app.run(debug=True)
