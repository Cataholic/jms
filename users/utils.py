import os
import subprocess
import pwd


class Bash:
    def __init__(self):
        self.ret = None

    def excute(self, command):
        self.ret = subprocess.Popen('{}'.format(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.ret.wait()
        print(self.ret.stderr.read())

    @property
    def stdout(self):
        return self.ret.stdout.read()

    @property
    def stderr(self):
        return self.ret.stderr.read()

    @property
    def code(self):
        return self.ret.returncode


class ServerUserManager:
    def __init__(self, sh):
        self.sh = sh()

    def present(self, username='', password='', shell='/bin/bash'):
        com_add = 'id {username} || useradd {username} -s {shell}'.format(username=username, shell=shell)
        self.sh.excute(com_add)

        if self.sh.code != 0:
            return [1, '添加用户失败']

        if password:
            com_password = 'echo {password} | passwd --stdin {username}'.format(username=username, password=password)
            self.sh.excute(com_password)
            if self.sh.code != 0:
                return [1, '修改用户密码失败']
        return [0, '添加用户成功']

    def absent(self, username, force=False):
        if not self.check_user_exist(username):
            return [0, '用户不存在']

        cmd = ['userdel {}'.format(username)]
        if force:
            cmd.append('--force -r')

        self.sh.excute(cmd)
        if self.sh.code != 0:
            return [1, '移除用户失败']
        else:
            return [0, '移除用户成功']

    def check_user_exist(self, username):
        cmd = 'id {}'.format(username)
        self.sh.excute(cmd)

        if self.sh.code == 0:
            return True
        else:
            return False

    def ssh_key_gen(self, username, ssh_dir, ssh_type='rsa', ssh_key_name='id_rsa', force=False, passphrase=''):
        uid, gid = self.get_user_ug_id(username)
        if not os.path.exists(ssh_dir):
            try:
                os.makedirs(ssh_dir, 0o700)
                os.chown(ssh_dir, uid, gid)
            except OSError as e:
                return [1, '创建目录{}失败{}'.format(ssh_dir, str(e))]

        ssh_key_file = os.path.join(ssh_dir, ssh_key_name)
        if os.path.isfile(ssh_key_file) and not force:
            return [0, '用户key已存在{}'.format(ssh_key_file)]

        cmd = 'ssh-keygen -t {} -f {} -N "{}"'.format(ssh_type, ssh_key_file, passphrase)
        self.sh.excute(cmd)
        if self.sh.code != 0:
            return [1, 'SSH Key生成失败 {}'.format(self.sh.stderr)]
        else:
            return [0, 'SSH Key生成成功']

    @staticmethod
    def get_user_ug_id(username):
        uid = pwd.getpwnam(username).pw_uid
        gid = pwd.getpwnam(username).pw_gid
        return uid, gid
