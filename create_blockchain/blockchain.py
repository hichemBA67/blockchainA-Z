# Module 1 - Create a blockchain

# To be installed:
    # Flask==0.12.2: pip install Flask==0.12.2
    # Postman

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify
# Part 1 - Building a Blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        # Genesis block -> previous_hash = '0'
        self.create_block(proof = 1, previous_hash = '0')
        
    # Create block function
    def create_block(self, proof, previous_hash):
        # Create new block
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        
        # Append created block to chain
        self.chain.append(block)
        # Return new block for later display
        return block
    
    # Get previous/current block
    def get_previous_block(self):
        return self.chain[-1]
    
    # POW (Proof-of-work) function
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # Problem has to be non-symmetrical (! new_proof + previous_proof) -> every two iterations same proof
            # SHA256 expects String & endcoded (b'...')
            # To get hexadecimal -> .hexdigest()
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # Check if hash_operation has 4 leading zeros
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1 
                
        return new_proof
    
    # Hash function return cryptographic hash of block
    def hash(self, block):
        # Encode block for SHA256 to accept it
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # Check 1
            # Check if previous hash of current block is equal to hash of previous block
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # Check 2
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            # Check if current proof and previous proof have 4 leading zeros after SHA256
            if hash_operation[:4] != '0000':
                return False
            # Update previous block and current block index
            previous_block = block
            block_index += 1
            
        return True
            
# Part 2 - Mining our Blockchain
# Creating web application
app = Flask(__name__)

# Creating blockchain
blockchain = Blockchain()

# Create new route
@app.route('/mine_block', methods=['GET'])
# Mining new block
def mine_block():
    # Get previous block
    previous_block = blockchain.get_previous_block()
    # Get previous proof
    previous_proof = previous_block['proof']
    # Get proof of future new block
    proof = blockchain.proof_of_work(previous_proof)
    # Get previous hash
    previous_hash = blockchain.hash(previous_block)
    # Create new block
    block = blockchain.create_block(proof, previous_hash)
    # Create response for display
    response = {'message': 'Congratulation, You just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    
    return jsonify(response), 200

# Get full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Validate Chain
@app.route('/is_valid', methods=['GET'])
def is_valid():
    chain = blockchain.chain
    is_valid = blockchain.is_chain_valid(chain)
    if is_valid:
        response = {'message': 'The blockchain is valid'}
    else:
        response = {'message': 'The blockchain is not valid'}
    
    return jsonify(response), 200
    
# Running the app
app.run(host = '0.0.0.0', port = 5001)