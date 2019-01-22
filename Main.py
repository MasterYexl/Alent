
import re
import webbrowser

from Alent import Zhidao, Baike, Baidu, Novel

while True:

    cts = input(">")
    cts = re.sub(r"[!?.！？。吗]+", "", cts)
    if re.match("小说", cts) is not None:
        cts = re.sub("小说", "", cts)
        print("正在搜索，请稍后..")
        t = Novel.Novel(cts)
        tit = t.getTit()
        for i in range(len(tit)):
            print(str(i+1) + ". "+tit[i])
        print("你想看第几章？需要缓存吗？")
        while True:
            cmd = input("("+cts+")>")
            if re.search("帮助|怎么", cmd) is not None:
                print("直接查看：输入序号\n下载：输入你想下载的章节")
            elif re.search("缓存|下载", cmd):
                if re.search("全部|所有", cmd):
                    t.down()
                else:
                    st = ""
                    en = ""
                    swc = 0
                    for cm in cmd:
                        if '0' <= cm <= '9':
                            if swc == 0:
                                swc = 1
                            if swc == 1:
                                st = st + cm
                            else:
                                en = en + cm
                        if swc == 1:
                            swc = 2
                    print(str(swc)+" "+st+" "+en)
                    if swc != 2:
                        t.down(int(st-1))
                    t.down(int(st)-1, en)
            elif re.search("退出|不看了", cmd) is not None:
                break
            else:
                nb = ""
                for cm in cmd:
                    if '0' <= cm <= '9':
                        nb = nb + cm
                if nb == "":
                    print("直接查看：输入序号\n下载：输入你想下载的章节")
                else:
                    print(t.read(nb))
    elif re.search("打开|官网|首页", cts) is not None:
        cts = re.sub("打开|进入|搜索", "", cts)
        cts = re.sub("首页|官网", "", cts)
        print("请稍后..")
        t = Baidu.Baidu(cts+"官网")
        url = t.getOneUrl(0)
        webbrowser.open(url)

    elif re.match("百度|查找|搜索", cts) is not None:
         cts = re.sub("百度|的资料|搜索|查找+", "", cts)
         t = Baidu.Baidu(cts)
         t.getAns()
    elif re.search("是什么|什么是|你知道", cts) is not None:
        if re.search("什么是", cts) is None and re.search("是", cts) is None:
            cts = re.sub("你知道", "", cts)
            t = Zhidao.Zhidao(cts)
            print(t.getAns())
        else:
            cts = re.sub("什么是|你知道|是什么+", "", cts)
            t = Baike.Baike(cts)
            print(t.getAns())
    elif re.search("你知道|为什么", cts) is not None:
        cts = re.sub("你知道", "", cts)
        t = Zhidao.Zhidao(cts)
        print(t.getAns())
    elif re.search("帮助|功能", cts) is not None:
        print("目前的功能：\n小说：输入小说+小说名\n百度、搜索\n回答一些问题\n打开网址")
    else:
        print(cts)