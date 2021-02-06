from src.config import *
from src.color_print import *
from multiprocessing import Queue, Pool
from tqdm import tqdm
from src.get_user_agent import *
from src.read_file import *
import subprocess
from pprint import pprint
from prettytable import PrettyTable
import requests
import json
import os


def judge_file_delete(path):
    if not os.path.exists(path):
        pass
    else:
        os.remove(path=path)
        print_info('删除{PATH}'.format(PATH=path))


def deal_url_dict(dict1, dict2):
    dict3 = {}
    dict4 = {}
    for k1, v1 in dict1.items():
        if k1.endswith('/'):
            dict3[k1[:-1]] = v1
        else:
            dict3[k1] = v1
    for k2, v2 in dict2.items():
        if k2.endswith('/'):
            dict4[k2[:-1]] = v2
        else:
            dict4[k2] = v2
    all_url_dict = dict3.copy()
    all_url_dict.update(dict4)
    return all_url_dict


def get_rad_dict(FILE):
    rad_dict = {}
    f = open(FILE, 'r').read()
    tmp = json.loads(f)
    for i in tmp:
        rad_dict[i['URL']] = i['Method']
    return rad_dict


def get_crawlergo_dir(file):
    crawlergo_dict = {}
    f = open(file, 'r').readlines()[0]
    tmp = json.loads(f)
    for i in tmp['all_req_list']:
        if i['url'].startswith('/'):
            pass
        else:
            crawlergo_dict[i['url']] = i['method']

    return crawlergo_dict


def rad_crawl(target):
    JSON_OUT = './output/' + target.replace('.', '_').replace('http://', '').replace('https://', '') + '_rad.json'
    judge_file_delete(JSON_OUT)
    CMD_STR = "./rad_linux_amd64 --target {TARGET} --json-output {JSON_OUT}".format(TARGET=target, JSON_OUT=JSON_OUT)
    print_info('使用Rad扫描  Command: ' + color.yellow(CMD_STR))
    CMD = CMD_STR.split(' ')
    rsp = subprocess.Popen(CMD)
    rsp.communicate()
    rad_dict = get_rad_dict(FILE=JSON_OUT)
    return rad_dict


def crawlergo_crawl(target):
    CRAWLERGO_OUTPUT_JSON = './output/' + target.replace('.', '_').replace('http://', '').replace('https://',
                                                                                                  '') + '_crawlergo.json'
    judge_file_delete(CRAWLERGO_OUTPUT_JSON)
    print_info('使用CrawLergo扫描')
    cmd = ["./crawlergo", "-c", CHROME_PATH, "-t", CRAWLERGO_THREADS, "--robots-path", "--fuzz-path",
           "--custom-headers", json.dumps(get_user_agent()), "--output-json", CRAWLERGO_OUTPUT_JSON, target]
    rsp = subprocess.Popen(cmd)
    rsp.communicate()
    result = get_crawlergo_dir(file=CRAWLERGO_OUTPUT_JSON)
    return result


def xray_scan(TARGET):
    CMD_STR = './xray_linux_amd64 webscan --basic-crawler {TARGET} --webhook-output {WEBHOOK}'.format(TARGET=TARGET,
                                                                                                      WEBHOOK=WEBHOOK)
    print_info('使用Xray扫描  Command: ' + color.yellow(CMD_STR))
    CMD = CMD_STR.split(' ')
    rsp = subprocess.Popen(CMD)
    rsp.communicate()


def request_get_url(pool_get_url):  # 判断url是否可以访问
    try:
        r = requests.request(method='GET', url=pool_get_url, headers=get_user_agent(), timeout=(3, 7)).status_code
        if r == 200:
            return 1, pool_get_url
        else:
            return 0, pool_get_url
    except:
        return 0, pool_get_url


def request_post_url(pool_post_url):  # 判断url是否可以访问
    try:
        r = requests.request(method='POST', url=pool_post_url, headers=get_user_agent(), timeout=(3, 7)).status_code
        if r == 200:
            return 1, pool_post_url
        else:
            return 0, pool_post_url
    except:
        return 0, pool_post_url


def judge_get_addressable_url(sub_list):  # 判断GET可访问的域名
    scan_url_list = []
    alive_url = []
    for line in sub_list:
        if line.startswith('https://'):
            tmp_url = line.replace('https://', 'http://')
        elif line.startswith('http://'):
            tmp_url = line
        else:
            tmp_url = 'http://' + line
        scan_url_list.append(tmp_url)
    # print(scan_url_list)
    thread_count = 10
    print_info('使用 ' + str(thread_count) + ' 线程')
    with Pool(10) as p:
        pool_result = list(tqdm(p.imap(request_get_url, scan_url_list), total=len(scan_url_list)))
    for result in pool_result:
        if result[0] == 1:
            alive_url.append(str(result[1]).replace('http://', ''))
    return alive_url


def judge_post_addressable_url(sub_list):  # 判断POST可访问的域名
    scan_url_list = []
    alive_url = []
    for line in sub_list:
        if line.startswith('https://'):
            tmp_url = line.replace('https://', 'http://')
        elif line.startswith('http://'):
            tmp_url = line
        else:
            tmp_url = 'http://' + line
        scan_url_list.append(tmp_url)
    # print(scan_url_list)
    thread_count = 5
    print_info('使用 ' + str(thread_count) + ' 线程')
    with Pool(10) as p:
        pool_result = list(tqdm(p.imap(request_post_url, scan_url_list), total=len(scan_url_list)))
    for result in pool_result:
        if result[0] == 1:
            alive_url.append(str(result[1]).replace('http://', ''))
    return alive_url


def oneforall():
    CMD_STR = "python3 ./OneForAll/oneforall.py --targets ./target.txt --path={ONEFORALL_OUTPUT_PATH} run".format(
        ONEFORALL_OUTPUT_PATH=ONEFORALL_OUTPUT_PATH)
    print_info('使用OneForAll扫描  Command: ' + color.yellow(CMD_STR))
    CMD = CMD_STR.split(' ')
    rsp = subprocess.Popen(CMD)
    rsp.communicate()


def get_oneforall_info(info):  # 对oneforall查询到的子域名去重
    l = []
    for i in info:
        tmp = i.strip().split(',')
        l.append(tmp[5])
    result = set(l)
    return_list = list(result)
    return return_list


def jsfinder(jsfinder_url):
    TMP_JSFIND_OUT = jsfinder_url.replace('http://', '').replace('https://', '').replace('.', '_')
    JSFIND_OUT = './output/' + TMP_JSFIND_OUT.replace('/', '_')
    judge_file_delete(JSFIND_OUT)
    cmd = ['python3', 'JSFinder.py', '-u', jsfinder_url, '-ou', JSFIND_OUT]
    rsp = subprocess.Popen(cmd)
    rsp.communicate()
    bool_js = judge_file_empty(file=JSFIND_OUT)
    if bool_js:
        return False
    else:
        result = read_file(JSFIND_OUT)
        judge_file_delete(JSFIND_OUT)
    return result


def judge_file_empty(file):
    if os.path.getsize(file) == 0:
        return True
    else:
        return False


def detect_url(target, url_list):  # 清除crawlergo的中扫描到的不属于目标子域名的url
    result = []
    for url in url_list:
        if target in url:
            result.append(url)
    return result


def use_jsfinder(url_dict):
    jsfinder_url_dict = {}
    for url in list(url_dict.keys()):
        try:
            print_info('jsfinder扫描' + color.yellow(url))
            tmp_jsfinder_url = jsfinder(url)
            if not tmp_jsfinder_url:
                pass
            else:
                for i in tmp_jsfinder_url:
                    jsfinder_url_dict[i] = 'GET'
        except:
            print_error('无法使用JSFinder访问' + url)
    return jsfinder_url_dict


def get_subdomain():
    subdomain = []
    oneforall()  # Oneforall扫描
    info = read_file('./output/oneforall.txt')
    oneforall_url = get_oneforall_info(info)  # 子域名列表
    alive_url = judge_get_addressable_url(oneforall_url)
    for subdomain_url in alive_url:
        subdomain.append(subdomain_url)
    return subdomain


def suffix_judge(url_dict):
    for key in list(url_dict.keys()):
        for suffix in UNSCAN_SUFFIX:
            if suffix in key:
                try:
                    url_dict.pop(key)
                except:
                    pass
                continue
    return url_dict


def judge_url_subdomain(url_dict, subdomain):
    for url in list(url_dict.keys()):
        if subdomain not in url:
            url_dict.pop(url)
    return url_dict


def url_trans(url):
    if url.startswith('https://'):
        tmp_url = url.replace('https://', 'http://')
    elif url.startswith('http://'):
        tmp_url = url.replace('http://', '')
    else:
        tmp_url = url
    return tmp_url


def xray_listen(result_url_dict):
    for TMP_URL, ACCESS_TYPE in result_url_dict.items():
        URL = 'http://' + TMP_URL
        if ACCESS_TYPE == 'GET':
            try:
                requests.get(url=URL, headers=get_user_agent(), proxies=proxies, timeout=30,
                             verify=False)  # 想使用xray --listen参数取消注释
                print_info('Send ' + color.yellow(URL))
            except:
                print_error(URL + '无法发送 请检查xray是否正在监听端口')
        elif ACCESS_TYPE == 'POST':
            try:
                requests.post(url=URL, headers=get_user_agent(), proxies=proxies, timeout=30,
                              verify=False)  # 想使用xray --listen参数取消注释
                print_info('Send ' + color.yellow(URL))
            except:
                print_error(URL + '无法发送 请检查xray是否正在监听端口')

        else:
            pass


def xray_basic_crawl(result_url_dict):
    for TMP_URL, ACCESS_TYPE in result_url_dict.items():
        URL = 'http://' + TMP_URL
        xray_scan(URL)


if __name__ == '__main__':
    post_url_list = []
    get_url_list = []
    result_url_dict = {}
    new_url_dict = {}
    alive_subdomain_table = PrettyTable(['可访问的子域名'])
    print_msg()
    TARGET_LIST = get_subdomain()
    for sub in TARGET_LIST:
        alive_subdomain_table.add_row([sub])
    print(alive_subdomain_table)
    for TARGET in TARGET_LIST:  # 根据子域名扫描URL
        print_info('rad扫描' + color.yellow(TARGET))
        rad_dict = rad_crawl(TARGET)
        print_info('rad扫描完成')
        # print(rad_dict)
        try:
            craw_dict = crawlergo_crawl(TARGET)
            print_info('crawlergo扫描完成')
        except:
            craw_dict = {}
            print_error('请检查src目录下的config.py文件中的CHROME_PATH变量')
        rad_crawlergo_url_dict = deal_url_dict(dict1=rad_dict, dict2=craw_dict)
        print_info('去除不需要扫描的url后缀')
        tmp_deal_dict = suffix_judge(rad_crawlergo_url_dict)
        print_info('判断是否为子域名url')
        judge_url_dict = judge_url_subdomain(tmp_deal_dict, TARGET)
        print_info('使用JSFinder')
        tmp_jsfinder_dict = use_jsfinder(judge_url_dict)
        print_info('去除不需要扫描的url后缀')
        jsfinder_dict = suffix_judge(tmp_jsfinder_dict)
        print_info('url字典合并去重')
        tmp_url_dict = deal_url_dict(dict1=judge_url_dict, dict2=jsfinder_dict)
        print_info('多线程判断url是否可访问')
        url_dict = judge_url_subdomain(tmp_url_dict, TARGET)
        # print(url_dict)
        for k, v in url_dict.items():
            new_url_dict[url_trans(k)] = v
        # print(new_url_dict)
        print_info('url可访问判断完成')
        for url, acc_type in new_url_dict.items():
            if acc_type == 'GET':
                get_url_list.append(url)
            elif acc_type == 'POST':
                post_url_list.append(url)
            else:
                get_url_list.append(url)
        print_info('使用GET请求访问url')
        addressable_get_url_list = judge_get_addressable_url(get_url_list)
        print_info('使用POST请求访问url')
        addressable_post_url_list = judge_post_addressable_url(post_url_list)
        # pprint(addressable_get_url_list)
        # pprint(addressable_post_url_list)
        for url_get in addressable_get_url_list:
            result_url_dict[url_get] = new_url_dict[url_get]
        for url_post in addressable_post_url_list:
            result_url_dict[url_post] = new_url_dict[url_post]
        xray_listen(result_url_dict=result_url_dict)
        # xray_basic_crawl(result_url_dict=result_url_dict)
