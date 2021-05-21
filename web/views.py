from django.http import HttpResponse
import json
from django.shortcuts import render

def Login(request):
    # 输入用户名提交后返回"hello,用户名"
    if request.method == "POST":
        username = request.POST.get('username')
        return HttpResponse("hello," + username)
    else:  # 初始登录时返回一个静态登录页面
        return render(request, 'login.html')


def Index(request):
    # 输入用户名提交后返回"hello,用户名"
    if request.method == "POST":
        username = request.POST.get('username')
        return HttpResponse("hello," + username)
    else:  # 初始登录时返回一个静态登录页面
        return render(request, 'index.html')


def LoginByGet(request):
    if request.method == "GET":
        result = {}  # 先指定一个字典
        user = request.GET.get('user')
        mobile = request.GET.get('mobile')
        date = request.GET.get('date')
        result['user'] = user
        result['mobile'] = mobile
        result['date'] = date
        result = json.dumps(result)
        # 指定返回数据类型为json且编码为utf-8
        return HttpResponse(result, content_type='application/json;charset=utf-8')
