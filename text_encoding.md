Python
======
无法解码的问题，直到看了这篇[博文](http://blog.csdn.net/a657941877/article/details/9063883)才算闹明白。执行以下代码时：
```Python
s = '中文'  # 注意这里的 str 是 str 类型的，而不是 unicode   
s.encode('gb18030')
```
一般会出现异常如
```Python
UnicodeDecodeError: 'ascii' codec can't decode byte ... in position
```
时，这是因为Python在解码文本字符串为```Unicode```时使用了错误的编码，所以只要使用正确的编码进行解码就能避免这样的错误：
```
s.decode('utf-8')
```

Java
====
输出XML时遇到错误：
```Java
javax.xml.transform.TransformerException: java.io.IOException: Detected invalid substitute UTF-16: xxxx xx ?
```
可能的解决办法是将字符串转换为utf-8：
```Java
try {
    res = new String(res.getBytes(),"utf8");
} catch (UnsupportedEncodingException e) {
    e.printStackTrace();
}
```
