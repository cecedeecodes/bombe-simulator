import string
from copy import deepcopy

class Rotor:
    def __init__(self, wiring, notch):
        self.base_wiring = wiring
        self.notch = notch  # when position == notch, next rotor steps
        self.position = 0
        self.letters = list(string.ascii_uppercase)
        self._update_wiring()

    def _update_wiring(self):
        shifted = self.letters[self.position:] + self.letters[:self.position]
        self.wiring = dict(zip(self.letters, shifted))
        self.reverse_wiring = {v: k for k, v in self.wiring.items()}

    def step(self):
        self.position = (self.position + 1) % 26
        self._update_wiring()

    def at_notch(self):
        return self.position == self.notch

    def reset(self):
        self.position = 0
        self._update_wiring()

    def encrypt(self, char):
        return self.wiring.get(char, char)

    def decrypt(self, char):
        return self.reverse_wiring.get(char, char)

def reflect(char):
    reflection = dict(zip(string.ascii_uppercase, reversed(string.ascii_uppercase)))
    return reflection.get(char, char)

# === Rotor Setup ===
caesar = dict(zip(string.ascii_uppercase, string.ascii_uppercase[1:] + "A"))
rotor1 = Rotor(deepcopy(caesar), notch=5)
rotor2 = Rotor(deepcopy(caesar), notch=5)
rotor3 = Rotor(deepcopy(caesar), notch=5)
rotors = [rotor1, rotor2, rotor3]

def step_rotors(rotors):
    # Rightmost rotor always steps
    rotors[0].step()
    # Middle rotor steps if right rotor is at notch
    if rotors[0].at_notch():
        rotors[1].step()
    # Left rotor steps if middle rotor is at notch
    if rotors[1].at_notch():
        rotors[2].step()

def reset_rotors(rotors):
    for rotor in rotors:
        rotor.reset()

def encrypt_letter(letter, rotors):
    # Forward pass
    for r in rotors:
        letter = r.encrypt(letter)
    # Reflector
    letter = reflect(letter)
    # Backward pass
    for r in reversed(rotors):
        letter = r.decrypt(letter)
    return letter

# === Test ===
crib = "HELLO"
encrypted = ""
reset_rotors(rotors)

for char in crib:
    encrypted += encrypt_letter(char, rotors)
    step_rotors(rotors)

print(f"Encrypted: {encrypted}")

# Decrypt
reset_rotors(rotors)
decrypted = ""
for char in encrypted:
    decrypted += encrypt_letter(char, rotors)  # same process due to symmetric reflector
    step_rotors(rotors)

print(f"Decrypted: {decrypted}")
