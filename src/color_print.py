from colorama import init, Fore, Back, Style
import colorama
import time

G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

colorama.init()


class Colored(object):
    # 前景色:红色 背景色:默认
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET

    # 前景色:绿色 背景色:默认
    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    # 前景色:黄色 背景色:默认
    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    # 前景色:蓝色 背景色:默认
    def blue(self, s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET

    # 前景色:白色 背景色:默认
    def white(self,s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    # 前景色:洋红色 背景色:默认
    def magenta(self, s):
        return Fore.LIGHTMAGENTA_EX + s + Fore.RESET

    # 前景色:青色 背景色:默认
    def cyan(self, s):
        return Fore.LIGHTCYAN_EX + s + Fore.RESET


color = Colored()


def print_blue_white(info):
    print(
        B 
        + time.strftime("%Y-%m-%d")
        + ' '
        + time.strftime("%H:%M:%S")
        + W)

def print_flush(info):
    print(
        color.white("[")
        + color.blue(time.strftime("%H:%M:%S"))
        + color.white("]")
        + color.white("[")
        + color.green("INFO")
        + color.white("] ")
        + info, end="\r", flush=True
    )



def print_flush_two(info):
    print(
        "\r",
        color.white("[")
        + color.blue(time.strftime("%H:%M:%S"))
        + color.white("]")
        + color.white("[")
        + color.green("INFO")
        + color.white("] ")
        + info, end=""
    )


def print_info(info):
    print(
        B 
        + time.strftime("%Y-%m-%d")
        + ' '
        + time.strftime("%H:%M:%S")
        + W
        + color.white(" [")
        + color.green("INFOR")
        + color.white("]")
        + color.white(' - ')
        + color.green(info)
    )


def print_error(info):
    print(
        B 
        + time.strftime("%Y-%m-%d")
        + ' '
        + time.strftime("%H:%M:%S")
        + W
        + color.white(" [")
        + color.red("ERROR")
        + color.white("]")
        + color.white(' - ')
        + color.red(info)
    )


def print_warn(info):
    print(
        B 
        + time.strftime("%Y-%m-%d")
        + ' '
        + time.strftime("%H:%M:%S")
        + W
        + color.white(" [")
        + color.yellow("ALTER")
        + color.white("]")
        + color.white(' - ')
        + color.yellow(info)
    )


def print_msg():
    msg1 = '''   ____  _   ____  _                    _ 
  / ___|/ | / ___|| |  ___   _   _   __| |		Author: CMACCKK'''
    msg2 = ''' | |    | || |    | | / _ \\ | | | | / _` |		Version: 0.1
 | |___ | || |___ | || (_) || |_| || (_| |		Email: emailforgty@163.com'''

    msg3 = '''  \\____||_| \\____||_| \\___/  \\__,_| \\__,_|
    '''
    print(color.yellow(msg1))
    print(color.green(msg2))
    print(color.cyan(msg3))
