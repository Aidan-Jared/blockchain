import hashlib as hasher
import datetime as date
import numpy as np
from flask import Flask
from flask import request
import json
import requests
node = Flask(__name__)

chain = [create_genisis_block()]
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block
    
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))
        return sha.hexdigest()

def create_genisis_block():
    return Block(0, date.datetime.now(), 'Genesis Block', "0")

def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = np.random.random()
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_nodes_transactions.append(new_txion)
        print("New transaction")
        print("FROM: {}".format(new_txion['from']))
        print("TO: {}".format(new_txion['to']))
        print("AMOUNT: {}\n".format(new_txion['amount']))
        return "Transaction submission successful\n"

node.run

this_nodes_transactions = []

def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor

@node.route('/mine', mehtods = ['GET'])
def mine():
    last_block = chain[len(chain) - 1]
    last_proof = last_block.data['proof-of-work']
    proof = proof_of_work(last_proof)
    this_nodes_transactions.append({"from":'network', 'to':miner_address, 'amount':1})
    new_block_data = {"proof-of-work":proof, 'transactions':list(this_nodes_transactions)}
    new_block_index = last_block.index + 1
    new_block_timestamp = date.datetime.now()
    last_block_hash = last_block.hash

    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )

    chain.append(mined_block)
    return json.dumps(
        {
            'index': new_block_index,
            'timestamp': str(new_block_timestamp),
            'data':new_block_data,
            'hash':last_block_hash
        }
    ) + '/n'

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = chain
    for block in chain_to_send:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        block = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data":block_data,
            "hash":block_hash
        }
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send    

def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        block = requests.get(node_url + '/blocks').content
        block = json.load(block)
        other_chains.append(block)
    return other_chains

def consensus():
    other_chains = find_new_chains()
    longest_chain = chain
    for i in other_chains:
        if len(longest_chain) < len(i):
            longest_chain = chain
    chain = longest_chain

if __name__ == "__main__":
    previous_block = chain[0]

    for i in range(20):
        block_to_add = next_block(previous_block)
        chain.append(block_to_add)
        previous_block = block_to_add
        print("Block #{} has been added to the blockchain!".format(block_to_add.index))
        print("Hash: {}\n".format(block_to_add.hash))