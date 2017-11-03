#coding:utf8
import urllib2,urllib
import cookielib
import re
import random

# 设置是否开启代理池  0: 花钱代理  1 使用免费代理  2 不使用代理
proxy_switch = 1
max_retry = 5

# 创建cookiehandler
cookie = cookielib.CookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookie)

# 创建代理handler


def getProxyHandler(proxy_list):
    
    if proxy_switch == 1:
        # 免费代理，从爬取的代理池中读取
        print '用免费代理'
        with open('proxy.txt','r') as f:
        
            proxy_list = f.readlines()  #从文件中读取的代理列表
            print proxy_list
            proxy_poll = []  # 代理池
            for proxy in proxy_list:
                res = proxy.split(' ')
                proxy_poll.append( #向代理池中加入一个代理
                    {
                        'http' : res[2].lower() + '://'  + res[0] + ':' + res[1],
                        'https' : res[2].lower() + '://'  + res[0] + ':' + res[1],
                    }
                )
        print proxy_list
        proxy_poll = []  # 代理池
        for proxy in proxy_list:
            res = proxy.split(' ')
            proxy_poll.append( #向代理池中加入一个代理
                {
                    'http' : res[2].lower() + '://'  + res[0] + ':' + res[1],
                    'https' : res[2].lower() + '://'  + res[0] + ':' + res[1],
                }
            )
        if proxy_poll:  #如果有代理则随机 ，否则不实用代理
            proxy = random.choice(proxy_poll)
        else:
            proxy = {}

        print proxy
        proxy_handler = urllib2.ProxyHandler(proxy)

    else:
        proxy_handler = urllib2.ProxyHandler()  # 使用私密代理

    return proxy_handler


def getOpener(proxy_handler):
    opener = urllib2.build_opener(proxy_handler)
    # urllib2.install_opener(opener)  # urllib2.urlopen时候都用这个opener去发请求

    urllib2.install_opener(opener)
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    return opener

def getPage():
    base_url = 'http://www.xicidaili.com/nn/'
   
    start = raw_input('起始：')
    end = raw_input('结束：')

    with open('proxy.txt','r') as f:
        proxy_list = f.readlines()  # 打开时候一定不能先清空

    with open('proxy.txt', 'w+') as f:
        for i in range(int(start), int(end)):
            fullurl = base_url + str(i)
            for i in range(max_retry): #循环去尝试open
                try:
                    proxy_handler = getProxyHandler(proxy_list)
                    opener = getOpener(proxy_handler)
                    response = opener.open(fullurl,timeout=3)
                    break
                except (urllib2.URLError,Exception) as e:
                    response = None
                    print str(e)
            if response is not None:  # 多次尝试成功以后就进行html读取
                html = response.read()
            else:
                print '代理不可用，请检查！！'
                exit()
            # print html
            tr_pattern = re.compile(r'<tr.*?>.*?' + r'(?:<td.*?>(.*?)</td>.*?)' * 10 + r'.*?</tr>' ,re.S)
            tr_list = tr_pattern.findall(html)

            speed_pattern = re.compile(r'title="(.*?)"')
            for tr in tr_list:
                # 过滤响应小于2秒的
                res = speed_pattern.search(tr[6])
                speed = res.group(1)
                speed = speed.replace('秒','')
                # 存活期大于1天以上的
                if float(speed) < 2 and '天' in tr[8]:
                    print 'crawling : %s' % tr[1]
                    f.write("%s %s %s %s %s\n" % (tr[1],tr[2],tr[5],speed,tr[8],))
                    

if __name__ == '__main__':
    getPage()
    pass

