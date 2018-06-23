import random
import requests
from lxml import etree
import csv
import time
import re

def get_header():
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
#Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.
    HEADER = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate'
    }
    return HEADER


def write_csv(info,txt_name):
    with open(txt_name, 'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(info)

# def get_info(url,proxies):
#     header=get_header()
#     html=requests.get(url,headers=header,proxies=proxies).content
#     # html = requests.get('http://api.xicidaili.com/free2016.txt').content
#     selector = etree.HTML(html)
#     panel_heading = selector.xpath("//div[@class='panel-heading']")[0].xpath('h1')[0].text
#     panel_body = selector.xpath("//ul[@class='list-group']/li")
#     content_l = []
#     content_l.append(panel_heading)
#     for group_item in panel_body[:3]:
#         content = group_item.xpath('a/text()')[0]
#         # print(content)
#         content_l.append(content)
#     for group_item in panel_body[3:]:
#         content = group_item.xpath('text()')[0]
#         # print(content)
#         content_l.append(content)
#     content_l.append(url.split('/')[-1].split('.')[0])
#
#     '''
#     poi名字，省份，市，区域，位置，电话，分类，大地坐标，火星坐标，百度坐标，url号码
#     '''
#     return content_l

def init_proxy_file():
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Referer': 'http://www.xicidaili.com/nn/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Ubuntu Chromium/60.0.3112.113 Chrome/60.0.3112.113 Safari/537.36',
    }
    proxyHeaders = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Ubuntu Chromium/60.0.3112.113 Chrome/60.0.3112.113 Safari/537.36',
    }
    ls=[]
    for pageNum in range(1,50):
        url = 'http://www.xicidaili.com/nn/' + str(pageNum)
        page = requests.get(url, headers=headers).text
        # time.sleep(2)
        pattern = re.compile(u'<tr class=".*?">.*?'
                             + u'<td class="country"><img.*?/></td>.*?'
                             + u'<td>(\d+\.\d+\.\d+\.\d+)</td>.*?'
                             + u'<td>(\d+)</td>.*?'
                             + u'<td>.*?'
                             + u'<a href=".*?">(.*?)</a>.*?'
                             + u'</td>.*?'
                             + u'<td class="country">(.*?)</td>.*?'
                             + u'<td>([A-Z]+)</td>.*?'
                             + '</tr>'
                             , re.S)
        l = re.findall(pattern, page)
        ls=ls+l
    ls_http=[i for i in ls if i[4]=='HTTP']
    ls_https=[i for i in ls if i[4]=='HTTPS']
    with open('../proxy_ip_http.txt', 'w',newline='') as f:
        writer = csv.writer(f)
        for i in ls_http:
            writer.writerow(i)
    with open('../proxy_ip_https.txt', 'w',newline='') as f:
        writer = csv.writer(f)
        for i in ls_https:
            writer.writerow(i)

def select():
    f=open('../proxy_ip_http.txt','r')
    proxy_ip=f.readlines()
    f.close()
    proxy_ip_http=[i.strip().split(',') for i in proxy_ip]

    f=open('../proxy_ip_https.txt','r')
    proxy_ip=f.readlines()
    f.close()
    proxy_ip_https=[i.strip().split(',') for i in proxy_ip]
    return proxy_ip_http,proxy_ip_https

def getAccessIP(size=1):
    info_http,info_https = select()
    p_http = []
    for k,i in enumerate(info_http):

        if len(p_http) == size:
            break
            # return p_http
        header = get_header()
        try:
            r=requests.get('http://ip.chinaz.com/',
                       proxies={"{}".format(i[4].lower()): "{}://{}:{}".format(i[4].lower(), i[0], i[1])},
                           headers=header,timeout=5)

            selector = etree.HTML(r.content)
            ip_ = selector.xpath("//p[@class='getlist pl10']/text()")[0].strip()
            if r.status_code==200:
                if ip_==i[0]:
                    p_http.append(i)
        except:
            continue

    p_https=[]
    for k,i in enumerate(info_https):
        if len(p_https) == size:
            # break
            return p_http,p_https
        header = get_header()
        try:
            r = requests.get('https://www.ip.cn/',
                             proxies={"{}".format(i[4].lower()): "{}://{}:{}".format(i[4].lower(), i[0], i[1])},
                             headers=header,timeout=5)
            selector = etree.HTML(r.content)
            ip_ = selector.xpath("//div[@class='well']/p/code")[0].text
            # r=requests.get('https://www.baidu.com/',
            #            proxies={"{}".format(i[4]): "{}://{}:{}".format(i[4], i[0], i[1])},headers=header,timeout=5)
            if r.status_code==200:
                if ip_==i[0]:
                    p_https.append(i)
        except:
            continue


from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
def send_email(num=1):
    #qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    #sender_qq为发件人的qq号码
    sender_qq = '291885444'
    #pwd为qq邮箱的授权码
    pwd = 'vautdvccfxcycbdb'
    #发件人的邮箱
    sender_qq_mail = '291885444@qq.com'
    #收件人邮箱
    receiver = '291885444@qq.com'
    #邮件的正文内容
    mail_content = '爬虫{}已经停止'.format(num)
    #邮件标题
    mail_title = '爬虫远程提醒'

    #ssl登录
    smtp = SMTP_SSL(host_server)
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()