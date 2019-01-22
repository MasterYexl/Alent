import re
import urllib.parse
from Alent import Parser


class Zhidao:

    def __init__(self, cts):
        self.cts = urllib.parse.quote(cts)
        ps = Parser.Parser("https://zhidao.baidu.com/search?word="+self.cts)
        url = ps.getOreUrl(1, "dt", "dt mb-4 line")
        ps = Parser.Parser(url)
        self.cont = ps.getContent("div", "best-text mb-10")

    def getAns(self):
        cont = re.sub("[　 。\n]+", "\n\t", self.cont)
        return "\t"+cont
    # https://zhidao.baidu.com/search?word=china