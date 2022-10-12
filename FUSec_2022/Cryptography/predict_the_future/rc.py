import socket

from randcrack import RandCrack

HOST = "34.80.117.212"
PORT = 8001

rc = RandCrack()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.recv(1024)
    s.recv(1024)
    for i in range(624):
        print(i, end=" ")
        s.send(b"1\n")
        r = s.recv(1024)
        # thỉnh thoagnr server bị lag và gửi 2 dòng cùng lúc
        if r.endswith(b"\n"):
            n = int(r[21:-1])
            s.recv(1024)
        else:
            n = int(r[21:r.index(b"\n")])
        rc.submit(n)
        print(n)
    while True:
        data = str(rc.predict_getrandbits(32)).encode() + b"\n"
        print(data, end=" ")
        s.send(data)
        r = s.recv(1024)
        print(r)
        if r.endswith(b"\n"):
            print(s.recv(1024))
