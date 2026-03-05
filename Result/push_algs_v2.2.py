import argparse
import glob
import os
import platform
import shutil
import smbclient
import smbclient.path

release_version = 'v2.1'

usage = '''%(prog)s [options] algs_path [algs_path ...]

  1. 推送SMB服务器中的算法库到设备（必须以 smb:// 开头）
  push_algs.py smb://192.168.9.228/a.tar.gz

  2. 依次推送多个算法库到设备
  push_algs.py /path/to/algs /path/to/algs.tar.gz

  3. 推送算法库到指定设备
  push_algs.py /path/to/algs --device 123456
'''
adb_options = ''
adb_command = "adb"

# 判断是否基于WSL下运行
if 'WSL_DISTRO_NAME' in os.environ:
    print('WSL环境')
    adb_command = "adb.exe"

def run_cmd_with_result(cmd: str):
    print(f'\n> {cmd}')
    ret = os.popen(cmd).read()  # 使用 os.popen 获取命令输出
    if ret == '':
        print(f'Run command [{cmd}] failed.')
        return False
    return ret.strip()  # 返回输出字符串并去除首尾空格

def run_cmd(cmd: str):
    print(f'\n> {cmd}')
    ret = os.system(cmd)
    if ret != 0:
        print(f'Run command [{cmd}] failed: {ret}')
        return False
    return True

def get_valid_algs_dir(algs_dir: str) -> str:
    """Search for a *_algs_release.json or *@ota.version file in the given directory and its subdirectories."""
    try:
        for root, _, files in os.walk(algs_dir):
            for file in files:
                if file.endswith('_algs_release.json') or file.endswith('@ota.version'):
                    return root
    except Exception as e:
        print(f"Error while scanning directories: {e}")
    
    return ''

# 获取产品型号
def get_device_model():
    model = run_cmd_with_result(f'{adb_command} {adb_options} shell getprop ro.product.odm.model')
    return model.strip()

def root_device():
    print('\nRoot设备')
    run_cmd(f' {adb_command} {adb_options} wait-for-device')
    run_cmd(f' {adb_command} {adb_options} shell setprop service.dev.mode 1')
    run_cmd(f' {adb_command} {adb_options} wait-for-device')
    run_cmd(f' {adb_command} {adb_options} remount')
    run_cmd(f' {adb_command} {adb_options} wait-for-device')
    return True


def push_dir(src_dir: str, dst_dir: str):
    if not os.path.isdir(src_dir):
        return True
    return run_cmd(f' {adb_command} {adb_options} push {src_dir}/. {dst_dir}')

def push_file(file_path: str, dst_dir: str):
    if not os.path.isfile(file_path):
        return True
    return run_cmd(f' {adb_command} {adb_options} push {file_path} {dst_dir}')

def do_push_algs(product_name: str, algs_dir: str):
    print(f'\n开始推送：{algs_dir}')

    # 根据 product_name 确定推送的目标目录
    if product_name == "YVR3":
        push_items = [
            (f'{algs_dir}/bin', '/vendor/bin'),
            (f'{algs_dir}/lib64', '/vendor/yvr/lib64'),
            (f'{algs_dir}/lib32', '/vendor/yvr/lib'),
            (f'{algs_dir}/cdsp', '/vendor/lib/rfsa/adsp'),
            (f'{algs_dir}/adsp', '/vendor/lib/rfsa/adsp'),
            (f'{algs_dir}/config/vendor', '/vendor/etc/yvr'),
            (f'{algs_dir}/config/backup', '/backup'),
            (f'{algs_dir}/config/data', '/data/misc/trackingservice')
        ]
        version_target_dir = "/vendor/etc/yvr"
    else:
        push_items = [
            (f'{algs_dir}/bin', '/system/bin'),
            (f'{algs_dir}/lib64', '/system/lib64'),
            (f'{algs_dir}/lib32', '/system/lib'),
            (f'{algs_dir}/cdsp', '/vendor/lib/rfsa/adsp'),
            (f'{algs_dir}/adsp', '/vendor/lib/rfsa/adsp'),
            (f'{algs_dir}/config/vendor', '/system/etc/yvr'),
            (f'{algs_dir}/config/backup', '/backup'),
            (f'{algs_dir}/config/data', '/data/misc/trackingservice')
        ]
        version_target_dir = "/system/etc/yvr"

    # 处理常规文件夹推送
    for src, dst in push_items:
        if not push_dir(src, dst):
            print(f'推送文件到设备失败，终止程序：{src} => {dst}')
            return False

    # 处理 *.version 文件推送
    version_files = glob.glob(f"{algs_dir}/*.version")
    for file_path in version_files:
        file_name = os.path.basename(file_path)
        dst_path = f"{version_target_dir}/"
        push_file(file_path, dst_path)

    return True

def smb_download_file(remote_path, local_path):
    print(f'\n下载文件：{remote_path} => {local_path}')

    with smbclient.open_file(remote_path, mode='rb', share_access='r') as remote_file:
        with open(local_path, 'wb') as local_file:
            local_file.write(remote_file.read())
    print('下载完成！')
    return True


def smb_download_directory(remote_path, local_path):
    print(f'\n下载SMB文件夹：{remote_path} => {local_path}')

    if not os.path.exists(local_path):
        os.makedirs(local_path, exist_ok=True)

    for root, dirs, files in smbclient.walk(remote_path):
        root = root.replace('\\', '/')
        for dir in dirs:
            remote_dir_path = os.path.join(root, dir)
            local_dir_path = os.path.join(local_path, remote_dir_path[len(remote_path):].lstrip('/\\'))
            os.makedirs(local_dir_path, exist_ok=True)
        for file in files:
            remote_file_path = os.path.join(root, file)
            local_file_path = os.path.join(local_path, remote_file_path[len(remote_path):].lstrip('/\\'))
            print('\r下载中 {}\033[K'.format(local_file_path), end='')
            with smbclient.open_file(remote_file_path, mode='rb', share_access='r') as remote_file:
                with open(local_file_path, 'wb') as local_file:
                    local_file.write(remote_file.read())
    print('\r下载完成！\033[K')
    return True


def extract_file(compressed_file, dst_dir):
    print(f'\n开始解压：{compressed_file} => {dst_dir}')
    try:
        if compressed_file.endswith('.tar.gz'):
            import tarfile
            with tarfile.open(compressed_file, 'r:gz') as tar_ref:
                tar_ref.extractall(dst_dir,filter="tar")
            print(f'解压完成!')
            return True
        elif compressed_file.endswith('.zip'):
            import zipfile
            with zipfile.ZipFile(compressed_file, 'r') as zip_ref:
                zip_ref.extractall(dst_dir,filter="tar")
            print(f'解压完成!')
            return True
        else:
            supported_exts = ['.zip', '.tar.gz']
            print(f'仅支持以下压缩格式：{supported_exts}')
            return False
    except Exception as e:
        print(f'解压文件失败 {compressed_file}: {e}')
        return False


def prepare_algs_dir(algs_path: str, outdir: str):
    import tempfile
    if len(outdir) > 0 and not os.path.exists(outdir):
        print(f'创建输出目录：{outdir}')
        os.makedirs(outdir, exist_ok=True)
    if algs_path.startswith('smb://'):
        smbclient.ClientConfig(username='alg_dataset', password='alg_dataset@2022')
        algs_path = algs_path[len('smb://'):]
        if smbclient.path.isdir(algs_path):
            tmp_dir = outdir if os.path.isdir(outdir) else tempfile.mkdtemp(prefix='algs.', suffix='.tmp')
            if smb_download_directory(algs_path, tmp_dir):
                return (True, tmp_dir)
            else:
                print(f'下载失败： {algs_path} => {tmp_dir}')
                return (False, tmp_dir)
        elif smbclient.path.isfile(algs_path):
            import pathlib
            filepath = pathlib.Path(algs_path)
            tmp_dir = outdir if os.path.isdir(outdir) else tempfile.mkdtemp(prefix='algs.', suffix='.tmp')
            tmp_file = os.path.join(tmp_dir, filepath.name)
            if not smb_download_file(algs_path, tmp_file):
                return (False, tmp_dir)
            if not extract_file(tmp_file, tmp_dir):
                return (False, tmp_dir)
            return (True, tmp_dir)
        else:
            print(f'SMB文件（夹）不存在：{algs_path}')
            return (False, '')
    else:
        if os.path.isdir(algs_path):
            return (True, '')
        elif os.path.isfile(algs_path):
            tmp_dir = outdir if os.path.isdir(outdir) else tempfile.mkdtemp(prefix='algs.', suffix='.tmp')
            if extract_file(algs_path, tmp_dir):
                return (True, tmp_dir)
            else:
                return (False, tmp_dir)
        else:
            print(f'本地文件（夹）不存在：{algs_path}')
            return (False, '')


def push_algs(product_name: str, algs_dir: str):
    # 根据 product_name 确定推送的目标目录
    if product_name == "YVR3":
        target_dir = "/vendor/etc/yvr"
    else:
        target_dir = "/system/etc/yvr"

    # 推送 *_algs_release.json 文件到指定目录
    for file in os.listdir(algs_dir):
        if file.endswith('_algs_release.json'):
            if not run_cmd(f' {adb_command} {adb_options} push {os.path.join(algs_dir, file)} {target_dir}'):
                return False
            break

    # 执行额外的推送操作
    if not do_push_algs(product_name, algs_dir):
        return False

    return True

def for_each_algs(args, func):
    success = True
    for path in args.algs_path:
        ok, tmp_dir = prepare_algs_dir(path, args.outdir)
        if ok:
            algs_dir = tmp_dir if tmp_dir != '' else path
            valid_algs_dir = get_valid_algs_dir(algs_dir)
            if valid_algs_dir == '':
                print(f'算法库路径不合法：{algs_dir}')
                success = False
            else:
                success = func(args, valid_algs_dir)
        else:
            success = False

        if tmp_dir != '' and args.outdir != tmp_dir:
            if not args.keep_tempdir:
                try:
                    print(f'\n删除临时文件夹 {tmp_dir}')
                    shutil.rmtree(tmp_dir)
                except Exception as e:
                    print(f'删除临时文件夹失败 {tmp_dir}: {e}')
            else:
                print(f'\n检测到 --keep_tempdir，保留临时文件夹 {tmp_dir}')

        if not success:
            break

    return success


def handle_sync_package(args, algs_dir):
    out_alg_dir = os.path.join(args.sync_dev_dir, 'TrackingService/external/algorithm/alg_master')
    if not os.path.isdir(out_alg_dir):
        print(f'开发路径不合法：{args.sync_dev_dir}')
        return False

    if not os.path.isfile(os.path.join(algs_dir, 'package_algs_release.json')):
        print(f'算法库路径不合法，必须是基础包：{algs_dir}')
        return False

def validate_algs_dir(algs_dir):
    if not os.path.isfile(os.path.join(algs_dir, 'package_algs_release.json')) and \
       not any(fname.endswith('@ota.version') for fname in os.listdir(algs_dir)):
        print(f'算法库路径不合法，必须是基础包：{algs_dir}')
        return False

    print(f'\n同步算法库：{algs_dir} => {out_alg_dir}')
    shutil.copytree(f'{algs_dir}/bin/', f'{out_alg_dir}/bin/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/include/', f'{out_alg_dir}/include/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/config/vendor/', f'{out_alg_dir}/config/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/lib64/', f'{out_alg_dir}/libs/lib64/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/lib32/', f'{out_alg_dir}/libs/lib32/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/adsp/', f'{out_alg_dir}/adsp/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/cdsp/', f'{out_alg_dir}/cdsp/', dirs_exist_ok=True)
    shutil.copyfile(f'{algs_dir}/package_algs_release.json', f'{out_alg_dir}/package_algs_release.json')
    print(f'同步算法库完成！')
    return True


def handle_sync_dev(args, algs_dir):
    out_alg_dir = 'TrackingService/external/algorithm/alg_master'
    if not os.path.isdir(out_alg_dir):
        print(f'请 cd 到 yvr 仓库根目录，再运行此脚本')
        return False

    print(f'\n同步算法库：{algs_dir} => {out_alg_dir}')
    shutil.copytree(f'{algs_dir}/bin/', f'{out_alg_dir}/bin/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/include/', f'{out_alg_dir}/include/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/config/vendor/', f'{out_alg_dir}/config/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/lib64/', f'{out_alg_dir}/libs/lib64/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/lib32/', f'{out_alg_dir}/libs/lib32/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/adsp/', f'{out_alg_dir}/adsp/', dirs_exist_ok=True)
    shutil.copytree(f'{algs_dir}/cdsp/', f'{out_alg_dir}/cdsp/', dirs_exist_ok=True)
    if os.path.isfile(f'{algs_dir}/package_algs_release.json'):
        shutil.copyfile(f'{algs_dir}/package_algs_release.json', f'{out_alg_dir}/package_algs_release.json')
    print(f'同步算法库完成！')
    return True


def handle_push_algs(args, algs_dir):
    if args.download_only:
        print(f'\n检测到 --download_only，跳过推送！')
        return True

    supported_devices = {
        "YVR 1": "YVR1",
        "YVR 2": "YVR2",
        "PFDM MR": "YVR3"
    }

    print(f'\n产品名称：{args.product_name}')
    device_model = get_device_model()
    if device_model not in supported_devices or supported_devices[device_model] != args.product_name:
        print(f'设备型号不在支持列表中或与产品名称不匹配，无法推送算法库，device_model: {device_model} product_name: {args.product_name}')
        return False

    if ('algs_package@d2' in algs_dir and args.product_name == 'YVR3') or ('algs_package@d3' in algs_dir and args.product_name != 'YVR3'):
        if 'algs_package@d2' in algs_dir:
            print(f'YVR2的算法包不允许推送到YVR3设备上！')
        else:
            print(f'YVR3的算法包不允许推送到YVR2设备上！')
        return False

    if not root_device():
        print(f'\nRoot设备失败！')
        return False

    return push_algs(args.product_name, algs_dir)


def main():
    parser = argparse.ArgumentParser(description=f'推送算法库到设备 {release_version}', usage=usage)
    parser.add_argument('algs_path', type=str, nargs='*', help='算法库路径（支持压缩包、文件夹、SMB路径）')
    parser.add_argument('--version', action='version', version=f'%(prog)s {release_version}')
    parser.add_argument('--device', type=str, default='', help='设备SN号（主机同时连接多个设备时很有用）')
    parser.add_argument('--keep_tempdir', action='store_true', help='保留临时文件夹（解压、SMB下载的临时文件夹）')
    parser.add_argument('--reboot', action='store_true', help='推送完成后重启设备')
    parser.add_argument('--download_only', action='store_true', help='仅下载，不安装')
    parser.add_argument('--outdir', type=str, default='', help='设置输出（解压、下载）目录')
    parser.add_argument('--dump_algs', action='store_true', help='输出算法库清单内容')
    parser.add_argument('--sync_dev_dir', type=str, default='', help='同步算法库到开发目录（用于算法发布）')
    parser.add_argument('--dev', action='store_true', help='同步算法库到开发目录，支持patch包（用于开发）')
    parser.add_argument('--product_name', type=str, default='YVR3', help='选择"YVR1/YVR2/YVR3"')
    args = parser.parse_args()

    global adb_options
    if args.device != '':
        adb_options = f'-s {args.device}'

    if len(args.algs_path) > 0:
        pass
    elif args.dump_algs:
        run_cmd(f' {adb_command} {adb_options} shell cat /vendor/etc/yvr/package_algs_release.json')
        return True
    else:
        parser.print_help()
        return False

    if args.sync_dev_dir != '':
        for_each_algs(args, handle_sync_package)
    elif args.dev:
        for_each_algs(args, handle_sync_dev)
    else:
        success = for_each_algs(args, handle_push_algs)
        if success:
            if args.reboot:
                print('\n重启设备')
                run_cmd(f' {adb_command} {adb_options} reboot')
                run_cmd(f' {adb_command} {adb_options} wait-for-device')
            if args.dump_algs:
                run_cmd(f' {adb_command} {adb_options} shell cat /vendor/etc/yvr/package_algs_release.json')
        else:
            print('\n推送算法库失败!')


if __name__ == '__main__':
    main()
