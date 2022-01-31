import sys

sys.path.extend(['.'])
from block import Block
from transaction import Transaction

__authors__ = ["Baptiste Coudray", "Quentin Berthet"]
__date__ = "31.05.2020"
__course__ = "Sécurité réseau"
__description__ = "Blockchain"


class Blockchain:
    nb_blocks_to_verify: int
    max_transactions_per_block: int
    difficulty: int
    blocks: [Block]

    def __init__(self, difficulty, max_transactions_per_block, nb_blocks_to_verify):
        """
        Crée une nouvelle Blockchain
        :param difficulty: Le nombre de 0 que doit commencer l'empreinte numérique d'un bloc
        :param max_transactions_per_block: Le nombre de transactions par bloc
        :param nb_blocks_to_verify: Le nombre de blocs à vérifier avant de créer un nouveau bloc
        """
        self.difficulty = difficulty
        self.max_transactions_per_block = max_transactions_per_block
        self.nb_blocks_to_verify = nb_blocks_to_verify
        self.blocks = [Block(0, None, self.difficulty)]

    def verify(self, nb_blocks):
        """
        Vérifie si la Blockchain est toujours valide en comparant l'empreinte numérique d'un bloc précédent
        avec le bloc qui le succède
        :param nb_blocks: Le nombre de blocs à vérifier
        :return: True si la blockchain est toujours valide, sinon False
        """
        blocks = self.blocks[:nb_blocks]
        current_digest = blocks.pop(0).header.digest
        for block in blocks:
            if block.header.previous_block_digest != current_digest:
                return False
            current_digest = block.header.digest
        return True

    def add_transaction(self, seller: str, buyer: str, amount: float):
        """
        Ajoute une transaction dans le bloc courant ou dans un nouveau bloc si le nombre de transaction du bloc
        actuel a atteint le maximum. Dans ce cas, une vérification de la chaîne est effectuée avant
        de créer un nouveau bloc.
        :param seller: Nom du vendeur
        :param buyer: Nom de l'acheteur
        :param amount: Montant de la transaction
        """
        transaction = Transaction(seller, buyer, amount)
        if len(self.blocks[-1].transactions) < self.max_transactions_per_block:
            self.blocks[-1].add_transaction(transaction)
        else:
            self.blocks[-1].compute_digest()
            if not self.verify(self.nb_blocks_to_verify):
                raise Exception("L'intégrité de la blockchain est compromise.")
            new_block = Block(len(self.blocks), self.blocks[-1], self.difficulty)
            new_block.add_transaction(transaction)
            self.blocks.append(new_block)


if __name__ == '__main__':
    blockchain = Blockchain(difficulty=3, max_transactions_per_block=5, nb_blocks_to_verify=2)
    while True:
        try:
            print("Ajouter une transaction :")
            seller = input("Vendeur :")
            buyer = input("Acheteur :")
            amount = float(input("Amount:"))
            blockchain.add_transaction(seller, buyer, amount)
        except Exception as e:
            print(f"\x1b[1;31m{e}\x1b[0m")
            exit(1)
