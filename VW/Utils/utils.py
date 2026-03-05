import base64
from os import environ
from sys import stdout
from datetime import datetime, date, timedelta
from random import randint, uniform, choices
import pathlib
import hashlib
import uuid
import yaml
import time
import json
import re


# 计算acw_sc__v2 cookie值
def calculate_acw_sc__v2(waf_text: str, c1: str = '4e7c9bda13f58602', prefix: str = '197d84838') -> str | None:
  match = re.search(r"var arg1='([a-f0-9]+)'", waf_text)
  if match:
    arg1 = match.group(1)
  else:
    return None
  try:
    e = list(arg1[:40])
    b = (len(e) + 7) // 8
    _e = [e[j * b + i] for i in range(b) for j in range(8) if j * b + i < len(e)]
    acw_sc__v2 = ''.join([c1[int(c, 16)] for c in _e])
    r_str = ''.join(choices('0123456789abcdef', k=10))
    return f"{prefix}-{acw_sc__v2}{r_str}"
  except Exception as e:
    print(f'Cookie计算失败: {e}')
    return None


# 生成时间戳
def create_timestamp(figure: int = 10) -> str:
  timestamp = time.time()
  power = figure - 10
  return str(int(timestamp * (10 ** power)))


# 获取uuid
def create_uuid(ver: str = 'v4', namespace: uuid.UUID = uuid.UUID, name: str = '') -> str:
  if ver == 'v4':
    return str(uuid.uuid4())
  elif ver == 'v3':
    return str(uuid.uuid3(namespace, name))
  elif ver == 'v5':
    return str(uuid.uuid5(namespace, name))
  else:
    return ''


# 读取yaml文件
def read_yaml(path: str = 'config.yaml') -> dict:
  with open(pathlib.Path(path), 'rb') as stream:
    return yaml.safe_load(stream)


# 解析 JWT 的 payload 部分
def decode_jwt_payload(token: str) -> dict | None:
  if not token:
    return None
  try:
    parts = token.split('.')
    if len(parts) != 3:
      return None
    payload_b64 = parts[1]
    # 补全 base64 padding
    payload_b64 += '=' * (4 - len(payload_b64) % 4)
    # URL-safe base64 解码
    payload_b64 = payload_b64.replace('-', '+').replace('_', '/')
    payload_json = base64.b64decode(payload_b64)
    return json.loads(payload_json)
  except Exception:
    return None


# 去除 HTML 标签
def strip_html_tags(html: str) -> str:
  if not html:
    return ""
  return re.sub(r'<[^>]+>', '', html).strip()