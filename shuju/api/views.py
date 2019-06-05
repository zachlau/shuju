from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
import json
from api.models import *
from django.contrib import auth
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import codecs, csv, os, sys
# Create your views here.
def login(requests):
    return render(requests, 'login.html')

def api_login(requests):
    username = requests.POST.get('username')
    password = requests.POST.get('password')
    if username and password:
        user = auth.authenticate(username=username, password=password)
        if user:
            res = render(requests, 'home.html')
            token = Token.objects.get(user=user).key
            uid = User.objects.get(username=username).id
            res.set_cookie('uid',uid ,max_age=None)
            res.set_cookie('token', token, max_age=None)
            return res
        else:
            return HttpResponse('用户名或密码错误!')
    else:
        return HttpResponse('参数错误!')

@require_http_methods(['GET'])
def get_city(requests):
    b = bizcircle.objects.all().values('city_id', 'city_name').distinct()
    print(b)
    l = []
    for c in b:
        l.append({'id': c.get('city_id'), 'name': c.get('city_name')})
    return JsonResponse({"city": l})

@require_http_methods(['POST'])
def get_salesMonthly(requests):
    uid = requests.COOKIES.get('uid')
    token = requests.COOKIES.get('token')
    if uid and token:
        if not Token.objects.filter(key=token, user_id=uid).exists():
            return JsonResponse({"error_msg": "登录失败!"})
    else:
        return JsonResponse({"error_msg": "未登录!"})

    try:
        data = json.loads(requests.body)
        month = int(data.get('month'))
        city = data.get('city')
    except:
        return JsonResponse({"error_msg": "请求参数格式错误!"})

    if month and city:
        if month in range(1, 13):
            if month in (1,3,5,7,8,10,12):
                end_time = '2019-%d-31'%month
            elif month in (4,6,9,11):
                end_time = '2019-%d-30'%month
            else:
                end_time = '2019-%d-28'%month
            city_name = bizcircle.objects.filter(city_id=city).first()
            if city_name:
                orders = order.objects.filter(sign_time__gte='2019-%d-01'%month, sign_time__lte=end_time, city_id=city)
                if orders.count() > 0:
                    total = 0.0
                    for o in orders:
                        total += o.final_price
                    return JsonResponse({"city": city_name.city_name, "count": orders.count(), "total": round(total/10000, 2)})
                else:
                    return JsonResponse({"error_msg": "本月该地区，无销售记录", "total": 0})
            else:
                return JsonResponse({"error_msg": "城市编号错误!"})
        else:
            return JsonResponse({"error_msg": "月份格式错误!"})
    else:
        return JsonResponse({"error_msg": "缺少必要参数month或city"})

@require_http_methods(['POST'])
def get_signDetails(requests):
    uid = requests.COOKIES.get('uid')
    token = requests.COOKIES.get('token')
    if uid and token:
        if not Token.objects.filter(key=token, user_id=uid).exists():
            return JsonResponse({"error_msg": "登录失败!"})
    else:
        return JsonResponse({"error_msg": "未登录!"})

    try:
        data = json.loads(requests.body)
        month = int(data.get('month'))
        city = data.get('city')
    except:
        return JsonResponse({"error_msg": "请求参数格式错误!"})

    if month and city:
        if month in range(1, 13):
            if month in (1,3,5,7,8,10,12):
                end_time = '2019-%d-31'%month
            elif month in (4,6,9,11):
                end_time = '2019-%d-30'%month
            else:
                end_time = '2019-%d-28'%month
            city_name = bizcircle.objects.filter(city_id=city).values('city_name').first()
            if city_name:
                orders = order.objects.filter(sign_time__gte='2019-%d-01'%month, sign_time__lte=end_time, city_id=city)
                orders_list = []
                if orders.count() > 0:
                    for o in orders:
                        frame_area = room.objects.filter(id=o.room_id).first().frame_area
                        orders_list.append({'customer': o.customer_id, 'final_price': o.final_price/10000,
                                            'frame_area': frame_area, 'avg_price':  round(o.final_price/frame_area, 2)})
                    return JsonResponse({"city": city_name.get('city_name'), "month": month, "count": orders.count(), "details": orders_list})
                else:
                    return JsonResponse({"error_msg": "本月该地区，无销售记录"})
            else:
                return JsonResponse({"error_msg": "城市编号错误!"})
        else:
            return JsonResponse({"error_msg": "月份格式错误!"})
    else:
        return JsonResponse({"error_msg": "缺少必要参数month或city"})

@require_http_methods(['GET'])
def export(requests):
    uid = requests.COOKIES.get('uid')
    token = requests.COOKIES.get('token')
    if uid and token:
        if not Token.objects.filter(key=token, user_id=uid).exists():
            return JsonResponse({"error_msg": "登录失败!"})
    response = HttpResponse(content_type='text/csv;charset=UTF-8')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'
    writer = csv.writer(response)
    writer.writerow(['用户身份证信息', '房屋总价', '平米数', '平均价'])
    try:
        month = int(requests.GET.get('month'))
    except:
        month = 0
    city = requests.GET.get('city')
    if month and city:
        if month in range(1, 13):
            if month in (1,3,5,7,8,10,12):
                end_time = '2019-%d-31'%month
            elif month in (4,6,9,11):
                end_time = '2019-%d-30'%month
            else:
                end_time = '2019-%d-28'%month
            city_name = bizcircle.objects.filter(city_id=city).values('city_name').first()
            if city_name:
                orders = order.objects.filter(sign_time__gte='2019-%d-01'%month, sign_time__lte=end_time, city_id=city)
                # orders_list = []
                if orders.count() > 0:
                    for o in orders:
                        frame_area = room.objects.filter(id=o.room_id).first().frame_area
                        # orders_list.append({'customer': o.customer_id, 'final_price': o.final_price/10000,
                        #                     'frame_area': frame_area, 'avg_price':  round(o.final_price/frame_area, 2)})
                        writer.writerow([o.customer_id, o.final_price/10000, frame_area, round(o.final_price/frame_area, 2)])
                    return response
                else:
                    return JsonResponse({"error_msg": "本月该地区，无销售记录"})
            else:
                return JsonResponse({"error_msg": "城市编号错误!"})
        else:
            return JsonResponse({"error_msg": "月份格式错误!"})
    else:
        return JsonResponse({"error_msg": "缺少必要参数month或city"})

@require_http_methods(['POST'])
def uploadFile(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join(sys.path[0] + "/save", myFile.name), 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse("upload over!")