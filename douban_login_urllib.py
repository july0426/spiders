#coding:utf8
import urllib2,urllib
import cookielib
from lxml import etree

login_url = 'https://www.douban.com/accounts/login'

cookie = cookielib.CookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(cookie_handler)

headers = {
    "Host": "www.douban.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Origin": "https://www.douban.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.douban.com/",
    "Accept-Language": "zh-CN,zh;q=0.8",
}

def getLogin():
    response = urllib2.urlopen(login_url)
    return response.read()

def login(login_page):
    html = etree.HTML(login_page)
    captcha_url = html.xpath('//img[@id="captcha_image"]/@src')[0]
    request = urllib2.Request(captcha_url,headers=headers)
    response = urllib2.urlopen(request)
    with open('code.jpg','wb') as f:
        f.write(response.read())

    captcha_solution = raw_input('输入solution ：')
    # captcha_id = raw_input('输入id：')

    captcha_id = html.xpath('//input[@name="captcha-id"]/@value')[0]

    data = {
        'source' : 'index_nav',
        'form_email' : 'hgkgj',
        'form_password' : 'jkhj',
        'login' : '登录',
        'captcha-solution' : captcha_solution,
        'captcha-id' : captcha_id,
    }
    data = urllib.urlencode(data)



    request = urllib2.Request(login_url,data=data,headers=headers)

    response = opener.open(request)
    # print response.read()

def accountManage():
    url = 'https://www.douban.com/accounts/'
    response = opener.open(url)
    print response.read()

if __name__ == '__main__':
    login_page = getLogin() #获取登陆页面
    print '-' * 300
    login(login_page)
    accountManage() # 获取账户管理