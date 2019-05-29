#encoding:utf8

from __future__ import unicode_literals
from django.shortcuts import render
import math
from django.http import HttpResponse
from django.template import loader
from pyecharts import Line3D,Pie
from django.shortcuts import render,render_to_response
import pandas as pd
import numpy as np
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def recommender(request):
    if request.method=='POST':
        app_dic = {}
        tel = int(request.POST.get('user_tel'))
        app_list = get_recommender(tel)
        for app in app_list:
            if app not in app_dic:
                app_dic[app] = {}
            name = get_name(app)
            app_dic[app] = {'app_id': app , 'name':name}
        return render_to_response('recommender.html',{
            'app_dic':app_dic,
            'flag':True
        })
        # return HttpResponse(app_dic)
        # return HttpResponse(tel)
    return render_to_response('recommender.html')



app_tab = pd.read_csv('/Users/bellick/MyProjects/UserProfile/data/appTab.txt',encoding='gb18030',sep='|',names=['app_id','name','male','female','_24','25_30','31_35','36_40','40_'])
app_tab = app_tab.set_index('app_id',drop=False)
user_data = pd.read_csv('/Users/bellick/MyProjects/UserProfile/data/userdata_new.txt',sep='|',names = ['tel','app_id','date','time'])
user_data = user_data.set_index('tel')

def get_name(id):
    return app_tab.loc[id,'name']

# 计算某两个app之间的相似度,利用pearson相关系数
from scipy.stats import pearsonr
def get_similarity(id_1,id_2):
    data_1 = app_tab.loc[id_1,['male','_24','25_30','31_35','36_40']].values
    data_2 = app_tab.loc[id_2,['male','_24','25_30','31_35','36_40']].values
    return pearsonr(data_1,data_2)[0]
# 计算余弦相似度
def cos_like(id_1,id_2):
    data_1 = app_tab.loc[id_1, ['male', '_24', '25_30', '31_35', '36_40']].values.astype('float64')
    data_2 = app_tab.loc[id_2, ['male', '_24', '25_30', '31_35', '36_40']].values.astype('float64')
    num = float(np.matmul(data_1, data_2))
    s = np.linalg.norm(data_1) * np.linalg.norm(data_2)
    return num/s

def get_app_ids():
    return app_tab.loc[:,'app_id'].values
# 获得和某个app最相似的10个app
def get_most_similar(id_):
    app_ids = get_app_ids()
    distances = {}
    for app_id in app_ids:
        distances[app_id] = cos_like(app_id,id_)
    most_similar =  sorted(distances.items(),key=lambda item:item[1])[-10:][::-1]
    return most_similar

# 获得某用户的推荐结果
def get_recommender(tel):
    used_apps = user_data.loc[tel].values
    result = {}
    for used_app in used_apps:
        # print(used_app)
        app_id = used_app[0]
        time = used_app[2]
        most_similar = get_most_similar(app_id) # 获得和此app最相似的10个app及其相似度
        for app in most_similar:
            if app[0] in result:
                result[app[0]] += app[1] * time  # 该app的相似度乘以停留时间
            else:
                result[app[0]] = app[1]* time
    sort = sorted(result.items(),key=lambda item:item[1])[-10:][::-1]
    return [item[0] for item in sort]

if __name__ == '__main__':
    # print(get_recommender(13900000005))

    # used_apps = user_data.loc[13900000005].values
    # for used_app in used_apps:
    #     print(used_app)

    # app_dic = {}
    # tel = 13900000005
    # app_list = get_recommender(tel)
    # for app in app_list:
    #     if app not in app_dic:
    #         app_dic[app] = {}
    #     name = get_name(app)
    #     app_dic[app] = {'app_id': app, 'name': name}
    # print(app_dic)

    app_dic = {360261: {u'app_id': 360261, u'name': u'chinahr'}, 360262: {u'app_id': 360262, u'name': u'\u524d\u7a0b\u65e0\u5fe7'}, 360263: {u'app_id': 360263, u'name': u'\u667a\u8054\u62db\u8058'}, 360264: {u'app_id': 360264, u'name': u'\u667a\u901a\u4eba\u624d'}, 360265: {u'app_id': 360265, u'name': u'\u767e\u57ce\u6c42\u804c\u5b9d'}, 191087: {u'app_id': 191087, u'name': u'\u5b9c\u4eba\u8d37\u501f\u6b3e'}, 191088: {u'app_id': 191088, u'name': u'\u4eba\u4eba\u8d37'}, 81798: {u'app_id': 81798, u'name': u'\u68c9\u82b1\u7cd6'}, 191063: {u'app_id': 191063, u'name': u'51\u4fe1\u7528\u5361\u7ba1\u5bb6'}, 81788: {u'app_id': 81788, u'name': u'\u5192\u6ce1'}}
    print(app_dic)
