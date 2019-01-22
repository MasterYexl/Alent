import requests, re
from Alent import Baidu, Parser
from bs4 import BeautifulSoup

header = {'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
          }


class Novel:
    def __init__(self, book_name):
        self.book_name = book_name
        self.engine = 0
        bd = Baidu.Baidu(book_name+"小说")
        page = 0
        while True:
            href = bd.getOneUrl(page)
            try:
                if not href: break
                self.relurl = requests.get(href, headers=header).url
                p = Parser.Parser(self.relurl)
                soup = p.getSoup()
                # 找出可能的章节
                dir_ = soup.find_all("a", class_="", id="", text=re.compile(r"(第.+[章幕])|序|引子"))
                if len(dir_) < 50:
                    mulu = soup.find_all("a", text=re.compile(r"章节"))
                    if mulu is None:
                        mulu = soup.find_all("", text=re.compile(r"目录"))
                    if mulu is not None:
                        newhf = self.url_txt(self.relurl, mulu[0]['href'])
                        print(newhf)
                        p = Parser.Parser(newhf)
                        soup = p.getSoup()
                        # 找出可能的章节
                        dir_ = soup.find_all("a", class_="", id="", text=re.compile(r"(第.+[章幕])|序|引子"))
                self.url = []
                self.tit = []
                swc = 1
                for d in dir_:
                    if swc == 0:
                        self.url.append(self.url_txt(self.relurl, d['href']))
                        self.tit.append(d.text.strip())
                        continue
                    if re.search(r"(第0*[1一壹][章节回幕])|序|引子", d.text.strip()) is None:
                        continue
                    self.url.append(self.url_txt(self.relurl, d['href']))
                    self.tit.append(d.text.strip())
                    swc = 0

                if len(dir_) == 0:
                    page = page + 1
                    continue
                break
            except:
                page = page + 1

    def url_txt(self, relurl, href):
        if re.search('/', href) is None:
            tmpurl = relurl[::-1]
            tmpurl = re.sub('[a-z]+\.[a-z].*?/', "", tmpurl, 1)
            href = tmpurl[::-1] + "/" + href
            return href
        if re.search('\..+\..+?/', href) is None:
            y = 0
            # 去重
            for x in range(0, len(relurl)):
                if relurl[x] == href[y]: y = y + 1
                else:
                    y = 0
                    if relurl[x] == href[y]: y = y + 1
            href = relurl.rstrip("/") + "/" + href[y:].lstrip("/")
        if re.search(r'//', href) is None:
            href = "//" + href
        if re.search('http:|https:', href) is None:
            href = 'http:' + href
        return href

    def getUrl(self):
        return self.url

    def getTit(self):
        return self.tit

    def down(self, start=0, end=-1):
        if end == -1:
            end = len(self.tit)+1
        for pg in range(int(start), int(end)):
            self.read(pg, True)


    def read(self, page, down=False):
        page = int(page)
        url = self.url[page]
        soup = Parser.Parser(url).getSoup()
        if self.engine == 1:
            count = soup.find("", class_=re.compile("content")).text
        elif self.engine == 2:
            count = soup.find("", id=re.compile("content")).text
        elif self.engine == 3:
            count = ""
            tmpcount = soup.find_all("", text=re.compile(r"[，。？！]"))
            for c in tmpcount:
                count = count + c + "\n\n"
        # 获取最佳抓取方法
        else:
            try:
                self.engine = 1
                count = soup.find("", class_=re.compile("content")).text
                if len(count) < 100:
                    count[111]

            except:
                try:
                    self.engine = 2
                    count = soup.find("", id=re.compile("content")).text
                    if len(count) < 100:
                        count[111]

                # 最后的解决办法
                except:
                    count = ""
                    self.engine = 3
                    tmpcount = soup.find_all("", text=re.compile(r"[，。？！]"))
                    for c in tmpcount:
                        count = count + c + "\n\n"
        # 整理数据
        wrcode = 18
        # 去除章节引导
        count = re.sub(r"[上下]一.*\n*.*\n*.*目*录*.*\n*.*\n*[下上]一.*\n*.*\n*书*签*.*", "", count)
        # 去除广告语句
        count = re.sub(r"\n+[A-Za-z\u4e00-\u9fa5\n]+\n", "\n", count)
        # 去除可疑代码
        count = re.sub(r'[A-Za-z0-9]+\(*\)*;', "\n", count)
        # 去除代码语句
        count = re.sub(r"\n*[^\u4e00-\u9fa5，。；！？.,]+\n+", "\n", count)
        count = re.sub(r"\n+[^\u4e00-\u9fa5，。；！？.,]+\n*", "\n", count)
        #  去除多余行
        count = re.sub("[　  \n]+", "\n\t", count)

        if down:
            try:
                txt = open(self.book_name + ".txt", "a", encoding="utf-8")
            except:
                txt = open(self.book_name + ".txt", "w", encoding="utf-8")
                txt.close()
                txt = open(self.book_name + ".txt", "a", encoding="utf-8")
                print("书名抓取错误")
            print("第缓"+str(page)+"存完成")
            txt.write("\n\n" + self.tit[page] + "\n\n")
            txt.write(count)
        else:
            return count


if __name__ == "__main__":
    t = Novel("斗罗大陆")
    url = t.getUrl()
    tit = t.getTit()
    for a in range(len(url)):
        print(tit[a])
        print(url[a])
    a = input()
    t.read(a)