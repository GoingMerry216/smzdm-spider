import requests
from bs4 import BeautifulSoup
import json

def get_real_time_data(key):
    url = 'https://search.smzdm.com/'
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
    params = {
        'c': 'home',
        's': key,
        'order': 'time'
    }
    r = requests.get(url=url, params=params, headers=headers, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')

    print(soup.prettify())


if __name__ == '__main__':
    get_real_time_data('漱口水')

# feed-main-list => ul
# li is product
# feed-block-title：smzdm's everything   # money div .z-highlight
# z-feed-foot: producta salers /p/{id}


# .feed-block-title => whole thing
# title
