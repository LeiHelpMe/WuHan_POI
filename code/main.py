import Get_tool
import os
import requests
from lxml import etree
import csv
import natsort
import sys
import time


# Get_tool.init_proxy_file()
CKPT_PATH='../log/ckpt.txt'
base_url='http://www.poi86.com'
base_url_area='http://www.poi86.com/poi/amap/district/'
poi_url_name=os.listdir('../log/poi_url')
poi_url_name=natsort.natsorted(poi_url_name)
if os.path.exists(CKPT_PATH):
    f = open(CKPT_PATH, 'r')
    ckpt = f.read()
    f.close()
    ckpt=ckpt.split(',')
    ckpt=[int(i) for i in ckpt]
    AREA=ckpt[0]
    LINE=ckpt[1]
else:
    AREA=0
    LINE=0
FILEPATH='../file/'+str(AREA)+'_'+str(LINE)+'_poi.csv'

def get_info(r):
    html = r.content
    selector = etree.HTML(html)
    panel_heading = selector.xpath("//div[@class='panel-heading']")[0].xpath('h1')[0].text
    panel_body = selector.xpath("//ul[@class='list-group']/li")
    content_l = []
    content_l.append(panel_heading)
    for group_item in panel_body[:3]:
        content = group_item.xpath('a/text()')[0]
        # print(content)
        content_l.append(content)
    for group_item in panel_body[3:]:
        content = group_item.xpath('text()')[0]
        # print(content)
        content_l.append(content)
    content_l.append(url.split('/')[-1].split('.')[0])
    return content_l

def get_proxies():
    ip_http, ip_https = Get_tool.getAccessIP()
    ip_http = ip_http[0]
    ip_https = ip_https[0]

    proxies = {ip_http[4].lower(): ip_http[4].lower() + '://' + ip_http[0] + ':' + ip_http[1],
               ip_https[4].lower(): ip_https[4].lower() + '://' + ip_https[0] + ':' + ip_https[1]}
    return proxies
# proxies=get_proxies()
proxies=None
for area in range(AREA,10):
    if LINE==0:
       FILEPATH='../file/'+str(area)+'_000_poi.csv'
    f = open('../log/poi_url/'+poi_url_name[area], 'r')
    area_poi_url = f.read()
    area_poi_url=area_poi_url.split('\n')
    f.close()
    del area_poi_url[-1]
    for line in range(LINE,len(area_poi_url)):
        url=area_poi_url[line]
        try:
            if line %20==0:
                # print(proxies.values())
                time.sleep(2)
            header = Get_tool.get_header()
            r=requests.get(url, headers=header, proxies=proxies)
            # if r.status_code==200:
            content_l=get_info(r)
        except:
            f = open('../log/ckpt.txt', 'w')
            f.writelines('{},{}'.format(area, line))
            f.close()
            # Get_tool.send_email()
            print(header)
            print('/n')
            print(line)
            print('sys.exit')
            sys.exit(0)
        if line==len(area_poi_url)-1:
            LINE=0
        try:
            Get_tool.write_csv(content_l,FILEPATH)
        except  :
            print(line,'is error')
        if line % 20==0:
           print('{}-{}/{}'.format(area,line,len(area_poi_url)))

'''
[927,933,630,526,1240,
 263,1322,494,88,602,
 654,755,1047]

['420102', '420103', '420104','420105','420106',
 '420107','420111','420112','420113','420114',
 '420115','420116','420117']

['江岸区','江汉区','硚口区','汉阳区','武昌区',
 '青山区','洪山区','东西湖区','汉南区','蔡甸区',
 '江夏区','黄陂区','新洲区']

'''
