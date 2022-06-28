# characters

Ở bài này, chúng ta lại được cho [source code](enc.py) và [n, e và c của từng ký tự](out.txt)

Thay vì encrypt toàn bộ flag bằng RSA trong 1 lần thì bài này encrypt từng ký tự. Điều này không làm ảnh được đến việc decrypt.

Vì N nhỏ nên mình liền vứt thử lên [factordb](http://factordb.com/) thì ra được:
`p = 74437321397109323485877016517`
và
`q = 79150800181745408199941108327`

Giải mã từng ký tự ra được flag: `FPTUHacking{3ncRYpt1ng_34ch_ch4r_ainT_G0nn4_h3lp}`

Full src code để giải bài này [ở đây](dec.py)
