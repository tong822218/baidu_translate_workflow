#!/usr/bin/python
#coding=utf8
import sys,json
reload(sys)
sys.setdefaultencoding('utf-8')

from workflow import Workflow, web
import baiduTranslate
import logging
import logging.handlers 

def search(query):
    # url = 'http://gankio.herokuapp.com/search'
    # params = dict(keyword=query)
    # r = web.post(url, params)
    # r.raise_for_status()

    # translator = Translator()
    # obj = translator.translate(query, dest='zh-cn')

    obj = baiduTranslate.start(query)

    return obj


def main(wf):

    query = wf.args[0]

    def wrapper():
        return search(query)

    # list = wf.cached_data(query, wrapper, max_age=0)
    list = wrapper()
    for item in list:
        ar = {}
        ar["to"] = item["to"]
        ar["from"] = item["from"]
        ar["query"] = query
        args = json.dumps(ar)
        wf.add_item(title=item['dst'], subtitle=item['src'], arg=args, valid=True, icon=item['icon'])

    wf.send_feedback()


#创建一个logger实例  
def getLog():
    logger = logging.getLogger("mylogger") 
    logger.setLevel("DEBUG") #设置级别为DEBUG，覆盖掉默认级别WARNING  
    fh = logging.FileHandler('./log')  
    fh.setLevel("INFO")  
    ch = logging.StreamHandler()  
    ch.setLevel("ERROR") 
    #定义handler的格式输出  
    log_format=logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s-[%(filename)s:%(lineno)d]")  
    fh.setFormatter(log_format) #setFormatter() selects a Formatter object for this handler to use  
    ch.setFormatter(log_format) 
    #为logger添加handler  
    logger.addHandler(fh)   
    logger.addHandler(ch) 
    return logger


if __name__ == '__main__':
    # logger = getLog()
    wf = Workflow()
    sys.exit(wf.run(main))
