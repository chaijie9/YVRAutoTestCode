COMMON_CONFIG = {
    # 通用目录配置
    'log_dir': './LOG',
    'tomb_dir': './tomb',
    'archive_dir': './Test_Results',  # 本地归档目录
    # 网络共享目录（如不可用会在脚本里自动降级为本地保存）
    'network_share': r'\\192.168.9.247\share\测试\aaa_cj\长跑测试记录',
    # 钉钉机器人 Webhook
    'dingtalk_webhook': 'https://oapi.dingtalk.com/robot/send?access_token=ac6710a1ccc6f62d22e0cd8aa690986f5cf3afb2064f60e63c7a4b832d64b622',
}


REBOOT_CONFIG = {
    **COMMON_CONFIG,
    # 设备信息（重启场景）
    'device_sn': '-s 192.168.8.103:5555',   # 设备序列号
    'device_id': '192.168.8.103:5555',      # 设备ID
    # 结果 Excel
    'excel_file': './reboot_D3_RC_4.1.0.1428+0.4.97R_OnlyHand.xlsx',
    # 时序参数
    'sleep_duration': 65,   # 重启后等待时长(秒)
    'wake_delay': 5,        # 预留延时(秒)
    'interval': 2,          # 测试间隔(秒)
    'max_iterations': 500,  # 最大测试次数 (0表示无限)
}


SLEEP_CONFIG = {
    **COMMON_CONFIG,
    # 设备信息（休眠唤醒场景）
    'device_sn': '-s 192.168.8.108:5555',   # 设备序列号
    'device_id': '192.168.8.108:5555',      # 设备ID
    # 结果 Excel
    'excel_file': './sleep_D3_RC_4.2.0.152+0.4.101R_OnlyController.xlsx',
    # 时序参数
    'sleep_duration': 62,   # 休眠时长(秒)
    'wake_delay': 8,        # 唤醒后等待时间(秒)
    'interval': 5,          # 测试间隔(秒)
    'max_iterations': 1000, # 最大测试次数 (0表示无限)
}

