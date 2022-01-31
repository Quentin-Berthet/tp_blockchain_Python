import sys
from time import time

sys.path.extend(['.'])
from transaction import Transaction
from merkle_tree import MerkleTree
from utils import sha256


class BlockHeader:
    def __init__(self, index, previous_block_digest, mining_date, nonce, digest):
        """
        Crée l'en-tête d'un bloc
        :param index: Index du bloc
        :param previous_block_digest: Empreinte numérique du bloc précédent
        :param mining_date: Date et heure du minage du bloc
        :param nonce: Nombre arbitraite qui sera utilisé pour respecter la difficulté de la blockchain
        :param digest: Empreinte numérique du bloc
        """
        self.index = index
        self.previous_block_digest = previous_block_digest
        self.mining_date = mining_date
        self.nonce = nonce
        self.digest = digest


class Block:
    root: MerkleTree
    header: BlockHeader
    transactions: [Transaction]
    difficulty: int

    def __init__(self, index: int, previous_block, difficulty):
        """
        Crée un nouveau bloc
        :param index: Index du bloc dans la blockchain
        :param previous_block: Référence vers le bloc précédent
        :param difficulty: Difficulté de la blockchain
        """
        previous_digest = previous_block.header.digest if index > 0 else ""
        self.header = BlockHeader(index, previous_digest, None, 0, "")
        self.transactions = list()
        self.merkle_tree = None
        self.difficulty = difficulty

    def compute_digest(self):
        """
        Calcul l'empreinte numérique du bloc tout en respectant la difficulté de la blockchain
        """
        zero_to_match = "0" * self.difficulty
        while True:
            to_hash = str(self.header.index) + self.header.previous_block_digest + self.merkle_tree.root.content + str(
                self.header.nonce)
            digest = sha256(to_hash)
            if digest[:self.difficulty] == zero_to_match:
                self.header.digest = digest
                self.header.mining_date = time()
                break
            self.header.nonce += 1

    def add_transaction(self, transaction: Transaction):
        """
        Ajoute une transaction dans le bloc et met à jour l'arbre de Merkle
        :param transaction: Référence vers une transaction
        """
        self.transactions.append(transaction)
        self.merkle_tree = MerkleTree([transaction.id for transaction in self.transactions])
