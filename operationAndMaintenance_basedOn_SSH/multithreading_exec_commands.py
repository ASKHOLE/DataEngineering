import time
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from utils.ssh_client import SSHClient, connect

user_name = ""
user_passwd = ""
command = ""


def exec_command(cmd, user, passwd, ip):
    global lock, cnt
    print("-------------start to exec command-------------")

    client = connect(ip, 22, user, passwd)
    with SSHClient(client) as ssh_client:
        _, stdout, stderr = ssh_client.exec_command(cmd)
        # 防止IO太快（ValueError: I/O operation on closed file）
        time.sleep(1)
        with stdout:
            res = stdout.read().decode().strip()
            if res != "" or res is not None:
                with lock:
                    cnt += 1
                    print(res)
                    print(f"finished cmd on {ip}, total:{cnt} \n")
            else:
                with stderr:
                    print(stderr.read().decode())

    print("-------------end-------------")


def ec_curry(ip):
    # command = ""
    return exec_command(command, user_name, user_passwd, ip)


if __name__ == '__main__':

    with open("./resources/IPs.txt", "r", encoding="utf-8") as ifile:
        IPs = ifile.readlines()
    IPs = list(map(str.strip, IPs))

    with open("./resources/commands.txt", "r", encoding="utf-8") as cfile:
        command = cfile.read()

    lock = Lock()
    cnt = 0
    with ThreadPoolExecutor as tp:
        tasks = []
        for ip in tqdm(IPs, desc="traverse IP list"):
            tasks.append(tp.submit(ec_curry, ip))

    for fut in tqdm(as_completed(tasks), desc="get result") :
        ans = fut.result()
        print(f"{ans} \n")

