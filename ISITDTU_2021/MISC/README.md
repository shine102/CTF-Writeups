# Characters

Đề bài cho chúng ta tệp [Characters.rar](https://drive.google.com/file/d/1v4u8Iu8CAB97uV-3CV7E4-A-ica_ZvSC/view?usp=sharing), sau khi tải về giải nén ta được 2 file tương ứng như hình bên dưới:

![image-20211129133527782](C:\Users\Asus\AppData\Roaming\Typora\typora-user-images\image-20211129133527782.png)

Bên trong file Hex_Base.rar bao gồm một tập tin Player.txt (được bảo vệ bằng mật khẩu) và một đoạn mã `466f726d61742074686520666c6167206279206368617261637465723a20377b375f325f31307d`:

![image-20211129133944729](C:\Users\Asus\AppData\Roaming\Typora\typora-user-images\image-20211129133944729.png)

Có thể đoán flag có thể ẩn giấu đâu đó trong tệp *.txt được bảo vệ kia. Như vậy nhiệm vụ trước mắt của chúng ta bây giờ là đi tìm được cái đoạn mật khẩu đó để tìm hiểu xem nội dung bên trong của Player.txt. Các dữ kiện chúng ta đang có là đoạn mã dài loằng ngoằng ở trên và tệp Go_find_the_flag.txt. Dựa vào tên của tệp thì ta có thể đoán đây là mã hex, giải mã ra cho chúng ta nội dung  `Format the flag by character: 7{7_2_10}`. Có thể suy luận đây là định dạng của flag trong bài này.

Việc tiếp theo của chúng ta là kiểm tra file Go_find_the_flag.txt kia:

`ak ak ak ak ak ak ak ak ak ak pika pipi ak pipi ak ak ak pipi ak ak ak ak ak ak ak pipi ak ak ak ak ak ak ak ak ak ak pichu pichu pichu pichu ka chu pipi pipi pipi ak ak ak ak ak ak ak ak ak ak ak ak ak ak pikachu pipi ak ak ak ak pikachu ka ka ka pikachu pichu pichu ak ak pikachu pipi pipi ak ak ak ak ak ak ak ak ak ak ak pikachu pichu ak ak ak ak ak ak ak ak ak ak ak ak ak pikachu pipi ak ak ak pikachu pikachu ak ak ak ak pikachu ka ka ka ka ka ka ka ka pikachu ak ak ak pikachu pichu ak ak ak pikachu pichu pikachu pipi ak ak ak ak ak pikachu pipi ak pikachu pichu pichu ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak pikachu pichu ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak ak pikachu pipi ka ka ka pikachu pikachu ka ka ka ka ka pikachu ka pikachu ka pikachu`

Nhìn có vẻ khá là pikachu, nhìn kỹ hơn thì đây có khả năng chính là pikalang (mà theo như người tạo ra nó mô tả là biến thể của Brainfuck dựa trên nhân vật Pikachu). Về cơ bản thì nó chỉ thay thế các ký tự của brainfuck thành các từ có trong cái tên của nhân vật này bao gồm: `pi, ka, pika, chu, pipi, pichu, pikapi, pikachu`

![image-20211129135924460](C:\Users\Asus\AppData\Roaming\Typora\typora-user-images\image-20211129135924460.png)

Thông qua trang [Dcode.fr](https://www.dcode.fr/pikalang-language)  này ta có thể dễ dịch chuyển đổi đoạn mã trên. Tuy nhiên chúng ta lại gặp khó khăn vì dựa vào bảng mã chuyển thể thì `ak` không có tương ứng ở brainfuck. Vậy nên đoạn mã trên không thể dịch được. Điều cần làm bây giờ là phải xoá hoặc thay thế `ak` để nó có thể dịch được. Mình có thử xoá nó đi thì ra các ký tự không rõ ràng. Vậy ta có thể loại trừ phương pháp này. Điều còn lại ta có thể thử từng ký tự trong bản trên với hi vọng mong manh là tìm được lựa chọn thích hợp. Tuy nhiên thử thì cũng hơi lâu nên mình mò lại đề bài xem có tìm được gì hay ho không,

Theo như đề bài thì đoạn flag bắt đầu bằng `ISITDTU{}`, mình thử dịch đoạn này sang pikalang:

`pi pi pi pi pi pi pi pi pi pi pika pipi pi pipi pi pi pi pipi pi pi pi pi pi pi pi pipi pi pi pi pi pi pi pi pi pi pi pichu pichu pichu pichu ka chu pipi pipi pipi pipi pi pi pi pi pi pikachu pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pi pikachu pi pi pi pi pi pi pikachu pi pi pikachu pichu pichu pichu pi pi pi pi pi pi pi pi pi pi pikachu` 

Đem kết quả này so sánh với đoạn mã trên, mình thấy nó có vẻ tương đồng với nhau nếu thay `ak` thành `pi`. Thử thay thế phương án này, dịch ra thì được `The password is: 77210`. Như vậy là quá rõ ràng rồi, hi vọng là không có cú lừa nào ở đây.

Thật may là không có cú lừa nào cả, file Hex_Base.rar giải nén thành công. Nội dung bên trong file Player.txt:

`IFdlbGNvbWUgdG8gSVNJVERUVSBDVEYgMjAyMSEKIEhlcmUgaXMgYSBsaXN0IG9mIHRoZSBwbGF5ZXJzIEkgZm91bmQKLS0tLS0tLS0tLSAtLS0tLS0tLS0tLQpELiBBbGxpCkYuIFRvcnJlcwpDLiBIdWRzb24tT2RvaQpNLiBNb3VudApNLiBSYXNoZm9yZApDLiBMZW5nbGV0ClIuIEx1a2FrdQpBLiBHcmllem1hbm4KQy4gUm9uYWxkbwpELiBQYXlldApKLiBLaW1taWNoCkwuIE1lc3NpCkcuIEhpZ3VhaW4KUC4gQXViYW1leWFuZwpYYXZpClMuIFJhbW9zCkUuIENhdmFuaQpQLiBMYWhtCksuIFRyYXBwCkouIFNhbmNobwpULiBLcm9vcwpLLiBOYXZhcwpNLiBJY2FyZGkKSi4gVGl2YWIKSy4gU2NobWVpY2hlbApHLkJhbGUKLS0tLS0tLS0tLSAtLS0tLS0tLS0tLQpUaGUgRW5kCiEgIQoK`

Rõ ràng đây là Base64, do đó kết quả của việc decode:

 `Welcome to ISITDTU CTF 2021!`
`Here is a list of the players I found`

---------- -----------
`D. Alli`
`F. Torres`
`C. Hudson-Odoi`
`M. Mount`
`M. Rashford`
`C. Lenglet`
`R. Lukaku`
`A. Griezmann`
`C. Ronaldo`
`D. Payet`
`J. Kimmich`
`L. Messi`
`G. Higuain`
`P. Aubameyang`
`Xavi`
`S. Ramos`
`E. Cavani`
`P. Lahm`
`K. Trapp`
`J. Sancho`
`T. Kroos`
`K. Navas`
`M. Icardi`
`J. Tivab`
`K. Schmeichel`
`G.Bale`

---------- -----------
`The End`
`! !`

Đến đây mình đã hi vọng không có cái mã hoá nào gọi là playerlang, cũng may là không có. Mình đã thử đã xem có sự liên quan nào đến flag hay không. Qua kiểm tra, mình phát hiện kí tự cuối cùng của tên 7 cầu thủ đầu tiên trong danh sách là `isitdtu` giống như format của flag là `ISITDTU{}`. Vậy thì đã quá rõ ràng, tiếp tục thì mình thu được `isitdtunothingisimpossible`. Kết hợp với dữ kiện tìm được ở trên, mình có được kết quả của bài.

Flag: `isitdtu{nothing_is_impossible}`