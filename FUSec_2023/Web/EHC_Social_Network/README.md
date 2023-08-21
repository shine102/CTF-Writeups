# EHC Social Network

Đây là bài đầu tiên mình làm về lỗi prototype pollution (mỗi dịp đi thi đều có những dạng bài lần đầu làm, đây là điểm mình vô cùng thích khi chơi CTF). Cảm ơn anh Antoine Nguyễn đã cho mình 1 challenge thú vị như vậy.

Trong lúc thi, thì mình chỉ giải được phần 1 của challenge, tuy nhiên sau khi về nhà nghiền ngẫm, thì mình đã giải được phần 2 của challenge này.

## Description
- Link: https://ehc-social-network.fptunisecathon2023.tech/
- Source code: [source code](./src)
- Ảnh: ![image](./img/1.png)

## Part 1: IDOR 
Bài này cho source code khá dài, cùng với 1 số tính năng, mình sẽ tóm tắt lại những điểm quan trọng nhất.

![tweet](./img/2.png)

Đây là tính năng đầu tiên, bạn sẽ tạo 1 tweet, khi tạo xong sẽ redirect tới trang hiển thị nội dung tweet.

![tweet](./img/3.png)

`status` chính là số thứ tự của tweet vừa tạo trong mảng tweet, hash là giá trị của `status` sau khi được mã hóa bằng hàm `makeHash`.

![hash](./img/4.png)

Điều đáng chú ý là khi start server, một tweet sẽ được tạo sẵn, với status là 0, nội dung của tweet là flag của part 1. 
![flag](./img/5.png)

Cách duy nhất để lấy flag chính là tìm cách lấy được hash của tweet với status 0 này.

Ban đầu, khi mới đọc thoáng qua code, mình cảm thấy lấy được hash của tweet là điều không thể, vì hàm hash đã được thêm salt random vào, và mình không thể biết được giá trị của salt này. Tuy nhiên khi nhìn kỹ hơn, chúng ta có thể thấy, phần tạo salt có vẻ chưa được code 1 cách chuẩn chỉ cho lắm

![salt](./img/6.png)

```salt-${crypto.randomBytes(10).toString}``` luôn trả về 1 giá trị duy nhất do hàm toString không được gọi đúng cách trên mỗi phiên bản của Node. Điều này đã được mình kiểm chứng bằng cách start server trên local nhiều lần thì giá trị salt không thay đổi.

Từ đó, chúng ta sẽ sửa source code ở local và tìm cách lấy được hash của tweet với status 0.

![hash](./img/7.png)

Call tới api /get_tweet với status=0 và hash=1aceba1a720b2e9284eea7d9f5c7cb18b390d195 sẽ trả về nội dung của tweet với status=0.

![flag](./img/8.png)

## Part 2: Prototype Pollution
Đây là phần mình đã giải được sau khi về nhà. Đây là phần mình thích nhất, vì đây là lần đầu tiên mình khai thác 1 lỗi prototype pollution.

![profile](./img/9.png)

Đây là endpoint thứ 2, mình sẽ nhập flag của part 1 vào, và lên prime :)) 

![prime](./img/10.png)

![code](./img/12.png)
Đoạn code kiểm tra flag của part 1.

Sau khi "Bấm vào để xem các idol nói gì", sẽ có danh sách 1 list các câu nói của idol mạng xuất hiện.

![list](./img/11.png)

Đây là đoạn code để lấy danh sách các câu nói của idol mạng xuất hiện.
![code](./img/13.png)

Để nói về nodejs prototype pollution, mình đã đọc khá nhiều tài liệu, và mình recommend các bạn đọc ở trang: https://book.hacktricks.xyz/pentesting-web/deserialization/nodejs-proto-prototype-pollution, và trang: https://book.hacktricks.xyz/pentesting-web/deserialization/nodejs-proto-prototype-pollution/prototype-pollution-to-rce

Để tóm tắt lại, thì prototype pollution là 1 lỗi xảy ra khi chúng ta có thể thay đổi các thuộc tính của object prototype, từ đó có thể thay đổi các thuộc tính của object kế thừa từ object prototype đó.

Trong tài liệu, có chỉ ra 3 trường hợp có thể dẫn tới prototype pollution, và ở bài này, đoạn code bị dính nằm ở trường hợp: `Perform recursive merge`

![code](./img/14.png)

Đoạn code này được call ở function xử lý cho endpoint `/quote2`. Vì vậy, chúng ta sẽ tìm cách để thực hiện prototype pollution ở đây.

![code](./img/15.png)

Hàm `combine` bị lỗi được truyền 2 parameter là `superQuote` được merge 2 file `top-quote-1.js` và `top-quote-2.js` và `data` được truyền từ client.

Cộng thêm với việc ở api `/quote1`, chúng ta có thể sử dụng hàm require để require 1 file bất kì, chúng ta sẽ có hướng exploit như sau.

Đầu tiên, sử dụng api `/quote2` để pollute prototype của Object trong javascript, sau đó sử dụng api `/quote1` để require 1 file js bất kì trong hệ thống có chứa hàm `child_process`, từ đó có thể RCE.

Cụ thể các bạn hãy đọc trong 2 link mà mình đã mention ở phía trên để hiểu rõ hơn, mình sẽ trình bày payload của mình.

1. Mình đã vào môi trường ở máy local, tìm được file thỏa mãn yêu cầu là file `/usr/local/lib/node_modules/npm/scripts/changelog.js`. Đây là file có chứa đoạn code cần thiết để RCE.
![code](./img/16.png)

2. Xác định được hàm sẽ thực thi đoạn code để RCE là hàm `execSync` của module `child_process`. Chúng ta sẽ tiến hành pollute prototype của Object bằng cách gửi request tới api `/quote2` với data là 1 object có key là `__proto__` và value là các object có key và value như hình

![payload](./img/17.png) ![payload](./img/18.png) ![payload](./img/19.png)

3. Gửi request tới api `/quote1` với data là 
```
{
    "list": "../../../../usr/local/lib/node_modules/npm/scripts/changelog.js"
}
```
 và bùm, chúng ta có reverse shell.
![shell](./img/20.png)

và lấy được flag nhờ execute file getFlag
![flag](./img/21.png)

## Kết

GGWP :D 