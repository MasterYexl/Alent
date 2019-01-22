import re
import urllib.parse
from Alent import Parser


class Baidu:

    def __init__(self, cts):
        self.cts = urllib.parse.quote(cts)
        ps = Parser.Parser("https://www.baidu.com/s?wd="+self.cts)
        urls = ps.getUrl("h3", "t")
        self.conts = ps.getAllContent("h3", "t")
        self.urls = []
        for url in urls:
            if len(url) < 300:
                self.urls.append(url)

    def getAns(self):
        for a in range(len(self.urls)):
            print(self.conts[a])
            print(self.urls[a])

    def getOneUrl(self, nub):
        if nub > len(self.urls):
            return False
        return self.urls[nub]

    # https://www.baidu.com/s?wd=

if __name__ == "__main__":
    t = Baidu("康师傅")
    t.getAns()