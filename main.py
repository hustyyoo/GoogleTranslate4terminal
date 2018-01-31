import requests
from bs4 import BeautifulSoup
import bs4
import execjs  
import urllib
import sys


def getHTMLText(url,header):
    try:
        r = requests.get(url,timeout=30,headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getTKKjs(html):
    xlist=[]
    soup = BeautifulSoup(html, "html.parser")
    for gtc in soup.find_all('div',id='gt-c'):
        gtcs = gtc.find_all('script')
    tkkt=gtcs[0].text
    tkkt=tkkt.split("TKK")
    tkkt=tkkt[1].split(");")
    tkk="TKK"+tkkt[0]+");"
    return tkk

def getTKK(js):
    tkkjs_2="\n"+"return TKK;"
    tkkjs=js+tkkjs_2;
    with open ("TKK.js","w")  as  f:  
        f.write(tkkjs)  
        f.close
    tkk_value=execjs.compile(open(r"TKK.js").read()).call('eval')  
    #print(tkk_value)  
    return tkk_value  

def get_tk(qstr, tkk_value):
    tk_value=execjs.compile(open(r"getTKbyTKK.js").read()).call('tk',qstr,tkk_value)  
    #print(tk_value)  
    return tk_value 

def main():
    if len(sys.argv)>2:
        exit() 

    qstr=sys.argv[1]
    header={'user-agent':'"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    info = []
    url = 'https://translate.google.cn'
    url_api='/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=3&kc=0&tk='
    html = getHTMLText(url, header)
    tk_value=str(get_tk(qstr,getTKK(getTKKjs(html))))
    url_t=url+url_api+tk_value+'&q='+str(urllib.parse.quote(qstr))
    print(getHTMLText(url_t, header))

main()
