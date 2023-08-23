# Combine


## Given

[Source Code](combine.py)
[Output](output.txt)

`Flag` đã được mã hóa bằng `AES` và key mã hóa lại được mã hóa lần nữa bằng `RSA`


## Solution

Vì `e` nhỏ nên `m^e` nhỏ => ta chỉ cần [brute force](key.py) để tìm lại được `m^e`
Ra được key `secret#keysummerSuperSecureAyyah`
[Giải mã](decrypt.py) `AES` với key này ta được `Flag` `FUSEC{The_combine_crypto_system_is_really_secure!!!}`

