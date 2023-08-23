from Crypto.Cipher import AES

key = b"secret#keysummerSuperSecureAyyah"
ciphertext = "e6c2921a3edb52639e871ebad04f16ff4580870a8522295cf58914b09fee749afcdd94a0beb8471dbaa50ed37693653295d4e798798674e2048f5c233cd9aba1"


def encrypt_message(key, msg):
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    msg = pad(msg).encode()
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(msg).hex()
    return ciphertext


def decrypt_message(key, ciphertext):
    BS = 16
    unpad = lambda s: s[: -ord(s[len(s) - 1 :])]
    cipher = AES.new(key, AES.MODE_ECB)
    msg = cipher.decrypt(bytes.fromhex(ciphertext)).decode()
    msg = unpad(msg)
    return msg


print(decrypt_message(key, ciphertext))
