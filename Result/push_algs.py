import argparse
import os
import tempfile

adb_options = ''

def run_cmd(cmd: str):
    print(f'> {cmd}')
    ret = os.system(cmd)
    if ret != 0:
        print(f'\nRun command [{cmd}] failed: {ret}\n')
        return False
    return True


def check_algs_dir_valid(algs_dir: str):
    if not os.path.exists(algs_dir):
        return False
    
    required_files = [
        'bin',
        'adsp',
        'cdsp',
        'config/vendor',
        'config/backup',
        'config/data',
        'lib64',
        'lib32',
        'lib64/libalgs_master_core.so',
        'lib32/libalgs_master_core.so',
        'include/algs_basic_interface.h'
    ]
    required_files = [os.path.join(algs_dir, file) for file in required_files]
    for file in required_files:
        if not os.path.exists(file):
            print(f'required file {file} not found')
            return False
        
    return True


def root_device():
    print('\nRoot device\n')
    commands = [
        f'adb {adb_options} root',
        f'adb {adb_options} wait-for-device',
        f'adb {adb_options} remount',
        f'adb {adb_options} wait-for-device'
    ]
    for cmd in commands:
        if not run_cmd(cmd):
            return False
    return True
    
    
def do_push_algs(algs_dir: str):
    print(f'\nPush algs\n')
    commands = [
        f'adb {adb_options} push {algs_dir}/bin/. /vendor/bin/',
        f'adb {adb_options} push {algs_dir}/lib64/. /vendor/yvr/lib64/',
        f'adb {adb_options} push {algs_dir}/lib32/. /vendor/yvr/lib/',
        f'adb {adb_options} push {algs_dir}/cdsp/. /vendor/lib/rfsa/adsp/',
        f'adb {adb_options} push {algs_dir}/adsp/. /vendor/lib/rfsa/adsp/',
        f'adb {adb_options} push {algs_dir}/config/vendor/. /vendor/etc/yvr/',
        f'adb {adb_options} push {algs_dir}/config/backup/. /backup/',
        f'adb {adb_options} push {algs_dir}/config/data/. /data/misc/trackingservice/'
    ]
    for cmd in commands:
        if not run_cmd(cmd):
            return False
    return True


def smb_download_directory(remote_dir, local_dir):
    import importlib.util
    if importlib.util.find_spec('smbclient') is None:
        print('smbclient not found, please install it by `pip install smbclient`')
        return False
    
    print(f'Download {remote_dir} to {local_dir}')
        
    import smbclient
    import smbclient.path
    if not smbclient.path.exists(remote_dir):
        print(f'{remote_dir} not found')
        return False
    if not os.path.exists(local_dir):
        os.makedirs(local_dir, exist_ok=True)
    for root, dirs, files in smbclient.walk(remote_dir):
        for dir in dirs:
            remote_path = os.path.join(root, dir)
            local_path = os.path.join(local_dir, remote_path[len(remote_dir):].lstrip('/\\'))
            os.makedirs(local_path, exist_ok=True)
        for file in files:
            remote_path = os.path.join(root, file)
            local_path = os.path.join(local_dir, remote_path[len(remote_dir):].lstrip('/\\'))
            print('\rDownload {}\033[K'.format(local_path), end='')
            with smbclient.open_file(remote_path, mode='rb') as remote_file:
                with open(local_path, 'wb') as local_file:
                    local_file.write(remote_file.read())
                    
    print('\rDownload complete!\033[K')
    return True


def unzip_file(zip_file, dst_dir):
    import zipfile
    print(f'Unzip {zip_file} to {dst_dir}')
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(dst_dir)
    print(f'Unzip complete!')


def prepare_algs_dir(args):
    if args.algs_path is not None:
        if os.path.isdir(args.algs_path):
            return args.algs_path, False
        elif os.path.isfile(args.algs_path):
            tmp_dir = tempfile.mkdtemp(prefix="algs_", suffix=".tmp")
            unzip_file(args.algs_path, tmp_dir)
            return os.path.join(tmp_dir, 'algs'), True
        else:
            print(f'{args.algs_path} not found')
            return '', False
    else:
        smb_path = os.path.join(args.smb_base, args.algs_version)
        tmp_dir = tempfile.mkdtemp(prefix="algs_", suffix=".tmp")
        if smb_download_directory(smb_path[4:], tmp_dir):
            return tmp_dir, True
        else:
            print(f'Download {smb_path} failed')
            return '', False


def push_algs(algs_dir: str):
    if not check_algs_dir_valid(algs_dir):
        return False
    
    if not root_device():
        return False
        
    if not do_push_algs(algs_dir):
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description='推送算法库到设备')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--algs_path', type=str, help='算法库路径 (支持压缩包、文件夹)')
    group.add_argument('--algs_version', type=str, help='算法库版本号，从SMB服务器下载')
    parser.add_argument('--smb_base', type=str, default='smb://192.168.9.228/algs_master_release/release/d3_dev/2024-05-22/2024-05-22-17-23-49',
                        help='SMB服务器基础路径')
    parser.add_argument('--device', type=str, default='', help='设备SN号')
    
    args = parser.parse_args()
    
    global adb_options
    if args.device != '':
        adb_options = f'-s {args.device}'
        
    algs_dir, generated = prepare_algs_dir(args)
    if algs_dir == '':
        return False

    push_algs(algs_dir)

    if generated:
        import shutil
        try:
            print(f'Remove {algs_dir}')
            shutil.rmtree(algs_dir)
        except Exception as e:
            print(f'Failed to remove {algs_dir}: {e}')

if __name__ == "__main__":
    main()
