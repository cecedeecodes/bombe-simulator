import string
from copy import deepcopy

class Rotor:
    def __init__(self, wiring):
        self.base_wiring = wiring
        self.position = 0
        self.letters = list(string.ascii_uppercase)
        self._update_wiring()

    def _update_wiring(self):
        shifted_letters = self.letters[self.position:] + self.letters[:self.position]
        self.wiring = dict(zip(self.letters, shifted_letters))
        self.reverse_wiring = {v: k for k, v in self.wiring.items()}

    def step(self):
        self.position = (self.position + 1) % 26
        self._update_wiring()

    def reset(self):
        self.position = 0
        self._update_wiring()

    def encrypt(self, char):
        return self.wiring.get(char, char)

    def decrypt(self, char):
        return self.reverse_wiring.get(char, char)

# === Test with matching stepping ===
crib = "HELLO"

# Use a Caesar-style rotor (A→B, B→C … Z→A)
caesar_wiring = dict(zip(string.ascii_uppercase, string.ascii_uppercase[1:] + "A"))
rotor = Rotor(caesar_wiring)

# Encrypt
encrypted = ""
for letter in crib:
    encrypted += rotor.encrypt(letter)
    rotor.step()

print(f"Encrypted: {encrypted}")

# Decrypt
rotor.reset()
decrypted = ""
for letter in encrypted:
    decrypted += rotor.decrypt(letter)
    rotor.step()

print(f"Decrypted: {decrypted}")
