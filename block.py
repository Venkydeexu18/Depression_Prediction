import os
import ipfshttpclient
from web3 import Web3, HTTPProvider
from eth_account import Account
from solcx import compile_standard

# Ethereum configuration
eth_rpc_url = "https://mainnet.infura.io/v3/f8fa5bacc9f94817a35ac44590ec73d4"
private_key = "f8fa5bacc9f94817a35ac44590ec73d4"
contract_address = "CONTRACT_ADDRESS"

# Connect to Ethereum
w3 = Web3(HTTPProvider(eth_rpc_url))
account = Account.privateKeyToAccount(private_key)

# IPFS configuration
ipfs_client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001/http")

# Solidity contract source code
contract_source = """
pragma solidity ^0.8.0;

contract EVault {
    struct Document {
        string ipfsHash;
        uint256 timestamp;
    }
    
    mapping(string => Document) documents;

    function uploadDocument(string memory docHash) public {
        documents[docHash] = Document(docHash, block.timestamp);
    }

    function getDocument(string memory docHash) public view returns (string memory, uint256) {
        return (documents[docHash].ipfsHash, documents[docHash].timestamp);
    }
}
"""

# Compile the contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"evault.sol": {"content": contract_source}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
    }
)

contract_abi = compiled_sol["contracts"]["evault.sol"]["EVault"]["abi"]
contract_bytecode = compiled_sol["contracts"]["evault.sol"]["EVault"]["evm"]["bytecode"]["object"]

# Deploy the contract


def deploy_contract():
    Contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    tx_hash = Contract.constructor().transact(
        {"from": account.address, "gas": 2000000})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt["contractAddress"]

# Upload a document to IPFS and store its hash on the blockchain


def upload_document(file_path):
    with open(file_path, "rb") as file:
        ipfs_response = ipfs_client.add(file)
        ipfs_hash = ipfs_response["Hash"]

    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    tx_hash = contract.functions.uploadDocument(ipfs_hash).transact(
        {"from": account.address, "gas": 2000000}
    )
    w3.eth.waitForTransactionReceipt(tx_hash)
    print("Document uploaded successfully!")

# Get document details from the blockchain and download from IPFS


def download_document(doc_hash):
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    ipfs_hash, timestamp = contract.functions.getDocument(doc_hash).call()

    if ipfs_hash:
        ipfs_response = ipfs_client.get(ipfs_hash)
        file_path = os.path.join("downloads", doc_hash)
        with open(file_path, "wb") as file:
            for chunk in ipfs_response:
                file.write(chunk)
        print(f"Document downloaded to {file_path}")
    else:
        print("Document not found.")


# Main execution
if __name__ == "__main__":
    # Deploy the contract (only needed for the first time)
    # deployed_contract_address = deploy_contract()

    # Example usage
    document_path = "path_to_your_document.pdf"
    upload_document(document_path)

    document_hash = "Qm..."
    download_document(document_hash)
