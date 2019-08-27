from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Min, Max, Avg

from mainapp.models import UserEntity, FruitEntity, StoreEntity


# Create your views here.

def user_list(request):
    datas = [
        {'id': 101, 'name': '王杰超'},
        {'id': 102, 'name': '王宇辰'},
        {'id': 103, 'name': '王栋平'},
    ]
    return render(request,
                  'user/list.html',
                  {
                      'users': datas,
                      'msg': '最优秀的学员'
                  })


def user_list2(request):
    users = [
        {'id': 101, 'name': '王杰超'},
        {'id': 102, 'name': '王宇辰'},
        {'id': 103, 'name': '王栋平'},
    ]
    msg = '最优秀的学员'
    return render(request,
                  'user/list.html', locals())

def add_user(request):
    # 从GET请求中读取数据
    # request.GET.get('name')

    # reqeust.GET 是一个dict字典类型，保存的是查询参数
    name = request.GET.get('name', None)
    age = request.GET.get('age', 0)
    phone = request.GET.get('phone', None)


    # 验证是否数据是否完整
    if not all((name, age, phone)):
        return HttpResponse('<h3 style="color:red">请求参数不完整</h3>',
                            status=400)

    u1 = UserEntity()
    u1.name = name
    u1.age = age
    u1.phone = phone
    u1.save()
    return redirect('/user/list')

def update_user(request):
    # 查询参数有id, name, phone
    id = request.GET.get('id', None)
    if not id:
        return HttpResponse('id参数必须提供', status=400)

    # 通过模型查询id的用户是否存在(表中的数据（记录）是否存在)
    try:
        # Model类.objects.get() 可能会报异常-- 尝试捕获
        user = UserEntity.objects.get(pk=int(id))

        name = request.GET.get('name', None)
        phone = request.GET.get('phone', None)
        if any((name, phone)): # name 或 phone 任意一个存在即可
            if name:
                user.name = name

            if phone:
                user.phone = phone

            user.save()
            return redirect('/user/list')

    except:
        return HttpResponse('%s 的用户是不存在的' % id,
                            status=404)

def delete_user(request):
    # 查询参数有id
    id = request.GET.get('id')
    # 验证id是否存在
    if id:
        try:
            user = UserEntity.objects.get(pk=int(id))
            user.delete()
            html = """
            <p>
            %s 删除成功!  三秒后自动跳转到<a href="/user/list">列表</a>
            </p>
            <script>
                setTimeout(function(){
                    open('/user/list', target='_self');
                }, 3000)
            </script>
            """ % id
            return HttpResponse(html)
        except:
            return HttpResponse('%s 不存在' %id)
    else:
        return HttpResponse('必须提供id参数')

def user_list3(request):
    users = UserEntity.objects.all()
    msg = '最优秀的学员'
    return render(request,
                  'user/list.html', locals())

def find_fruit(request):
    # 从查询参数中获取价格区间[price1, price2]
    price1 = request.GET.get('price1', 0)
    price2 = request.GET.get('price2', 1000)

    # 根据价格区别查询满足条件所有水果信息
    fruits = FruitEntity.objects.filter(price__gte=price1,
                                        price__lte=price2)\
        .exclude(price=250)\
        .filter(name__contains='果') \
        .all()

    # 将查询的数据渲染到html模板中
    return render(request, 'fruit/list.html', locals())

def find_store(request):
    # 查询2019年开业的水果店
    # 查询参数： year, month
    queryset = StoreEntity.objects.filter(create_time__month__lt=6).order_by('-id', 'city')

    first_store = queryset.first()  # 模型类的实例对象
    print(first_store)
    stores = queryset.all().filter(city='西安')  # ?? 返回还是queryset吗?
    return render(request,'store/list.html', locals())

def all_store(request):
    # 返回所有水果店的json 数据
    result = {}
    if StoreEntity.objects.exists():
        datas = StoreEntity.objects.values()
        print(type(datas))  # list[{}, {}] ??  QuerySet<{}, {}>

        store_list = []
        for store in datas:
            store_list.append(store)

        result['data'] = store_list
        result['total'] = StoreEntity.objects.count()

    else:
        result['msg'] = '数据是空的'

    return JsonResponse(result)

def count_fruit(request):
    # 返回json数据： 统计每种分类的水果数量 、最高价格、最低价格和总价格
    result = FruitEntity.objects.aggregate(cnt=Count('name'),
                                           max=Max('price'),
                                           min=Min('price'),
                                           avg=Avg('price'),
                                           total=Sum('price'))
    return JsonResponse(result)
