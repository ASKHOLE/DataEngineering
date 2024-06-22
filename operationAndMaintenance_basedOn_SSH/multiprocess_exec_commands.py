from multiprocessing import Pool, Lock, Value

from utils.ssh_client import SSHClient, connect


user_name = ""
user_passwd = ""
command = ""

lock = Lock()
cnt = Value("i", 0, lock=True)

def exec_command(cmd, user, passwd, ip):
    global lock, cnt
    print("-------------start to exec command-------------")

    client = connect(ip, 22, user, passwd)
    with SSHClient(client) as ssh_client:
        _, stdout, stderr = ssh_client.exec_command(cmd)
        with stdout:
            res = stdout.read().decode().strip()
            if res != "" or res is not None:
                with lock:
                    cnt.value += 1
                print(res)
                print(f"finished cmd on {ip}, total:{cnt.value} \n")
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

    with Pool(10) as pool:
        pool.map(ec_curry, IPs)


