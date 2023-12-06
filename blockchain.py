import hashlib
import time
import random
import string

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, sender=None, receiver=None):
        # Constructor for the Block class
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.sender = sender
        self.receiver = receiver

class Blockchain:
    def __init__(self):
        # Constructor for the Blockchain class
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Creates the initial block in the blockchain (Genesis block)
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0))
        self.chain.append(genesis_block)

    def calculate_hash(self, index):
        # Calculates the hash of a block based on its index
        if 0 <= index < len(self.chain):
            block = self.chain[index]
            block_info = str(block.index) + str(block.previous_hash) + str(block.timestamp) + str(block.data)
            return hashlib.sha256(block_info.encode()).hexdigest()
        return None

    def add_block(self, sender, receiver, amount):
        # Adds a new block to the blockchain with a transaction
        index = len(self.chain)
        previous_hash = self.calculate_hash(index - 1)
        timestamp = time.time()
        data = f"{sender} sends {receiver} {amount} WesleyCoin"
        hash = self.calculate_hash(index)
        new_block = Block(index, previous_hash, timestamp, data, hash, sender, receiver)
        self.chain.append(new_block)

    def display_chain(self, block_index=None):
        # Displays information about a specific block or the latest block in the blockchain
        if block_index is None:
            block_index = len(self.chain) - 1

        block = self.chain[block_index]
        print(f"Block #{block.index}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}")
        print()

class Wallet:
    def __init__(self, userName, walletBalance=50):
        # Constructor for the Wallet class
        self.userName = userName
        self.walletID = "0x" + ''.join(random.choices(string.ascii_letters + string.digits, k=62))
        self.walletBalance = walletBalance

def main():
    user_blockchain = Blockchain()
    existing_wallets = set()

    print("Enter a command ('user_creation', 'commit_transaction', 'check_balance', 'display_chain', 'exit_0'):")

    while True:
        command = input()

        if command == 'exit_0':
            break

        elif command == 'user_creation':
            # Creates a new user with a wallet and adds it to the set of existing wallets
            user_name = input("Enter your username: ")
            initial_balance = float(input("Enter your initial balance of WesleyCoin: "))
            user_wallet = Wallet(user_name, initial_balance)
            existing_wallets.add(user_wallet)
            print(f"Wallet created for {user_wallet.userName}. Initial balance: {user_wallet.walletBalance} WesleyCoin.")

        elif command == 'commit_transaction':
            # Initiates a new transaction by selecting a sender, receiver, and amount
            print("Make a Transaction:")
            
            # Display available senders
            senders = list(existing_wallets)
            for i, sender in enumerate(senders, start=1):
                print(f"{i}. {sender.userName}")

            sender_index = input("Enter the number of the sender: ")
            
            try:
                sender_wallet = senders.pop(int(sender_index) - 1)
            except (ValueError, IndexError):
                print("Invalid sender selection. Please try again.")
                continue

            # Display available receivers
            receivers = [wallet for wallet in existing_wallets if wallet != sender_wallet]
            for i, receiver in enumerate(receivers, start=1):
                print(f"{i}. {receiver.userName}")

            receiver_index = input("Enter the number of the receiver: ")
            
            try:
                receiver_wallet = receivers.pop(int(receiver_index) - 1)
            except (ValueError, IndexError):
                print("Invalid receiver selection. Please try again.")
                continue

            transaction_amount = float(input("Enter the amount of WesleyCoin to send: "))
            
            if sender_wallet.walletBalance < transaction_amount:
                print("Insufficient funds. Please try a smaller amount.")
                continue

            # Update wallet balances and add a new block to the blockchain
            sender_wallet.walletBalance -= transaction_amount
            receiver_wallet.walletBalance += transaction_amount
            user_blockchain.add_block(sender_wallet.userName, receiver_wallet.userName, transaction_amount)
            print("Transaction committed. Current block of the blockchain:")
            user_blockchain.display_chain()

        elif command == 'check_balance':
            # Checks the balance of a selected wallet
            print("Choose a wallet to check balance:")

            # Display available wallets
            for i, wallet in enumerate(existing_wallets, start=1):
                print(f"{i}. {wallet.userName}")

            wallet_index = input("Enter the number of the wallet: ")

            try:
                selected_wallet = existing_wallets.pop(int(wallet_index) - 1)
                print(f"Balance of {selected_wallet.userName}'s wallet: {selected_wallet.walletBalance} WesleyCoin.")
                existing_wallets.add(selected_wallet)  # Add the wallet back to the set
            except (ValueError, IndexError):
                print("Invalid wallet selection. Please try again.")
                continue

        elif command == 'display_chain':
            # Displays the current state of the blockchain
            print("Current block of the blockchain:")
            user_blockchain.display_chain()

        print("\nEnter a command ('user_creation', 'commit_transaction', 'check_balance', 'display_chain', 'exit_0'): ")

if __name__ == "__main__":
    main()
