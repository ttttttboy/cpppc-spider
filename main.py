# coding:utf-8
import os
import time
import re
import json
import requests
import csv
import codecs
import urllib.parse

def requestPage(curPage,keyword,url):
    """

    :param curPage:
    :param url:
    :return: json
    """

    payload = {'queryPage':curPage,
               'distStr':'',
               'induStr':'',
               'investStr':'',
               'projName':urllib.parse.quote(keyword),
               'sortby':'',
               'orderby':'',
               'stageArr':'',
               'projStateType':1}

    time.sleep(0.3)
    r = requests.post(url,params=payload)
    return r.json()

def write2CSV(filename,dict):
    fieldnames = ['id',
                  '项目名称',
                  '项目建设类型',
                  '地点1',
                  '地点2',
                  '地点3',
                  '发起时间',
                  '发起单位',
                  '项目介绍',
                  '所属行业1',
                  '所属行业2',
                  '投资规模',
                  '运作模式',
                  '回报机制',
                  '项目阶段',
                  '项目公司成立时间']


    with codecs.open(filename,'w','utf_8_sig') as fp:
        csv_writer  =csv.DictWriter(fp,fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(dict)





def main():

    result_list = []
    url = 'http://www.cpppc.org:8086/pppcentral/map/getPPPList.do'
    keyword = '河北' #  %E5%AE%89%E5%BE%BD 安徽，  %E5%AE%BF%E5%B7%9E 宿州
    filename = keyword + '.csv'

    curPage = 1
    totalPage = -1
    totalCount = -1

    while curPage < 1000000:
        j = requestPage(curPage, keyword, url)

        if totalCount == -1:
            totalCount = j['totalCount']

        if totalPage == -1:
            totalPage = j['totalPage']

        curPage = j['currentPage']

        if curPage >= totalPage+1:
            break

        # 开始填信息
        print("loading page %s/%s" % (curPage, totalPage))
        for i in j['list']:

            item = dict()

            item['id'] = i['PROJ_RID']
            item['项目名称'] = i['PROJ_NAME']
            item['项目建设类型'] = i['PROJ_TYPE_NAME']
            item['地点1'] = i['PRV1']
            item['地点2'] = i['PRV2']
            item['地点3'] = i['PRV3']
            item['发起时间'] = i['START_TIME']
            item['发起单位'] = i['START_UNAME']
            item['项目介绍'] = i['PROJ_SURVEY']
            item['所属行业1'] = i['IVALUE']
            item['所属行业2'] = i['IVALUE2']
            item['投资规模'] = i['INVEST_COUNT']
            item['运作模式'] = i['OPERATE_MODE_NAME']
            item['回报机制'] = i['RETURN_MODE_NAME']
            item['项目阶段'] = i['PROJ_STATE_NAME']
            item['项目公司成立时间'] = i['LOCK_TIME']

            result_list.append(item)

        curPage = curPage + 1

    write2CSV(filename,result_list)

if __name__ == "__main__":
    main()







# id PROJ_RID
# 项目名称 PROJ_NAME
# 项目建设类型 PROJ_TYPE_NAME
# 地点1 PRV1
# 地点2 PRV2
# 地点3 PRV3
# 发起时间 START_TIME
# 发起单位 START_UNAME
# 项目介绍 PROJ_SURVEY；
# 所属行业1 IVALUE
# 所属行业2 IVALUE2
# 投资规模（万） INVEST_COUNT
# 项目阶段 PROJ_STATE_NAME
# 运作模式 OPERATE_MODE_NAME
# 回报机制 RETURN_MODE_NAME
# 项目公司成立时间 LOCK_TIME
#

