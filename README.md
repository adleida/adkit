# adkit

### Test flow
![flow](https://github.com/adleida/adkit/blob/master/bid.png?raw=true)

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
