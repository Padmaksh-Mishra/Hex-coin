import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from urllib.parse import urlparse
from uuid import uuid4


# Making the BlockChain for HEXcoin

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(nonce= 1,previous_Hash = '0') #since we use sha256 it only accepts encoding in strings 
                                                            #and since it is a genesis block ie the first one we have 
                                                            #to set the previous hash as 0 <standard method>
        self.nodes = set()
    
    def create_block(self,nonce,previous_Hash):
        block = {"index" : len(self.chain)+1,
                 "timestamp" : str(datetime.datetime.now()),
                 "nonce" : nonce,
                 "transactions" : self.transactions,
                 "previous_Hash" : previous_Hash}
        self.chain.append(block)
        self.transactions = []
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        accepted_nonce = 1
        check_proof = False
        
        while(check_proof==False):
            hash_operation = hashlib.sha256(str(accepted_nonce**2 - previous_proof**2).encode()).hexdigest()
            
            if(hash_operation[:4]=="0000"):
                check_proof = True
            else:
                accepted_nonce+=1
        return accepted_nonce
                
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1;
        while(block_index<len(chain)):
            current_block = chain[block_index]
            
            if(current_block["previous_Hash"] != self.hash(previous_block)):
                return False
            
            accepted_nonce = current_block["nonce"]
            previous_proof = previous_block["nonce"]
            hash_operation = hashlib.sha256(str(accepted_nonce**2 - previous_proof**2).encode()).hexdigest()
            
            if(hash_operation[:4]!="0000"):
                return False
            
            block_index+=1
            previous_block = current_block
            
            return True
         
    def add_transactions(self,sender,reciever,amount):
        self.transactions.append({"sender" : sender,
                                  "reciever" : reciever,
                                  "amount" : amount })
        previous_block_index = self.get_previous_block()["index"]
        return previous_block_index+1
    
    def add_node(self,address):
        parsed_address = urlparse(address)
        self.nodes.add(parsed_address.netloc)
        
    def replace_chain(self):        #More OPTIMIZATION possible
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            responce = requests.get(f"http://{node}/get_chain")
            if responce.status_code == 200:
                length = responce.json()["length"]
                chain = responce.json()["chain"]
                if(length>max_length and self.is_chain_valid(chain)):
                    max_length = length
                    longest_chain = chain
                
        if(longest_chain):
            self.chain = longest_chain
            return True
        return False
        
        
            
# Making a flask based web APP

app = Flask(__name__) 

# creating the address for the node @ port 5001

node_address = str(uuid4()).replace('-','')

# Instancinating an object of the BlockChain class

blockchain = Blockchain()

# Mining a block
@app.route("/mine_block", methods = ["GET"])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_POW = previous_block['nonce']
    proof_of_work = blockchain.proof_of_work(previous_POW)
    blockchain.add_transactions(node_address,'PM',1)
    block = blockchain.create_block(proof_of_work,blockchain.hash(previous_block))
    
    responce = {"message": "Congratulations, you have successfully mined a block!!!",
                "index": block['index'] ,
                "timestamp" : block['timestamp'],
                "nonce" : block['nonce'],
                "transactions" : block['transactions'],
                "previous_Hash" : block['previous_Hash']}
    
    
    return jsonify(responce) , 200 # it is a static responce indicating OK

# Getting the full blockchain
@app.route("/get_chain", methods = ["GET"])

def get_chain():
    responce = {"chain": blockchain.chain,
                "length": len(blockchain.chain)}
    return jsonify(responce) , 200

# checking the blockchain for its validity
@app.route("/is_valid",methods = ["GET"])

def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    responce = {"message" : 0}
    if (is_valid):
        responce["message"] = "Everything is PERFECT"
    else:
        responce['message'] = "There is a problem"
    return jsonify(responce) , 200

# a post request to add a transcition to the new block which is going to be mined in future

@app.route("/add_transcation", methods = ["POST"])

def add_transcation():
    json = request.get_json()
    keys = ["sender","reciever","amount"]
    if not all(key in json for key in keys ):
        return "Some keys are missing" , 400
    index = blockchain.add_transactions(sender=json["sender"],reciever=json["reciever"], amount=json["amount"])
    responce = {"message" : f"The trancation will be added on block {index}"}
    return jsonify(responce) , 201   # 201 is created



# decentralizing the chain
 
# connecting the nodes

@app.route("/connect_nodes",methods = ["POST"])

def connect_nodes():
    json = request.get_json()
    nodes = json.get("nodes")
    if nodes is None:
        return "No nodes present to be connected" , 400
    else:
        for node_address in nodes:
            blockchain.add_node(node_address)
    responce = {"message": "All the nodes of the network are now connected : ",
                "nodes": list(blockchain.nodes)}    # wo blockchain class wala nodes ka set
    
    return jsonify(responce), 201

# enshuring that each node has the same longest version of the blockchain
@app.route("/replace_chain",methods = ["GET"])

def replace_chain():
    chain_replaced = blockchain.replace_chain()
    responce = {"message" : 0,
                "newchain": blockchain.chain}
    if (chain_replaced):
        responce["message"] = "The chain was replaced according to consensus protocol"
    else:
        responce['message'] = "The chain was already the longest one"
    return jsonify(responce) , 200
# Running the flask application

app.run(host = '0.0.0.0',port=(5001))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    