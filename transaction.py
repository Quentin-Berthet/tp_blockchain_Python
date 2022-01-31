from utils import sha256


class Transaction:
    id: str
    amount: float
    buyer: str
    seller: str

    def __init__(self, seller: str, buyer: str, amount: float):
        """
        Crée une nouvelle transaction
        :param seller: Le nom du vendeur
        :param buyer: Le nom de l'acheteur
        :param amount: Le montant de la transaction
        """
        self.seller = seller
        self.buyer = buyer
        self.amount = amount
        self.id = sha256(self.seller + self.buyer + str(self.amount))
