# 代充网(daichong.vip)逆向
> 目的:逆向出账号支付接口,以便于后端调用
> 
> 目前不足: 未制作cookie注入
> 
> 
> 

## 关键逆向点:
### hashsalt
> 在某个传过来的js文件中找到了hashsalt的值,为一串很奇怪的值,此值为一堆奇怪的字符组合,经调试发现
> 此字符组合可以被js执行,并返回hashsalt


### orderid
> 发现最终的请求需要传入一个orderid,直接找orderid难以找到根源,故直接搜索ajax请求,找到orderid原来是
> 二号请求的trade_no,于是进行二号请求(二号请求需要传入hashsalt,刚好就有)


最终,发送请求的顺序:
1. 获取js 解析为hashsalt
2. 传入hashsalt,获取到trade_no
3. 传入trade_no,成功支付