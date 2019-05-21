
from django.shortcuts import render,render_to_response
# Create your views here.

def hello(request,name):
	return render_to_response('index.html',{
		'name',name
	})
def index(request,name):
	return render_to_response('index.html',{
		'name':name
	})
def main(request):
	return render_to_response('index.html')
