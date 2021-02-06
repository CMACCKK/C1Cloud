from prettytable import PrettyTable
import os
from src.color_print import *


def read_file(path):
    l = []
    try:
        content = open(path, 'r').readlines()
        for i in content:
            l.append(i.strip())
        return l
    except:
        return 


def get_oneforall_info(info):
    l = []
    # table = PrettyTable(['Subdomain', 'IP' ,'org', 'addr', 'isp', 'source'])
    for i in info:
        tmp = i.strip().split(',')
        l.append(tmp[5])
    result = set(l)
    return_list = list(result)
    return return_list


def table_print(l):
    table = PrettyTable(['subdomain'])
    for i in l:
        table.add_row([i.strip()])
    return table


def judge_file_delete(path):
    if not os.path.exists(path):
        pass
    else:
        os.remove(path=path)
        print_info('删除{PATH}'.format(PATH=path))


def get_url(info):
    tmp1 = info.replace('GET ', '')
    tmp2 = tmp1.replace('POST ', '')
    return tmp2