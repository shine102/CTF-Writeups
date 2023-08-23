#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getStrongPrime
from secret import flag, key


def encrypt_message(key, msg):
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    msg = pad(msg).encode()
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(msg).hex()
    return ciphertext


def encrypt_key(key):
    nbit = 2048
    p = getStrongPrime(nbit // 2)
    q = getStrongPrime(nbit // 2)
    n = p * q
    e = 3
    m = bytes_to_long(key)
    cipherkey = pow(m, e, n)
    return n, e, cipherkey


ciphertext = encrypt_message(key, flag)
n, e, c = encrypt_key(key)

print("n =", n)
print("e =", e)
print("cipherkey =", c)
print("ciphertext =", ciphertext)
