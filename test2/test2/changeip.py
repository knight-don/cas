# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:05:59 2018

@author: Administrator
"""
import re
from urllib import request
#import requests
#import random



    
def save_proxy_in_file():

    
    url = "http://tvp.daxiangdaili.com/ip/?tid=XXXXXXX&num=10&protocol=https&category=2"
    a = request.Request(url)
    page_of_daxiangdaili = request.urlopen(a).read().decode()
    #print(page_of_daxiangdaili)
#    proxy_list = []
    ip_list = re.findall(r'(\d+.\d+.\d+.\d+:\d+)', page_of_daxiangdaili)#\d表示匹配的是数字+表示重复一次或者多次
    #print(ip_list)
    #port_list = re.findall(r'<td>\d+</td>', first_page)
    ##    print(port_list)
    #for i in range(len(ip_list)):
    #    ip = ip_list[i]
    #    port = re.sub(r'<td>|</td>', '', port_list[i])
    #    proxy = '{}:{}'.format(ip, port)
    #    proxy_list.append(proxy)
    

#    测试可用性
    #for i in ip_list:
    #    proxies = {"http": "http://" + str(i),}
    ##    proxy_ip = {'http':'http://{}'.format(proxy_ip)}
    #    
    #    print(proxies)
    #    url1 = 'http://httpbin.org/ip'
    #    b = requests.get(url = url1, headers = headers, proxies=proxies).text
    #    print(b)


    #proxies = []
    for iii in ip_list:
    #    print(iii)
    #    proxies= {"proxy": "http://" + str(i), "valid":"true", "count":"0"}
        with open('F:///spiders/ip.txt', 'a') as f:
            f.write('http://' + str(iii) + '\n')
    
    #    proxy_ip = {'https':'http://{}'.format(proxy_ip)}

def save_proxy_in_list():

    
    url = "http://tvp.daxiangdaili.com/ip/?tid=XXXXXXX&num=10&protocol=https&category=2"
    a = request.Request(url)
    page_of_daxiangdaili = request.urlopen(a).read().decode()
    #print(page_of_daxiangdaili)
#    proxy_list = []
    ip_list = re.findall(r'(\d+.\d+.\d+.\d+:\d+)', page_of_daxiangdaili)#\d表示匹配的是数字+表示重复一次或者多次
    proxies = []
    for iii in ip_list:
    #    print(iii)
        proxies.append("http://" + str(iii))
#        print(proxies)
    return(proxies)
    
    
if __name__ == '__main__':
    save_proxy_in_file()
#    save_proxy_in_list()

  