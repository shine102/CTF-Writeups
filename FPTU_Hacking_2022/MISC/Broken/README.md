# Broken

## Challenge

It's a correct image? [flag.png](https://user-images.githubusercontent.com/19572025/175891933-7cc67973-4cbc-463e-a26d-0a1ce0a19b7e.png)

## Writeup
Đề bài cho ta một file có vẻ như là một file ảnh, và nó không thể xem được. Tuy nhiên, để chắc chắn đây đúng là một file png, mình đã dùng đến công cụ pngcheck để kiểm tra. 
```
$ pngcheck flag.png
flag.png  first chunk must be IHDR
ERROR: flag.png

```

Kết quả trả về cho ta biết file ảnh đã có vấn đề liên quan tới IHDR. Qua nghiên cứu, các kết quả liên quan tới vấn đề trên được mình tìm thấy trong trang [PNG Specification, Version 1.2](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html). Vậy ta cần khắc phục nó trước tiên.

Mình đã sử dụng [Hexedit](hexed.it) để kiểm tra file ảnh trên và phát hiện có điều không đúng khi trong phần header đã bị thiếu mất phần khai báo IHDR. Lạ lùng là ở địa chỉ `0x0000000C`, nó đã được thay thế bằng FPTU, việc thay thế , chỉnh sửa lại cho đúng cũng không tốn nhiều công sức. Tuy nhiên, vấn đề khác lại tiếp tục phát sinh:
```
$ pngcheck flag_fixedIHDR.png 
flag_fixedIHDR.png  invalid IHDR image dimensions (0x0)
ERROR: flag_fixedIHDR.png
```
Kết quả trả về khi dùng pngcheck cho ta biết file ảnh trên chưa có kích thước hợp lý. Trong tài liệu tìm về [PNG Chunks](https://www.w3.org/TR/PNG-Chunks.html), thông tin về độ rộng và chiều cao được thể hiện lần lượt trong 4 bytes đầu và 4 bytes tiếp theo. Mình đã thử thay thế kích thước này một cách ngẫu nhiên và kiểm tra lại thì lần này lại ra một vấn đề khác:

```
$ pngcheck flag_fixedDim.png 
flag_fixedDim.png  CRC error in chunk IHDR (computed 9a8f986c, expected aa0c1e79)
ERROR: flag_fixedDim.png
```

Một thứ gì đó liên quan đến CRC, pngcheck tính được ta cần dãy bytes `9A 8F 98 6C` thay vì `61 20 55 AA`. Mình đã thay thế nó, tuy nhiên kết quả ra được là một bức ảnh quái dị 

![image](https://user-images.githubusercontent.com/19572025/175998795-8ad35cc7-b724-4dbd-8587-371e3900c66d.png)

Thử với các kích thước khác, mình lại nhận được các bức ảnh kì quặc khác nhau. Vậy vấn đề đã rõ, điều tiếp theo mình cần làm là đi xác định kích thước chính xác của bức ảnh. Quay trở lại với pngcheck, mình nhận thấy mỗi lần thay đổi kích thước đi kèm với việc có một lỗi CRC khác. Nói cách khác, có sự liên hệ gì đó với CRC này, tức là nó có thể tính được. Ngay từ đầu, CRC đã được tính sẵn, vậy mình chỉ cần từ cái ban đầu quay ngược lại kích thước.  Vì thế, mình đã quyết định đi bruteforce ra chiều rộng và chiều cao.

```python
from binascii import crc32

correctCRC = int.from_bytes(b'\x61\x20\x55\xAA',byteorder='big')

for height in range(4000):
    for width in range(4000):
        tempCRC=b"\x49\x48\x44\x52"+width.to_bytes(4,byteorder='big')+height.to_bytes(4,byteorder='big')+b"\x08\x02\x00\x00\x00"
        if crc32(tempCRC) % (1<<32) == correctCRC:
            print ('Width: ',end="")
            print (hex(width))
            print ('Height :',end="")
            print (hex(height))
            exit()
```

Sau khi chạy đoạn script trên, mình đã xác định được kích thước tương đối của file ảnh này.  
```
$ python3 crc.py 
Width: 0x3f1
Height: 0xda
```

Kết quả sau khi sửa lại kích thước ảnh
```
$ pngcheck flag_fixed.png 
OK: flag_fixed.png (1009x218, 24-bit RGB, non-interlaced, 98.9%).
```
Sau cùng, đây là những gì mình nhận được

![image](https://user-images.githubusercontent.com/19572025/176132464-cfd43896-2bd4-4793-8980-29e467b81dc0.png)

Flag: `FPTUHacking{ju5t_ba5s1c_1HdR_r1ght}`