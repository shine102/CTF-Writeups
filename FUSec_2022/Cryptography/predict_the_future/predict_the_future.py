import os
import random
import socketserver
import sys
from binascii import hexlify


def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a % b
    return a


class AClassicalCipher:

    def __init__(self, modulus, block_size, key):

        assert(block_size > 1)
        assert(self._validate_key(modulus, block_size, key))

        self.N = modulus
        self.BLOCK_SIZE = block_size
        self.KEY = key

    def _determinant(self, M):
        """only working with square matrix.
        """
        det = 0
        if len(M) == 1 and len(M[0]) == 1:
            return M[0][0]

        indices = list(range(len(M)))
        for fc in indices:
            Ms = [[j for j in row] for row in M]  # deep copy of matrix M
            Ms = Ms[1:]
            height = len(Ms)
            for i in range(height):
                Ms[i] = Ms[i][0:fc] + Ms[i][fc+1:]
            sign = (-1) ** (fc % 2)
            sub_det = self._determinant(Ms)
            det += sign * M[0][fc] * sub_det

        return det

    def _validate_key(self, modulus, block_size, key):
        if len(key) != block_size:
            return False
        for i in range(block_size):
            if len(key[i]) != block_size:
                return False
            for j in range(block_size):
                if key[i][j] < 0 or key[i][j] >= modulus:
                    return False

        det = self._determinant(key)
        if gcd(det, modulus) != 1:
            return False

        return True

    def _encrypt_block(self, plain):
        assert(len(plain) == self.BLOCK_SIZE)
        cipher = [0] * self.BLOCK_SIZE
        for idx, _ in enumerate(plain):
            cipher[idx] = sum([plain[i] * self.KEY[i][idx]
                               for i in range(self.BLOCK_SIZE)]) % self.N

        return bytes(cipher)

    def encrypt(self, plain):
        assert(len(plain) % self.BLOCK_SIZE == 0)
        blocks = [plain[i:i+self.BLOCK_SIZE]
                  for i in range(0, len(plain), self.BLOCK_SIZE)]
        blocks = [self._encrypt_block(block) for block in blocks]
        cipher = b''.join(blocks)
        return cipher


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            r = random.Random()

            MODULUS = 251
            BLOCK_SIZE = 8
            KEY = [[r.randint(0, MODULUS) for _ in range(BLOCK_SIZE)]
                   for _ in range(BLOCK_SIZE)]
            with open("flag.txt", "rb") as f:
                flag = f.read()
            p = BLOCK_SIZE - (len(flag) % BLOCK_SIZE)
            flag += bytes([p] * p)

            cipher = AClassicalCipher(MODULUS, BLOCK_SIZE, KEY)
            ciphertext = hexlify(cipher.encrypt(flag))

            self.request.sendall(b"Welcome to the Predict the Future Game!\n")
            self.request.sendall(
                b"Great rewards for winners who can guess the correct numbers.\n")
            self.request.sendall(b"You will have 2022 chances.\n")

            count = 0
            for _ in range(2022):
                n = random.getrandbits(32)
                self.request.sendall(b"Enter your guess: ")
                guess = int(self.rfile.readline())
                if guess == n:
                    count += 1
                    if count == 1:
                        self.request.sendall(
                            f"You got it correct. Here is your first reward: {ciphertext.decode()}\n".encode())
                        self.request.sendall(b"Let us continue...\n")
                        continue
                    if count == 2:
                        self.request.sendall(
                            f"I have to admit you have completely won this game. Have your key and enjoy: {KEY}\n".encode())
                        return
                self.request.sendall(f"Oops, the number was {n}\n".encode())

            self.request.sendall(b"Oh nose...\n")
        except Exception:
            pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main(argv):
    host, port = 'localhost', 8000

    if len(argv) == 2:
        port = int(argv[1])
    elif len(argv) >= 3:
        host, port = argv[1], int(argv[2])

    sys.stderr.write('Listening {}:{}\n'.format(host, port))
    server = ThreadedTCPServer((host, port), RequestHandler)
    server.daemon_threads = True
    server.allow_reuse_address = True
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()


if __name__ == "__main__":
    main(sys.argv)
