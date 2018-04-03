# WITALK 在线社区系统
1. 按照requirements.txt内容，安装依赖的相关程序
2. 修改configuration.py，修改相关信息
3. 配置nginx转发fastcgi配置如下：
```
server{
    listen 80;
    server_name xxx.com;
    location / {
        fastcgi_pass 127.0.0.1:5200;
	include fastcgi.conf;
    }
}
```
5. 启动nginx
6. 切换到项目根目录执行 ./start.sh启动fastcgi解释器进程
7. 结束

>若有其他问题，看工程代码不能解决，请在<https://witalk.cc/f/witalk>开主题询问哦 !
