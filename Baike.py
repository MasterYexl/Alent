import re
import urllib.parse
from Alent import Parser, Zhidao


class Baike:
    def __init__(self, cts):
        self.cts = urllib.parse.quote(cts)
        ps = Parser.Parser("https://baike.baidu.com/item/"+self.cts)
        self.cont = ps.getContent("div", "lemma-summary")
        if self.cont is None:
            ps = Zhidao.Zhidao("什么是"+cts)
            self.cont = ps.getAns()

    def getAns(self):
        cont = re.sub("[　 。\n]+", "\n\t", self.cont)
        return "\t"+cont

    # https://baike.baidu.com/item/