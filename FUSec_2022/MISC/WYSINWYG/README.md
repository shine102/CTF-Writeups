# WYSINWYG
## Challenge
![Challenge](/FUSec_2022/MISC/WYSINWYG/images/Challenge.png)
## Solution
Sau khi tải file được cho từ đề bài (file apk), mình đã sử dụng jadx-gui để decompile cái file này.

(Do mình làm trên máy khác để viết writeup nên nó có đổi tên nhưng không ảnh hưởng gì cả)

![Decompile](/FUSec_2022/MISC/WYSINWYG/images/Decompile.png)

Cảm nhận đầu tiên sau khi mọi thứ hiện lên là "Duma sao nó rối rắm thế, chia tên như cc ý đm", "Sao lắm class với method thế đm", "ongnaolamradenaythinaocungtoday",...

Và sau một hồi mày mò trong bất lực vì nhiều, thì mình nhận ra "tại sao mình không search theo keyword là 'main' nhỉ, vì thường hàm chính sẽ liên quan đến 'main'". Nghĩ là làm, mình có search tên class, method theo keyword "Main" và tìm thấy "MainActivity"

(Đến bây giờ bình tĩnh ngồi làm lại, mới nhận ra mình tìm thấy cái này là giải xong bài rồi)

![MainActivity](/FUSec_2022/MISC/WYSINWYG/images/MainActivity.png)

Ngồi mày mò lục lọi trong này một hồi, mình biết được hàm này có kết nối đến một trang web hay server nào đó trên mạng, và việc mình cần làm là tìm được cái địa chỉ mà nó kết nối tới. Và mình đã tìm được nó, đây chính là mấu chốt

![](/FUSec_2022/MISC/WYSINWYG/images/SomeshitPart1.png)

Và mình thấy có 1 class được gọi trong phần này, mình copy toàn bộ cái class đó ra và xử lý, và đoán xem mình đã thấy gì nào

![](/FUSec_2022/MISC/WYSINWYG/images/SomeshitPart2.png)

Có ip là `34.80.117.212` và port `9006` trong tay, mình có kết nối bằng browser 😥 Bằng trực giác, mỗi lần reload trang là 1 lần có nội dung khác nhau, nên mình đã reload hẳn vài lần cho uy tín và flag xuất hiện

![flag](/FUSec_2022/MISC/WYSINWYG/images/flag.png)

Flag: `FUSec{s1Mpl3_tCp_k0MmUN1C4710n}`