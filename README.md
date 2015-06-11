# adkit

### 测试流程图
![flow](http://d.pcs.baidu.com/thumbnail/0bcc91842993dfc274b8241311a3137b?fid=2184835508-250528-1003357899818803&time=1433995200&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-DcxtlqlSmkHV12E2M2l4oClXrlI%3D&rt=sh&expires=2h&r=835486315&sharesign=unknown&size=c710_u500&quality=100)


### install

```bash
$ git clone https://github.com/adleida/adkit.git
$ cd adkit
$ sudo python3 setup.py install
```
### 参数说明

```bash
$ adkit -h
```
```
-v: adkit 版本号
-c: 为adkit 指定config 文件
-f: 指定adkit 的运行目录(默认值为当前目录, 若当前目录下有多个case, adkit会递归运行)
-n: 指定每个case 运行的次数
-t: 指定http request 的Timeout
--forever : 循环运行-f 指定的case
--normal: 仅发送case 中的request.json文件到adexchange，并打印log
```
