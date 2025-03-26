"""
Transaction implementation for blockchain interactions.
"""

from typing import Dict, Optional
from web3 import Web3
from eth_account import Account
import json
from datetime import datetime

class Transaction:
    """Transaction class for managing blockchain transactions."""
    
    def __init__(self, web3: Web3, tx_hash: Optional[str] = None):
        """Initialize the transaction.
        
        Args:
            web3: Web3 instance
            tx_hash: Optional transaction hash
        """
        self.web3 = web3
        self.tx_hash = tx_hash
        self.tx_receipt = None
        if tx_hash:
            self.tx_receipt = self.web3.eth.get_transaction_receipt(tx_hash)
            
    @classmethod
    def from_receipt(cls, web3: Web3, receipt: Dict) -> 'Transaction':
        """Create a transaction from a receipt.
        
        Args:
            web3: Web3 instance
            receipt: Transaction receipt
            
        Returns:
            Transaction instance
        """
        tx = cls(web3, receipt['transactionHash'].hex())
        tx.tx_receipt = receipt
        return tx
        
    def get_status(self) -> str:
        """Get the transaction status.
        
        Returns:
            Transaction status
        """
        if not self.tx_receipt:
            return 'pending'
            
        if self.tx_receipt['status'] == 1:
            return 'success'
        else:
            return 'failed'
            
    def get_block_number(self) -> Optional[int]:
        """Get the block number where the transaction was mined.
        
        Returns:
            Block number or None if not mined
        """
        if not self.tx_receipt:
            return None
        return self.tx_receipt['blockNumber']
        
    def get_gas_used(self) -> Optional[int]:
        """Get the amount of gas used by the transaction.
        
        Returns:
            Gas used or None if not mined
        """
        if not self.tx_receipt:
            return None
        return self.tx_receipt['gasUsed']
        
    def get_gas_price(self) -> Optional[int]:
        """Get the gas price used for the transaction.
        
        Returns:
            Gas price or None if not mined
        """
        if not self.tx_receipt:
            return None
        return self.tx_receipt['effectiveGasPrice']
        
    def get_logs(self) -> Optional[list]:
        """Get the transaction logs.
        
        Returns:
            List of logs or None if not mined
        """
        if not self.tx_receipt:
            return None
        return self.tx_receipt['logs']
        
    def to_dict(self) -> Dict:
        """Convert the transaction to a dictionary.
        
        Returns:
            Dictionary representation of the transaction
        """
        if not self.tx_receipt:
            return {
                'hash': self.tx_hash,
                'status': 'pending',
                'timestamp': datetime.now().isoformat()
            }
            
        return {
            'hash': self.tx_hash,
            'status': self.get_status(),
            'block_number': self.get_block_number(),
            'gas_used': self.get_gas_used(),
            'gas_price': self.get_gas_price(),
            'logs': self.get_logs(),
            'timestamp': datetime.now().isoformat()
        }
        
    def to_json(self) -> str:
        """Convert the transaction to a JSON string.
        
        Returns:
            JSON string representation of the transaction
        """
        return json.dumps(self.to_dict(), indent=2)
        
    def wait_for_receipt(self, timeout: int = 300) -> Dict:
        """Wait for the transaction receipt.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            Transaction receipt
        """
        if not self.tx_receipt:
            self.tx_receipt = self.web3.eth.wait_for_transaction_receipt(
                self.tx_hash,
                timeout=timeout
            )
        return self.tx_receipt 