import requests
from bs4 import BeautifulSoup
import json
import os
import sys
import json
import codecs
import re
from urllib.parse import urlparse,urlunparse,parse_qs,parse_qsl
from flask import Flask,request
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World, WDNMD!"

#  | 参数键值  | 值                          | 备注      |
#  | --------- | --------------------------- | --------- |
#  | c         | home                        | 不清楚    |
#  | s         | 漱口水                      | 查询键值  |
#  | order     | time/score                  | 时间/综合 |
#  | cate_id   | 75：母婴<br />113：个护化妆 | 分类      |
#  | mall_id   | 183：天猫                   | 商城      |
#  | min_price | 10                          | 最小价格  |
#  | max_price | 100                         | 最大价格  |
#  | brand_id  | 1049：李施德林              | 品牌id    |
@app.route('/api/v1.0/products')
def get_product_list():
    return get_real_time_data(suburl='', params=request.args)

@app.route('/api/v1.0/smzdm/<string:suburl>')
def get_product_list2(suburl):
    print(suburl)
    return get_real_time_data(suburl=suburl, params={})

def get_real_time_data(suburl, params):
    url = 'https://search.smzdm.com/'+suburl
    headers = {
        'Host': 'search.smzdm.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Cookie': '__ckguid=haJ39aanSIvTc42oK4tAe42; device_id=21307064331585273181171510acd2f8fd0dcce47f2a727349df8867bf; homepage_sug=i; r_sort_type=score; _ga=GA1.2.263182243.1585273185; __gads=ID=42d4a5069123a677:T=1585273186:S=ALNI_MYjLuDnpmWyMS19HchQaziJEfqKuw; __jsluid_s=62866222fb8a466627e3478816a38b09; ss_ab=ss52; zdm_qd=%7B%22referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D_nquptPSJQGpXAahBYwVIHF_KozE_RW_yogN-tSCNyS%26wd%3D%26eqid%3Ddf59e2dd00001be2000000025e7f7db0%22%7D; _gid=GA1.2.1583493778.1585413560; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1585273186,1585413559,1585447499; PHPSESSID=7318436e1ce8bda1706526c3cec773f3; wt3_sid=%3B999768690672041; wt3_eid=%3B999768690672041%7C2158544750100925873%232158544755000105190; s_his=%E5%8F%AF%E5%8F%A3%E5%8F%AF%E4%B9%90%2Cshukoushui%2C%E4%B9%A6%E5%8F%A3%E5%91%B3%2C%E6%BC%B1%E5%8F%A3%E6%B0%B4; _zdmA.uid=ZDMA.z4Hkbi9bm.1585451445.2419200; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1585451593; _gat_UA-27058866-1=1; amvid=717fdf0aa1d4b8ca12ae6ecd7d574e38'
    }

    s = requests.session()
    s.keep_alive = False
    r = requests.get(url=url, params=params, headers=headers, verify=False).content.decode("utf-8").encode("utf-8")
    soup = BeautifulSoup(r, 'html.parser')
    save_path = u"页面"
    if params != {}:
        key = params['s']
    else:
        query_obj = parse_qs(urlparse(url).query)
        print(query_obj)
        key = query_obj['s'][0]
    filename = u"" + key + '.html'
    # StringListSave(save_path, filename, r)

    subcate_tab_list = soup.find('ul', class_="subcate-tab-list")
    channelTag = []
    for childXml in subcate_tab_list :
        channelTag.append(childXml.string)
    
    # 前三个有意义 按顺序分别表示 分类 商城 品牌
    J_filter_items = soup.find_all('div', class_="filter-items J_filter_items")

    # getCategory(J_filter_items)

    # getMall(J_filter_items)

    # getBrand(J_filter_items)


    itemxmllist = soup.find_all('div', class_="z-feed-content")
    itemlist = []
    for item in itemxmllist:
        h5 = item.find('h5')
        if h5 != None:
            itemDetail = {}
            itemProperty = h5.find_all('a')
            itemDetail['name'] = itemProperty[0]['title']
            if len(itemProperty)>1:
                itemDetail['price'] = itemProperty[1].find('div',class_="z-highlight").text
                itemDetail['href'] = itemProperty[1]['href']
                itemDetail['id'] = itemProperty[1]['href'].split('https://www.smzdm.com/p/')[1].split('/')[0]
                itemlist.append(itemDetail)
    print(itemlist)

    save_path = u"页面"
    filename = u""+key+'.json'
    listJsonStr = json.dumps(itemlist, ensure_ascii=False).encode("utf-8")
    # StringListSave(save_path, filename, listJsonStr)
    return listJsonStr

def getBrand(J_filter_items):
    brand = []
    for childXml in J_filter_items[2].find_all('a') :
        brand.append(childXml.string)
        print(childXml.string)

def getMall(J_filter_items):
    mall = []
    for childXml in J_filter_items[1].find_all('a') :
        mall.append(childXml.string)
        print(childXml.string)
    return mall

def getCategory(J_filter_items):
    category = []
    for childXml in J_filter_items[0].find_all('a') :
        category.append(childXml.string)
        print(childXml.string)
    return category

def StringListSave(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename
    with open(path, "wb") as fp:
        fp.write(slist)

def listToJson(lst):
    import json
    import numpy as np
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
    return str_json

if __name__ == '__main__':
    get_real_time_data(suburl='?s=漱口水&max_price=5',params={})
    # app.run(port=8091, debug=True)

# feed-main-list => ul
# li is product
# feed-block-title：smzdm's everything   # money div .z-highlight
# z-feed-foot: producta salers /p/{id}


# .feed-block-title => whole thing
# title
