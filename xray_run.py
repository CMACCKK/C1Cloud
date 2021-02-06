import subprocess
from src.config import *


cmd = ["./xray_linux_amd64", 'webscan', '--listen', XRAY_LISTEN, '--webhook-output', WEBHOOK]
rsp = subprocess.Popen(cmd)
rsp.communicate()