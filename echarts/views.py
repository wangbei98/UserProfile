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


# from pyecharts.constants import DEFAULT_HOST # 这句会报错
REMOTE_HOST = 'http://chfw.github.io/jupyter-echarts/echarts'#加上这句

# def charts(request):
#     template = loader.get_template('charts/pyecharts.html')
#     l3d = line3d()
#     context = dict(
# 		myechart=l3d.render_embed(),
# 		host=REMOTE_HOST,
# 		script_list=l3d.get_js_dependencies()
#     )
#     return HttpResponse(template.render(context, request))
def line3d():
	_data = []
	for t in range(0, 25000):
		_t = t / 1000
		x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
		y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
		z = _t + 2.0 * math.sin(75 * _t)
		_data.append([x, y, z])
	range_color = [
		'#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
		'#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
	line3d = Line3D("3D line plot demo", width=1200, height=600)
	line3d.add("", _data, is_visualmap=True,
			   visual_range_color=range_color, visual_range=[0, 30],
			   is_grid3D_rotate=True, grid3D_rotate_speed=180)
	return line3d

app_tab = pd.read_csv('/Users/bellick/MyProjects/UserProfile/data/appTab.txt',encoding='gb18030',sep='|',names=['app_id','name','male','female','_24','25_30','31_35','36_40','40_'])
app_tab = app_tab.set_index('app_id')
user_data = pd.read_csv('/Users/bellick/MyProjects/UserProfile/data/userdata_new.txt',sep='|',names = ['tel','app_id','date','time'])


@csrf_exempt
def charts(request):
	if  request.method == "POST":
		app_id = int(request.POST.get('app_id'))
		template = loader.get_template('charts/pyecharts.html')
		gender_pie = gender_rate(app_tab,app_id)
		age_pie = age_distribution(app_tab,app_id)
		context = dict(
			host=REMOTE_HOST,
			myechart_gender = gender_pie.render_embed(),
			script_list_gender=gender_pie.get_js_dependencies(),
			myechart_age=age_pie.render_embed(),
			script_list_age=age_pie.get_js_dependencies()
		)
		return HttpResponse(template.render(context, request))
	return render_to_response('charts/pyecharts.html')
def get_name(id):
    return app_tab.loc[id,'name']

def gender_rate(app_tab,app_id):
    gender_data = app_tab.loc[[app_id],['male','female']]
    gender_data = np.array(gender_data).flat
    attr = ['male','female']
    v1 = gender_data
    pie = Pie(get_name(app_id)+"男女比例")
    pie.add("", attr, v1, is_label_show=True)
    return pie
def age_distribution(app_tab,app_id):
    age_data = app_tab.loc[[app_id],['_24','25_30','31_35','36_40','40_']]
    age_data = np.array(age_data).flat
    attr = ['24岁以下','25-30岁','31-35岁','36-40岁','40岁以上']
    v1 = age_data
    pie = Pie(get_name(app_id)+"年龄分布")
    pie.add("", attr, v1, is_label_show=True)
    return pie