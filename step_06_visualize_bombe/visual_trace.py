import string
from copy import deepcopy

class Rotor:
    def __init__(self, wiring, notch, name):
        self.base_wiring = wiring
        self.notch = notch
        self.position = 0
        self.name = name
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

    def set_position(self, pos):
        self.position = pos % 26
        self._update_wiring()

    def encrypt(self, char):
        return self.wiring.get(char, char)

    def decrypt(self, char):
        return self.reverse_wiring.get(char, char)

    def label(self):
        return f"{self.name}:{self.letters[self.position]}"

def reflect(char):
    reflection = dict(zip(string.ascii_uppercase, reversed(string.ascii_uppercase)))
    return reflection.get(char, char)

def step_rotors(rotors):
    rotors[0].step()
    if rotors[0].at_notch():
        rotors[1].step()
    if rotors[1].at_notch():
        rotors[2].step()

def reset_rotors(rotors, positions):
    for r, p in zip(rotors, positions):
        r.set_position(p)

def encrypt_trace(letter, rotors):
    trace = [letter]
    # Forward pass
    for r in rotors:
        letter = r.encrypt(letter)
        trace.append(letter)
    # Reflector
    letter = reflect(letter)
    trace.append(f"({letter})")
    # Reverse pass
    for r in reversed(rotors):
        letter = r.decrypt(letter)
        trace.append(letter)
    return trace

# === Rotor Setup ===
wiring = dict(zip(string.ascii_uppercase, string.ascii_uppercase[1:] + "A"))

rotor1 = Rotor(deepcopy(wiring), notch=5, name="R1")
rotor2 = Rotor(deepcopy(wiring), notch=5, name="R2")
rotor3 = Rotor(deepcopy(wiring), notch=5, name="R3")
rotors = [rotor1, rotor2, rotor3]

start_positions = [3, 0, 6]
reset_rotors(rotors, start_positions)

crib = "HELLO"
encrypted = ""

print("\n🧠 Bombe Trace – Step-by-step")
print("="*40)

for step_num, char in enumerate(crib, 1):
    trace = encrypt_trace(char, rotors)
    encrypted += trace[-1]

    rotor_labels = " | ".join([r.label() for r in rotors])
    path = " → ".join(trace)

    print(f"\nStep {step_num}")
    print(f"Rotor Positions: {rotor_labels}")
    print(f"Trace: {path}")
    print(f"Encrypted: {trace[-1]}")

    step_rotors(rotors)

print("\n" + "="*40)
print(f"Final Encrypted Message: {encrypted}")
