import paramiko

class SSHClient:
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def exec_command(self, cmd):
        try:
            _, stdout, stderr = self.ssh_client.exec_command(cmd)
        except Exception as e:
            print(f"Error executing command {cmd}: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ssh_client.close()

def connect(host, port, user_name, user_passwd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh_client.load_system_host_keys()
        ssh_client.connect(host, port, user_name, user_passwd, timeout=5)
    except paramiko.AuthenticationException:
        raise Exception(f"主机 {host} 连接失败，请检查参数！")
    except paramiko.BadHostKeyException as e:
        raise Exception(f"主机 {host} 验证不通过：{e}")
    except paramiko.SSHException as e:
        raise Exception(f"主机 {host} 连接出错：{e}")
    except Exception as e:
        raise Exception(f"主机 {host} 连接超时：{e}")

    return ssh_client