# sshpass远程命令执行



## 1、下载&安装

[sshpass的安装与使用-CSDN博客](https://blog.csdn.net/weixin_42405670/article/details/127191983)

[sshpass离线安装+应用场景_sshpass安装包-CSDN博客](https://blog.csdn.net/weixin_51788950/article/details/130731372)



## 2、使用

```shell
# 命令执行
sshpass -p "123456" ssh root@192.168.112.211 "shell command"

# scp
sshpass -p "123456" scp -o "StrictHostKeyChecking no" local_path root@192.168.112.211:remote_path

-o "StrictHostKeyChecking no" 第一次连远程IP，使用该参数，可以避免“if connect”的交互确认


```

```shell
# 多个远程IP的遍历
## 命令执行
if ["$#" -ne 2];then
    echo "cmd file missing ..."
    # invaild argument
    exit 22
fi

cmd=$1
IPs=$2

if [! -s $cmd || ! -s $IPs];then
    echo "cmd file not exists ..."
    # No such file or directory
    exit 2
fi

while IFS= read -r ip; do
    echo "server ${ip}"
    sshpass -p "123456" ssh root@192.168.112.211 < cmd
    echo $?
done < $IPs

## scp
if ["$#" -ne 3];then
    echo "cmd file missing ..."
    # invaild argument
    exit 22
fi

local_path=$1
remote_path=$2
IPs=$3

if [! -s $local_path || ! -s $remote_path || ! -s $IPs];then
    echo "cmd file not exists ..."
    # No such file or directory
    exit 2
fi

while IFS= read -r ip; do
    echo "server ${ip}"
    sshpass -p "123456" scp local_path root@192.168.112.211:remote_path
    echo $?
done < $IPs



```



## 3、常用cmd整理

```shell
# 后台启动python脚本
nohup python -u XXX.py >> log.log 2>&1 &

# 杀死后台进程 XXX是你启动脚本的名称
ps -ef | grep XXX | awk '{print $2}' | xargs -n 1 kill -9


# 文件的替换修改
whereis ffmpeg
sed -i 's/ffmpeg/\/home\/xin\/miniconda3\/bin\/ffmpeg/g' XXX.py

# 文件增加行修改
sed -i '19a\    print(s)\' XXX.py
```



## 4、注意

1、所有涉及路径or命令，最好都写绝对路径

2、涉及服务器上传和下载操作的，需检查代理，必要时执行如下命令：

    unset http_proxy

    unset https_proxy


