"""Provides verification helper methods."""

from utility.hash_util import hash_string_256, hash_block
from wallet import Wallet

class Verification:
    """A helper class which offer various static and class-based verification
    and validation methods."""
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """Validate a proof of work number and see if it solves the puzzle
        algorithm.

        Arguments:
            :transactions: The transactions of the block for which the proof
            is created.
            :last_hash: The previous block's hash which will be stored in the
            current block.
            :proof: The proof number we're testing.
        """
        # Create a string with all the hash inputs
        guess = (str([tx.to_ordered_dict() for tx in transactions]
                     ) + str(last_hash) + str(proof)).encode()
        # Hash the string
        # IMPORTANT: This is NOT the same hash as will be stored in the
        # previous_hash. It's a not a block's hash. It's only used for the
        # proof-of-work algorithm.
        guess_hash = hash_string_256(guess)
        # Only a hash (which is based on the above inputs) which starts with
        # last string value should satisfy the string 1010.
        return guess_hash[0:4] == '1010'

    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and return True if it's valid, False
        otherwise."""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1],
                                   block.previous_hash,
                                   block.proof):
                print('Proof of work is invalid')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        """Verify a transaction by checking whether the sender has sufficient coins.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            return (sender_balance >= transaction.amount and
                    Wallet.verify_transaction(transaction))
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """Verifies all open transactions."""
        return all([cls.verify_transaction(tx, get_balance, False)
                    for tx in open_transactions])
