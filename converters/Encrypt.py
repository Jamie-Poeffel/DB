import base64
import hashlib
from Crypto.Cipher import AES

def get_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def encrypt(data: str, password: str) -> str:
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode("utf-8"))
    # Ergebnis: nonce (16 Bytes) + tag (16 Bytes) + ciphertext
    return base64.b64encode(nonce + tag + ciphertext).decode("utf-8")

def decrypt(encrypted_data: str, password: str) -> str:
    key = get_key(password)
    raw = base64.b64decode(encrypted_data)
    nonce = raw[:16]
    tag = raw[16:32]
    ciphertext = raw[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode("utf-8")

def dual_encrypt(data: str, password1: str, password2: str) -> str:
    # Erste Verschlüsselung mit dem ersten Passwort
    first_encrypted = encrypt(data, password1)
    # Zweite Verschlüsselung: verschlüssele das erste Ergebnis mit dem zweiten Passwort
    second_encrypted = encrypt(first_encrypted, password2)
    return second_encrypted

def dual_decrypt(encrypted_data: str, password1: str, password2: str) -> str:
    # Entferne zuerst die zweite Verschlüsselung
    intermediate = decrypt(encrypted_data, password2)
    # Jetzt hast du das Ergebnis der ersten Verschlüsselung, das du
    # mit dem ersten Passwort entschlüsseln musst
    original = decrypt(intermediate, password1)
    return original

