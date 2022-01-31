import sys

sys.path.extend(['.'])
from utils import sha256


class Node:
    def __init__(self, content, left, right):
        self.content = content
        self.left = left
        self.right = right


class MerkleTree:
    def __init__(self, digests: [str]):
        """
        Crée un arbre de Merkle
        :param digests: Liste des empreintes numériques (sha256) des valeurs à mettre dans l'arbre
        """
        leafs = [Node(digest, None, None) for digest in digests]
        self.root = self._build_tree(leafs)

    def _build_tree(self, nodes: [Node]):
        # Il reste plus qu'un noeud, c'est donc la racine de l'arbre
        if len(nodes) == 1:
            return nodes[0]
        even_nodes = nodes
        # Si le nombre de noeuds n'est pas pair, on duplique le dernier noeud pour qu'il le soit
        if len(nodes) % 2 != 0:
            even_nodes.append(nodes[-1])
        nodes = []
        for i in range(0, len(even_nodes), 2):
            # A partir de deux noeuds, on crée un noeud parent qui contient l'empreinte numérique
            # du noeud à gauche + noeud à droite
            digest_left = even_nodes[i].content
            digest_right = even_nodes[i + 1].content
            digest = sha256(digest_left + digest_right)
            nodes.append(Node(digest, even_nodes[i], even_nodes[i + 1]))
        return self._build_tree(nodes)


if __name__ == '__main__':
    mk = MerkleTree([sha256(value) for value in ["bonjour", "blockchain", "sécurité"]])
    print(f'MerkleTree(["bonjour", "blockchain", "sécurité"]) = {mk.root.content}')
    mk2 = MerkleTree([sha256(value) for value in ["1234", "5678", "abcd", "efgh"]])
    print(f'MerkleTree(["1234", "5678", "abcd", "efgh"]) = {mk2.root.content}')
