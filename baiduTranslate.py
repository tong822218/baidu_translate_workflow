#/usr/bin/env python
# coding:utf-8
import sys
import httplib
import md5
import urllib
import random
import json
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')


def translate(query,toLang):
    conf = ConfigParser.ConfigParser()
    conf.read('config')  # 文件路径
    appid = conf.get("section1", "appid")
    secretKey = conf.get("section1", "secretKey")
    httpClient = conf.get("section1", "httpClient")
    myurl = conf.get("section1", "myurl")
    fromLang = conf.get("section1", "fromLang")
    toLang = toLang

    salt = random.randint(32768, 65536)
    q = query.encode('utf8')
    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        #response是HTTPResponse对象
        response = httpClient.getresponse()
        res = response.read()
        result = json.loads(res)
        aa = result['trans_result'][0]
        aa['to'] = result['to']
        aa['from'] = result['from']
        return aa
    except Exception, e:
        print ('*'*30)
        print e
    finally:
        if httpClient:
            httpClient.close()


def start(query):
    conf = ConfigParser.ConfigParser()
    conf.read('config')  # 文件路径
    tolang = conf.get("section1", "toLang")
    arr = tolang.split(',')
    result = []
    for item in arr:
        re = translate(query, item)
        icon = 'icon.jpg'
        if item == 'zh':
            icon = 'icon/china.png'
        elif item == 'en':
            icon = 'icon/us.png'
        elif item == 'jp':
            icon = 'icon/japan.png'
        elif item == 'kor':
            icon = 'icon/kor.png'
        re['lang'] = item
        re['icon'] = icon
        result.append(re)
    return result


if __name__ == '__main__':
    start('hello')
