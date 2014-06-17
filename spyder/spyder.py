#coding: utf-8
import os
import Queue
import requests
import requests as rq
import threading as thd
import parser as par

import sys
def monkey_patch():
    prop = requests.models.Response.content
    def content(self):
        _content = prop.fget(self)
        if self.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(_content)
            if encodings:
                self.encoding = encodings[0]
            else:
                self.encoding = self.apparent_encoding
            _content = _content.decode(self.encoding, 'replace').encode('utf8', 'replace')
            self._content = _content
        return _content
    requests.models.Response.content = property(content)
monkey_patch()

class Spyder(object):

    def __init__(self, re_queue):
        # queue to store the responds content
        self.r_q = re_queue

        self.time_out = 5
        self.url_base = "http://www.ijita.com/tab/{}.html"   


        # how much page you want to get
        self.page_num = 6825

        # page queue
        self.queue = Queue.Queue()

        self.thd_pool = []
        self.thd_num = 10

    def __put(self):
        """
        put works to queue
        """
        for i in range(self.page_num):
            page_index = i+1
            url = self.url_base.format(page_index)
            self.queue.put((url, page_index))

    def __get(self):
        while not self.queue.empty():
            url, page_index = self.queue.get()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}  
            try:
                responce = rq.get(url, timeout=self.time_out, headers=headers)
            except:# rq.Timeout:
                print "TIMEOUT page {}".format(page_index)
                continue
            self.r_q.put(responce.text)

    def __creat_thd(self):
        """
        add thread to thread pool
        """
        for i in range(self.thd_num):
            thd_ = thd.Thread(target=self.__get)
            self.thd_pool.append(thd_)

    def run(self):
        self.__put()
        self.__creat_thd()

        for thd_ in self.thd_pool:
            thd_.start()

    def is_over(self):
        """
        is all jobs done?
        """
        undone = filter(lambda t: t.isAlive(), self.thd_pool)
        if not undone:
            return True
        else:
            return False

if __name__ == "__main__":
    q= Queue.Queue()
    s=Spyder(q)
    s.run()
    
        
