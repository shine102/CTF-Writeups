
from binascii import hexlify, unhexlify
import string


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


ct = unhexlify(b"4e311c356ac2d830e82a90630690e21ad39b5cc2187bf43069fa59d47ce03c0a7b5696117ee4a43681a8800ed30ef598")

KEY = [[173, 43, 204, 198, 248, 142, 129, 224], [30, 7, 34, 212, 4, 119, 197, 137], [184, 200, 69, 125, 75, 195, 171, 167], [25, 72, 147, 191, 53, 221, 226, 166], [247, 166, 141, 148, 247, 236, 129, 114], [160, 191, 125, 237, 45, 223, 231, 63], [231, 57, 108, 85, 224, 164, 88, 135], [1, 189, 234, 196, 166, 119, 135, 145]]
MODULUS = 251
BLOCK_SIZE = 8

KEY_INV = [[203,222,116,241,87,42,17,121],
[70,192,56,56,11,13,163,13],
[174,139,81,135,238,144,50,155],
[81,13,53,61,68,204,116,245],
[133,178,148,23,126,43,82,101],
[179,76,243,112,155,127,20,90],
[27,146,158,152,66,17,192,123],
[221,84,224,165,149,67,26,184],]

cipher = AClassicalCipher(MODULUS, BLOCK_SIZE, KEY_INV)

print(cipher.encrypt(ct))
