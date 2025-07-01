import string

# Simple example rotor with fixed wiring (just a Caesar +1 for now)
rotor_forward = dict(zip(string.ascii_uppercase, string.ascii_uppercase[1:] + "A"))
rotor_reverse = {v: k for k, v in rotor_forward.items()}

def step_rotor(rotor_map):
    letters = list(string.ascii_uppercase)
    stepped = letters[1:] + letters[:1]
    return dict(zip(letters, stepped))

def encrypt_letter(letter, rotor_map):
    return rotor_map.get(letter, letter)

def decrypt_letter(letter, rotor_map):
    return rotor_map.get(letter, letter)

def encrypt_message(message, rotor_map):
    result = ""
    for letter in message:
        result += encrypt_letter(letter, rotor_map)
        rotor_map = step_rotor(rotor_map)
    return result

def decrypt_message(message, rotor_map):
    result = ""
    for letter in message:
        result += decrypt_letter(letter, rotor_map)
        rotor_map = step_rotor(rotor_map)
    return result

# === Test ===
crib = "HELLO"
rotor = rotor_forward.copy()

encrypted = encrypt_message(crib, rotor.copy())
print(f"Encrypted with stepping rotor: {encrypted}")

# Reset rotor for decryption
decrypted = decrypt_message(encrypted, rotor_reverse.copy())
print(f"Decrypted back (reversing wiring): {decrypted}")
