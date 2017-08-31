# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

URL = 'http://dict.cn/'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)

DEFAULT_ITEM = {
        'Title': "not found",
        'IcoPath': os.path.join('img', 'dict.png')
    }

class Main(Wox):
  
    def request(self,url):
	#get system proxy if exists
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
	    proxies = {
		"http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
		"https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
	    }
	    return requests.get(url,proxies = proxies)
	return requests.get(url)
			
    def query(self, param):
        if not param:
            return [DEFAULT_ITEM]
	r = self.request(URL + param)
	bs = BeautifulSoup(r.content, 'html.parser')

        if not bs.find('ul', class_="dict-basic-ul"):
            return [DEFAULT_ITEM]
        means = bs.find('ul', class_="dict-basic-ul").find_all('li')
        result = []
	for m in means:
            if not m.find('span') or not m.find('strong'):
                continue
            item = {
                'Title': full2half(m.find('span').text + ": " + m.find('strong').text),
                'IcoPath': os.path.join('img', 'dict.png'),
                'JsonRPCAction': {
                        'method': 'open_url',
                        'parameters': [URL + param]
                }
            }
            result.append(item)
            
	return result
    
    def open_url(self, url):
	webbrowser.open(url) #use default browser

if __name__ == '__main__':
    Main()
