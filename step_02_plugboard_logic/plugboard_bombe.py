def apply_plugboard(text, plugboard_map):
    return ''.join(plugboard_map.get(c, c) for c in text)

def caesar_encrypt(text, shift):
    return ''.join(chr((ord(c) - 65 + shift) % 26 + 65) for c in text)

def caesar_decrypt(text, shift):
    return ''.join(chr((ord(c) - 65 - shift) % 26 + 65) for c in text)

# Crib and plugboard simulation
crib = "HELLO"
shift = 5
original_message = apply_plugboard(crib, {'H': 'Q', 'E': 'T', 'L': 'U', 'O': 'B'})
encrypted_message = caesar_encrypt(original_message, shift)

print(f"Encrypted (with plugboard + Caesar): {encrypted_message}")
print("\nRunning Bombe logic to reverse...")

# Bombe Simulation
for guess_shift in range(26):
    decrypted = caesar_decrypt(encrypted_message, guess_shift)
    reversed_plugboard = {v: k for k, v in {'H': 'Q', 'E': 'T', 'L': 'U', 'O': 'B'}.items()}
    after_plugboard = apply_plugboard(decrypted, reversed_plugboard)
    
    if after_plugboard == crib:
        print(f"Match found! Shift = {guess_shift}")
        break
