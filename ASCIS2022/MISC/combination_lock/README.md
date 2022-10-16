# Combination Lock
## Challenge

![Challenge](/ASCIS2022/MISC/combination_lock/images/challenge.png)

[File Source](/ASCIS2022/MISC/combination_lock/CombinationLock.zip)

## Solution

Lúc nhận được file, mình có unzip ra và nhận ra đây là 1 file ELF, nên mình đã sử dụng Ghidra để decompile xem nó làm gì nhưng sau một hồi loay hoay, mình đã quyết định chạy file xem nó làm gì. Sau một hồi hú hí, mình đã tìm ra được quy luật của r1 và r2. 

Mình sẽ đặt tên 8 thanh đó là N1 => N8, R1 và R2 sẽ được tính như sau

```
R1 = (N1 * N2) + (N3 * N4) + (N5 * N6) + (N7 * N8)
R2 = (N1 + N2) * (N3 + N4) * (N5 + N6) * (N7 + N8)

Với N1, N2,..., N8 nhận các giá trị từ 0 -> 8
```

Và nếu R1 = 88 và R2 = 8800 thì mình sẽ có flag

Với kiến thức toán học cũng như kiến thức về thuật toán có hạn, mình đã viết 1 cái [script](/ASCIS2022/MISC/combination_lock/script.py) trông hơi ngu để bruteforce tìm N1 -> N8

```python
for n1 in range(0,9):
    for n2 in range(0,9):
        for n3 in range(0,9):
            for n4 in range(0,9):
                for n5 in range(0,9):
                    for n6 in range(0,9):
                        for n7 in range(0,9):
                            for n8 in range(0,9):
                                r1 = (n1 * n2) + (n3 * n4) + (n5 * n6) + (n7 * n8)
                                r2 = (n1 + n2) * (n3 + n4) * (n5 + n6) * (n7 + n8)
                                if(r1 == 88 and r2 == 8800):
                                    print("{} {} {} {} {} {} {} {} ".format(n1, n2, n3, n4, n5, n6, n7, n8))
                                    exit()
```

Và sau khi chạy mình đã nhận lại được kết quả `2 6 3 7 5 5 5 6` tương ứng với các vị trí từ N1 -> N8

![solved](/ASCIS2022/MISC/combination_lock/images/solved.png)

Flag: `ASCIS{ca3512f4dfa95a03169c5a670a4c91a19b3077b4}`