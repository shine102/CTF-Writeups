Đây là 1 trong 3 chal mà team mình đã giải được trong giải lần này và là chal RE đầu tiên. Đây là lần đầu tiên tham gia nên khá nhiều challenge trong giải có vẻ hơi quá sức với mình và các đồng đội :(.
Giải ra chal này là kết quả research của GOG và 1 đoạn script python của FrostBurn.

I. Initial reconnaissance:

![image-20211129124122653](https://github.com/shine102/CTF-Writeups/blob/main/ISITDTU_2021/RE/warmup2.png)

- Nhìn qua thì challenge là 1 đoạn code lua, sau khi đã đọc qua hướng dẫn về lua tại [lua tutorialspoint](https://www.tutorialspoint.com/lua/index.htm) thì mình đã làm sạch nó như trên hình.

- Khi chạy bằng [Online interpreter](https://www.tutorialspoint.com/execute_lua_online.php) thì báo lỗi thiếu thư viện bit.

II. Analyze and find the vulnerabilities:

- Sau khi đọc qua về syntax của lua thì mình biết được, hàm a là hàm chính của chương trình. Đoạn code có lẽ là 1 dạng làm rối mã của lua, có thể hiểu được, tuy nhiên, để dịch ngược lại toàn bộ là điều vô cùng khó khăn. Để ý trước khi hàm a được gọi, sẽ có 1 function là loadstring() [lua doc](https://www.lua.org/pil/8.html). Vì lua là 1 ngôn ngữ thông dịch, hàm này sẽ giúp lập trình viên chạy luôn function bằng cách gọi tên_function() (như cách gọi if a then a() ở dòng cuối cùng của source code).

- Mình đã thử xóa dòng này đi, đồng thời thay a() bằng print(a) ở dòng cuối cùng. Kết quả khi chạy trên [online interpreter](https://www.tutorialspoint.com/execute_lua_online.php)
sẽ cho ra một đoạn code dễ đọc hơn nhiều. 

  ![image-20211129125539440](https://github.com/shine102/CTF-Writeups/blob/main/ISITDTU_2021/RE/warmup1.png)

- Công việc còn lại khá đơn giản, là viết 1 đoạn code để xuất ra flag, ở đây chúng mình dùng python: 
  - cipher = [61, 38, 40, 58, 40, 61, 59, 19, 30, 0, 18, 26, 51, 8, 49, 10, 27, 7, 8, 0, 11, 54, 25, 9, 6, 24, 76, 27, 28, 54, 13, 0, 21, 25, 13, 11, 2, 14, 11, 55, 19, 26, 14, 10, 51, 5, 27, 11, 31, 42, 9, 15, 26, 12, 49, 14, 1, 27, 28] key = "tuanlinh" for i, c in enumerate(cipher):    print(chr(ord(key[i%len(key)]) ^ c), end='')

III. Flag: ISITDTU{just_a_boring_warm-up_challenge_good_luck_have_fun}
