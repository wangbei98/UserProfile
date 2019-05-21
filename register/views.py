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
def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')
        # return HttpResponse(user_name)
        same_name_obj = User.objects.filter(name= user_name)
        print(len(same_name_obj))
        if len(same_name_obj) == 0:# 用户未注册
            new_user = User(name = str(user_name),password = str(user_password))
            new_user.save()
            return HttpResponse("<p>  注册成功! </p> ")
        else:
            return render_to_response('register.html',{
                'error':'用户已存在，请重新输入'
            })
    return render_to_response('register.html')
