import string
from copy import deepcopy

class Rotor:
    def __init__(self, wiring, notch):
        self.base_wiring = wiring
        self.notch = notch
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

    def set_position(self, pos):
        self.position = pos % 26
        self._update_wiring()

    def encrypt(self, char):
        return self.wiring.get(char, char)

    def decrypt(self, char):
        return self.reverse_wiring.get(char, char)

def reflect(char):
    reflection = dict(zip(string.ascii_uppercase, reversed(string.ascii_uppercase)))
    return reflection.get(char, char)

def encrypt_letter(letter, rotors):
    for r in rotors:
        letter = r.encrypt(letter)
    letter = reflect(letter)
    for r in reversed(rotors):
        letter = r.decrypt(letter)
    return letter

def step_rotors(rotors):
    rotors[0].step()
    if rotors[0].at_notch():
        rotors[1].step()
    if rotors[1].at_notch():
        rotors[2].step()

def reset_rotors(rotors, positions):
    for r, p in zip(rotors, positions):
        r.set_position(p)

# === Simulation Start ===
crib = "HELLO"
wiring = dict(zip(string.ascii_uppercase, string.ascii_uppercase[1:] + "A"))

# Setup rotors with secret position
rotor1 = Rotor(deepcopy(wiring), notch=5)
rotor2 = Rotor(deepcopy(wiring), notch=5)
rotor3 = Rotor(deepcopy(wiring), notch=5)
rotors = [rotor1, rotor2, rotor3]

secret_positions = [3, 12, 7]
reset_rotors(rotors, secret_positions)

encrypted = ""
for c in crib:
    encrypted += encrypt_letter(c, rotors)
    step_rotors(rotors)

print(f"[ENCRYPTED]: {encrypted}")

# === Bombe crack
print("\n[🔍 BOMBE CRACKING]")
for a in range(26):
    for b in range(26):
        for c in range(26):
            test_rotors = [
                Rotor(deepcopy(wiring), notch=5),
                Rotor(deepcopy(wiring), notch=5),
                Rotor(deepcopy(wiring), notch=5),
            ]
            reset_rotors(test_rotors, [a, b, c])

            candidate = ""
            for char in encrypted:
                candidate += encrypt_letter(char, test_rotors)
                step_rotors(test_rotors)

            if crib in candidate:
                print(f"\n✅ Match found!")
                print(f"Decrypted: {candidate}")
                print(f"Positions: R1={a}, R2={b}, R3={c}")
                exit()

print("No match found.")
