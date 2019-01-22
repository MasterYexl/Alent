import urllib.parse, urllib.request, re, requests, time
from bs4 import BeautifulSoup

header = {'Connection': 'keep-alive',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
          }


class Parser:

    def __init__(self, href):
        self.href = href
        req = urllib.request.Request(self.href, None, headers=header)
        cont = urllib.request.urlopen(req)
        self.soup = BeautifulSoup(cont.read(), 'html.parser', from_encoding='utf-8')

    def getOreUrl(self, page, bq, class_):
        nodes = self.soup.find_all(bq, class_=class_)
        return nodes[page].select('a')[0]['href']

    def getUrl(self, bq, class_):
        nodes = self.soup.find_all(bq, class_=class_)
        urls = []
        for node in nodes:
            urls.append(node.select('a')[0]['href'])
        return urls

    def getSoup(self):
        return self.soup

    def getContent(self, bq, class_):
        node = self.soup.find(bq, class_)
        if node is None:
            return None
        return node.text.strip().strip("展开全部").strip()

    def getAllContent(self, bq, class_):
        node = self.soup.find_all(bq, class_)
        conts = []
        if node is None:
            return None
        for cont in node:
            try:
                if re.search("c-", cont['class'][1]) is not None:
                    if cont['class'][2]:
                        continue
                else:
                    continue
            except:
                conts.append(cont.text.strip())
        return conts
