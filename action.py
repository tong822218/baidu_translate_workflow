#!/usr/bin/python
#coding=utf8
import sys
import json
import webbrowser
import urllib
from workflow import Workflow
reload(sys)
sys.setdefaultencoding('utf-8')
import logging
import logging.handlers 

def getLog():
    logger = logging.getLogger("mylogger") 
    logger.setLevel("DEBUG") #设置级别为DEBUG，覆盖掉默认级别WARNING  
    fh = logging.FileHandler('./log')  
    fh.setLevel("INFO")  
    
    #定义handler的格式输出  
    log_format=logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s-[%(filename)s:%(lineno)d]")  
    fh.setFormatter(log_format) #setFormatter() selects a Formatter object for this handler to use  
    #为logger添加handler  
    logger.addHandler(fh)   
    return logger

logger = getLog()
wf = Workflow()
query = wf.args[0].encode('utf8').replace('\\\"','\"')
query = query.replace('\\\\','\\')
try:
    lang = json.loads(query)
    logger.info(lang)
except Exception, e:
    logger.info(e)

search = urllib.quote(lang['query'].encode('utf8'))
url = "http://fanyi.baidu.com/#"+lang['from']+"/"+lang['to']+"/"+search
webbrowser.open(url)
