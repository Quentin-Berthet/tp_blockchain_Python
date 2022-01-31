import hashlib
import matplotlib.pyplot as plt
import numpy as np
import time

__authors__ = ["Baptiste Coudray", "Quentin Berthet"]
__date__ = "31.05.2020"
__course__ = "Sécurité réseau"
__description__ = "Blockchain"


class Block:
    @property
    def content(self) -> str:
        return self._content

    @property
    def nonce(self) -> int:
        return self._nonce

    def increment_nonce(self):
        self._nonce += 1

    @property
    def hash(self) -> str:
        to_hash = self.content + str(self.nonce)
        return hashlib.sha256(to_hash.encode("utf-8")).hexdigest()

    def __init__(self, content: str):
        self._content = content
        self._nonce = 0


def compute_word(difficulty, word, printing=True):
    zero_to_match = "0" * difficulty
    b = Block(word)
    while b.hash[:difficulty] != zero_to_match:
        b.increment_nonce()
    if printing:
        print(f"{word} : {b.hash} (Nonce = {b.nonce})")


if __name__ == '__main__':
    difficulty = 4

    # Effectuer un hash qui respecte une difficulté
    compute_word(difficulty, "bonjour")
    compute_word(difficulty, "blockchain")
    compute_word(difficulty, "sécurité")

    # Calcul du temps selon la difficulté
    max_difficulty = 7
    times_avg = np.array([])
    for difficulty in range(1, max_difficulty):
        times = np.array([])
        for _ in range(3):
            start = time.time()
            compute_word(difficulty, "blockchain", False)
            stop = time.time()
            times = np.append(times, stop - start)
        times_avg = np.append(times_avg, times.sum() / 3)
    fig, ax = plt.subplots()
    ax.plot(range(1, max_difficulty), times_avg)
    ax.set(xlabel='Difficulté', ylabel='Temps [s]', title='Calcul du temps selon la difficulté')
    ax.grid()
    plt.show()
