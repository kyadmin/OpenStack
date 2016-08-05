#_*_coding:utf-8_*_
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import models
import s3_api
import UserInfo
import time
from django.http import HttpResponse
import json
import re
# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')
    #return render(request, 'base.html')

@login_required
def lock_screen(request):
    print '-------------------------',request.GET

    print '===============',type(models.User.objects.get(username=request.user))
    u=models.User.objects.get(username=request.user)
    username=u.username
    email=u.email
    print ']]]]]]]]]]]]]]]]]]]',username,type(username)
    acount_logout(request)
    return render(request,'lock_screen.html',locals())

@login_required
def user_profile(request):
    active_2='user_profile'
    return render(request,'user_profile.html',locals())





def acount_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is None:
            log_err=u'用户名或密码错误'
        else:
            login(request,user)

            conn=conn_radosgw(username)
            global conn

            return HttpResponseRedirect('/')
        return render(request, 'login.html', locals())

@login_required
def acount_logout(request):
    try:
        del conn
    except Exception as e:
        pass
    logout(request)
    return render(request,'login.html')






#用户登录成功后获取对象存储的链接对象
def conn_radosgw(username):
    cmd_hook = UserInfo.paramiko_cmd()
    user_info = cmd_hook.user_info_get(username)

    access_key = user_info.s3_access_key
    secret_key = user_info.s3_secret_key
    radosgw_port = user_info.radosgw_port
    radosgw_host = user_info.radosgw_host
    connection_object=s3_api.CONNECTION(access_key,secret_key,radosgw_host,radosgw_port)


    return connection_object

@login_required
def oss(request):
    active_1='oss'
    bucket_list=[]
    bucket_all_object=conn.list_all_bucket()

    # bucket_list = [eval(b.get_key('create_info').get_contents_as_string()) for b in bucket_all_object]
    for b in bucket_all_object:
        try:
            # bucket_list.append(eval(b.get_key('create_info').get_contents_as_string()))
            bucket_list.append(b.get_key('create_info').metadata)
        except Exception as e:
            pass
    print '='*100,bucket_list
    for i in range(len(bucket_list))[::-1]:
        for j in range(i):
            if bucket_list[j]['createdate'] < bucket_list[j + 1]['createdate']:
                bucket_list[j], bucket_list[j + 1] = bucket_list[j + 1], bucket_list[j]
    print 'bucket_list is :',bucket_list
    return render(request,'oss.html',locals())

@login_required
def add_bucket(request):
    bucket_name=request.GET.get("bucketname")
    access=request.GET.get('access')
    zonename=request.GET.get('zonename')
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_date=time.strftime(ISOTIMEFORMAT, time.localtime())

    print bucket_name,access,zonename,create_date
    bucket_name=str(bucket_name)
    access=str(access)
    zonename=str(zonename)
    print type(bucket_name),type(access),type(zonename),type(create_date)
    feedback=conn.add_bucket(bucket_name,access,zonename,create_date)
    if not feedback:return HttpResponseRedirect('/oss/',{'tags':'limit_reached'})

    return HttpResponse('ok')



@login_required
def bucket_manage(request):
    print '---------------->',request.GET
    active_1='oss'
    bucket_name=request.GET.get("bucketname")
    # access=request.GET.get('access')
    # zonename=request.GET.get('zonename')
    # create_date=request.GET.get('create_date')


    # print bucket_name,access,zonename,create_date
    print bucket_name
    k=conn.get_object(bucket_name,'create_info')
    create_info=k.metadata
    return render(request,'bucket_manage1.html',locals())

@login_required
def check_bucket(request):
    print '--------------->>>>',request.GET.get('bucket_name')
    bucket_name=request.GET.get('bucket_name')
    res=conn.check_bucket(bucket_name)
    return HttpResponse(res)



