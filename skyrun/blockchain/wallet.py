"""
Wallet implementation for blockchain interactions.
"""

from typing import Dict, Optional
from web3 import Web3
from eth_account import Account
import json
import os

class Wallet:
    """Wallet class for managing blockchain accounts and transactions."""
    
    def __init__(self, web3: Web3, private_key: Optional[str] = None):
        """Initialize the wallet.
        
        Args:
            web3: Web3 instance
            private_key: Optional private key for the wallet
        """
        self.web3 = web3
        self.account = None
        if private_key:
            self.account = Account.from_key(private_key)
        else:
            self.account = Account.create()
            
    @classmethod
    def from_keyfile(cls, web3: Web3, keyfile_path: str, password: str) -> 'Wallet':
        """Create a wallet from a keyfile.
        
        Args:
            web3: Web3 instance
            keyfile_path: Path to the keyfile
            password: Password to decrypt the keyfile
            
        Returns:
            Wallet instance
        """
        with open(keyfile_path) as f:
            keyfile_json = json.load(f)
            
        private_key = Account.decrypt(keyfile_json, password)
        return cls(web3, private_key.hex())
        
    def save_keyfile(self, keyfile_path: str, password: str) -> None:
        """Save the wallet's private key to a keyfile.
        
        Args:
            keyfile_path: Path to save the keyfile
            password: Password to encrypt the keyfile
        """
        keyfile_json = Account.encrypt(self.account.key, password)
        
        os.makedirs(os.path.dirname(keyfile_path), exist_ok=True)
        with open(keyfile_path, 'w') as f:
            json.dump(keyfile_json, f)
            
    def get_balance(self) -> int:
        """Get the wallet's balance in wei.
        
        Returns:
            Balance in wei
        """
        return self.web3.eth.get_balance(self.account.address)
        
    def send_transaction(self, to_address: str, amount: int, data: Optional[bytes] = None) -> str:
        """Send a transaction.
        
        Args:
            to_address: Recipient address
            amount: Amount to send in wei
            data: Optional transaction data
            
        Returns:
            Transaction hash
        """
        tx = {
            'from': self.account.address,
            'to': to_address,
            'value': amount,
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
            'gas': 2000000,
            'gasPrice': self.web3.eth.gas_price,
            'data': data or b''
        }
        
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return self.web3.to_hex(tx_hash)
        
    def sign_message(self, message: str) -> Dict:
        """Sign a message.
        
        Args:
            message: Message to sign
            
        Returns:
            Dictionary containing signature components
        """
        message_hash = self.web3.keccak(text=message)
        signature = self.web3.eth.account.sign_message(
            message_hash,
            private_key=self.account.key
        )
        
        return {
            'r': signature.r,
            's': signature.s,
            'v': signature.v
        }
        
    def verify_signature(self, message: str, signature: Dict) -> bool:
        """Verify a message signature.
        
        Args:
            message: Original message
            signature: Signature components
            
        Returns:
            True if signature is valid, False otherwise
        """
        message_hash = self.web3.keccak(text=message)
        recovered_address = self.web3.eth.account.recover_message(
            message_hash,
            signature=signature
        )
        
        return recovered_address.lower() == self.account.address.lower() 