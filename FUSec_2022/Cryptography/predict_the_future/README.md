# Predict the future

## Problem

[src code server](predict_the_future.py)

`nc 34.80.117.212 8001`

Tổng quan đề bài là server sinh ra một số ngẫu nhiên 32 bit, và bắt chúng ta đoán nó là số nào.

Mỗi lần đoán sai thì server sẽ cho chúng ta biêt số cũ và sinh ra một số mới. Lặp lại 2022 lần.

Nếu đoán đúng đươc 2 lần thì server sẽ trả cho ta flag đã bị mã hóa bằng một thuật toán nào đó cùng với key mã hóa.

## Solution

### Part I, Lấy được flag đã mã hóa và key

Các thuật toán sinh random đều chỉ sinh ra được những số giả ngẫu nhiên nên chúng ta hoàn toàn có thể dự đoán được số tiếp theo dựa theo các số trước đó.

Các thư viện để crack được random của python đã có nhiều nên mình sẽ không phát minh lại bánh xe nữa :)

Ở đây mình dùng thư viện [rancrack](https://github.com/tna0y/Python-random-module-cracker)

Trước tiên mình gửi linh tinh để lấy được 624 số đầu tiên
```python
for i in range(624):
    print(i, end=" ")
    s.send(b"1\n")
    r = s.recv(1024)
    # thỉnh thoảng server bị lag và gửi 2 dòng cùng lúc
    if r.endswith(b"\n"):
        n = int(r[21:-1])
        s.recv(1024)
    else:
        n = int(r[21:r.index(b"\n")])
    rc.submit(n)
    print(n)
```

Sau khi đã đủ bit để crack thì mình gửi lại số được dự đoán lên server
```python
while True:
    data = str(rc.predict_getrandbits(32)).encode() + b"\n"
    print(data, end=" ")
    s.send(data)
    r = s.recv(1024)
    print(r)
    if r.endswith(b"\n"):
        print(s.recv(1024))
```

Không hiểu nhân phẩm mình bị làm sao mà gửi lên mấy lần đều không được. Đang trầm cảm, đi ra ngoài 1 tí quay lại thì thấy thằng bạn bấm hộ gửi thành công :D

Mình nhận là được flag sau khi mã hóa dưới dạng hex
`4e311c356ac2d830e82a90630690e21ad39b5cc2187bf43069fa59d47ce03c0a7b5696117ee4a43681a8800ed30ef598`

Cùng với đó là key mã hóa
`[[173, 43, 204, 198, 248, 142, 129, 224], [30, 7, 34, 212, 4, 119, 197, 137], [184, 200, 69, 125, 75, 195, 171, 167], [25, 72, 147, 191, 53, 221, 226, 166], [247, 166, 141, 148, 247, 236, 129, 114], [160, 191, 125, 237, 45, 223, 231, 63], [231, 57, 108, 85, 224, 164, 88, 135], [1, 189, 234, 196, 166, 119, 135, 145]]`

[src code](rc.py)

### Part II, Giải mã

Đây là đoạn code mã hóa của server
```python
def _encrypt_block(self, plain):
    assert(len(plain) == self.BLOCK_SIZE)
    cipher = [0] * self.BLOCK_SIZE
    for idx, _ in enumerate(plain):
        cipher[idx] = sum([plain[i] * self.KEY[i][idx]
                            for i in range(self.BLOCK_SIZE)]) % self.N
    return bytes(cipher)
```

Mình bị lú, ko hiểu đoạn code này đang làm gì :(. Lại rơi vào trầm cảm đến khi có Hint là [Hill cipher](https://en.wikipedia.org/wiki/Hill_cipher)

Đọc qua cách mã hóa của Hill cipher thì mình mới biết mình quá ngu, "Đ\*t m\*, đây là nhân mà trận mà" :D.

Đoạn code mã hóa bên trên chỉ là 1 hàm nhân ma trận nhưng cách code hơi lạ nên mình đã không nhận ra.
`[KEY]*[FLAG] = [CIPHER]`

Vậy thì bây giờ đơn giản chỉ cần tìm ma trận nghịch đảo của ma trận key là xong.
`[KEY]^-1 * [KEY] * [FLAG] = [I] * [FLAG] = [FLAG]`

Cái này thì có thể code tay, dễ hơn thì dùng thư viện `numpy` của python. Nhưng mà không, vì mình ~~lười~~ nên mình cần cài gì dễ hơn nữa [ở đây](https://planetcalc.com/3324/) :))

Quá trình giải mã cũng y hệt mã hóa là nhân ma trận nên mình tận dụng lại luôn code mã hóa.
```python
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
# b'FUSec{th15_ch4ll3ng3_w0nt_s4t1sfy_y0u_I_gu3ss}\x02\x02'
```

[src code](solve.py)
