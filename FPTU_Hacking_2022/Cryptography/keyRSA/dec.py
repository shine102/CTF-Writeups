import socket

HOST = "103.245.249.76"
PORT = 49160

def receive_until(s: socket.socket, c):
    msg = ""
    while True:
        m = s.recv(1).decode()
        msg += m
        if m == c:
            return msg

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    receive_until(s, ")")
    s.send(b"y")
    receive_until(s, "\n") # \n
    receive_until(s, "\n") # sure...
    receive_until(s, "\n") # \n

    e = int(receive_until(s, "\n")[4:]) # e
    n = int(receive_until(s, "\n")[4:]) # n
    p = int(receive_until(s, "\n")[4:]) # x

    receive_until(s, "\n") # enter...

    q = n // p
    f = (p-1) * (q-1)
    d = pow(e, -1, f)
    s.send(str(d+f).encode())

    print(s.recv(1000))
