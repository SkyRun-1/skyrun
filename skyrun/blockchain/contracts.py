"""
Smart contract for content ownership and rights management.
"""

from typing import Dict, List, Optional
from web3 import Web3
from web3.contract import Contract
from eth_account import Account

class ContentRegistry:
    """Smart contract for managing content ownership and rights."""
    
    def __init__(self, web3: Web3, contract_address: str, contract_abi: List[Dict]):
        """Initialize the content registry contract.
        
        Args:
            web3: Web3 instance
            contract_address: Address of the deployed contract
            contract_abi: Contract ABI
        """
        self.web3 = web3
        self.contract: Contract = web3.eth.contract(
            address=contract_address,
            abi=contract_abi
        )
        
    def register_content(self, content_hash: str, owner: str, metadata: Dict) -> str:
        """Register new content on the blockchain.
        
        Args:
            content_hash: Hash of the content
            owner: Address of the content owner
            metadata: Additional metadata about the content
            
        Returns:
            Transaction hash
        """
        tx = self.contract.functions.registerContent(
            content_hash,
            owner,
            metadata
        ).build_transaction({
            'from': owner,
            'nonce': self.web3.eth.get_transaction_count(owner),
            'gas': 2000000,
            'gasPrice': self.web3.eth.gas_price
        })
        
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=None)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return self.web3.to_hex(tx_hash)
        
    def get_content_owner(self, content_hash: str) -> str:
        """Get the owner of registered content.
        
        Args:
            content_hash: Hash of the content
            
        Returns:
            Address of the content owner
        """
        return self.contract.functions.getContentOwner(content_hash).call()
        
    def get_content_metadata(self, content_hash: str) -> Dict:
        """Get metadata for registered content.
        
        Args:
            content_hash: Hash of the content
            
        Returns:
            Content metadata dictionary
        """
        return self.contract.functions.getContentMetadata(content_hash).call()
        
    def transfer_ownership(self, content_hash: str, from_address: str, to_address: str) -> str:
        """Transfer content ownership to another address.
        
        Args:
            content_hash: Hash of the content
            from_address: Current owner's address
            to_address: New owner's address
            
        Returns:
            Transaction hash
        """
        tx = self.contract.functions.transferOwnership(
            content_hash,
            to_address
        ).build_transaction({
            'from': from_address,
            'nonce': self.web3.eth.get_transaction_count(from_address),
            'gas': 2000000,
            'gasPrice': self.web3.eth.gas_price
        })
        
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=None)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return self.web3.to_hex(tx_hash)
        
    def verify_ownership(self, content_hash: str, address: str) -> bool:
        """Verify if an address owns specific content.
        
        Args:
            content_hash: Hash of the content
            address: Address to verify
            
        Returns:
            True if the address owns the content, False otherwise
        """
        return self.contract.functions.verifyOwnership(content_hash, address).call() 