import paramiko

class SFTPClient:

    def __init__(self, host, port, user_name, password):
        self.transport = paramiko.Transport((host, port))
        self.transport.connect(username=user_name, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def uploader(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    def downloader(self, remote_path, local_path):
        self.sftp.get(remote_path, local_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sftp.close()
        self.transport.close()
