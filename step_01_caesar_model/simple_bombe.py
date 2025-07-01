# simple_bombe.py

# --- Step 1: Define Caesar encryption ---
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

# --- Step 2: Define Caesar decryption ---
def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# --- Step 3: Simulate Enigma encryption (very simplified) ---
crib = "HELLO"
secret_shift = 5  # This is like our rotor setting
ciphertext = caesar_encrypt(crib, secret_shift)
print(f"Encrypted (fake Enigma): {ciphertext}")

# --- Step 4: Bombe-style logic to guess the shift ---
print("\nRunning Bombe logic to find the shift...")
for guess_shift in range(26):
    attempt = caesar_decrypt(ciphertext, guess_shift)
    if attempt == crib:
        print(f"Match found! Shift = {guess_shift}")
        break
else:
    print("No match found.")
