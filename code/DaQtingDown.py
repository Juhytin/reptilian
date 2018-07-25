# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys,re

class downloader(object):

    def __init__(self):
        self.target = 'http://www.luoxia.com/daqing'
        self.names = []            #存放章节名
        self.urls = []            #存放章节链接
        self.nums = 0            #章节数
    def get_download_url(self):
        req = requests.get(url = self.target)
        req.encoding='utf-8'
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', class_ = 'book-list clearfix')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        
        for each in a:
            self.names.append(each.string)
            self.urls.append(each.get('href'))
        b = a_bf.find_all('b')
        for each in b:
            self.names.append(each.string)
            url =re.match('^window.open.*(http.*htm)',each.get('onclick'))
            self.urls.append(url.group(1))
        self.nums = len(a) + len(b)                                #统计章节数
    def get_contents(self, target):
        req = requests.get(url = target)
        req.encoding='utf-8'
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', id = 'nr1')
        texts = texts[0].text
        return texts
    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')
if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('《大清相国》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '大清相国.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" %  float(i/dl.nums) + '\n')
        sys.stdout.flush()
    print('《大清相国》下载完成')
