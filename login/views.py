from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse
# import mysql.connector
# import MySQLdb
from django.views.decorators.csrf import csrf_exempt
from register.models import User


# Create your views here.
# connect the database
# def connect():
# 	# con = mysql.connector.connect("127.0.0.1",'root','lxlh10388844','UserProfile')
# 	con = MySQLdb.connect("127.0.0.1",'root','lxlh10388844','UserProfile')
# 	cursor = con.cursor()
# 	return con,cursor
# # close the database
# def close(db,cursor):
# 	db.close()
# 	cursor.close()
# login
@csrf_exempt
def login(request):
	if request.method == 'POST':
		user_name = request.POST.get('username')
		user_password = request.POST.get('password')
		same_name_objs = User.objects.filter(name=user_name)
		if len(same_name_objs) == 0: # 用户不在数据库中
			return render_to_response('login.html',{
				'error':'用户不存在'
				})
		else:
			the_user = User.objects.get(name = user_name)
			if user_password == the_user.password:# 登录成功 -----------------未完成 --------------
				return HttpResponseRedirect('../../index/index/%s'%user_name)
			else:
				return render_to_response('login.html',{
					'error':' 密码错误 ，请重新输入'
				})
	return render_to_response('login.html')