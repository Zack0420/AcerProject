from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator
from .models import Trip
from .forms import PriceRangeForm
import pandas as pd
import numpy as np




# Create your views here.


#csv轉db
def import_data_from_csv(request):
    # csv_file_path = r'C:\Users\user\Desktop\trip_django\mysite\csv\all.csv'
    csv_file_path = r"C:\Users\han\Desktop\Project0614\mysite\csv\DomesticTravelInfo.csv"

    # 使用 pandas 读取 CSV 文件
    data = pd.read_csv(csv_file_path, encoding="UTF-8")

    # 将空字符串替换为 NaN
    data['price'] = data['price'].copy().replace(np.nan, None)
    data['duration'] = data['duration'].copy().replace(np.nan, None)

    # # 确保 price 和 duration 列为浮点数类型
    # data['price'] = data['price'].astype(float)
    # data['duration'] = data['duration'].astype(float)

    # 将 NaN 替换为 None，这样在导入数据库时会被识别为 NULL
    # data['price'] = data['price'].where(pd.isnull(data['price']), None)
    # data['duration'] = data['duration'].where(pd.isnull(data['duration']), None)


    for index, row in data.iterrows():
        trip_instance = Trip(
            travel_company=row['travel_company'],
            area=row['area'],
            title=row['title'],
            price=row['price'],
            date=row['date'],
            departure_city=row['departure_city'],
            duration=row['duration'],
            remaining_quota=row['remaining_quota'],
            tour_schedule=row['tour_schedule'],
            url=row['url']
        )
        trip_instance.save()
    # for row in csv_reader:
    #     price_str = row['price'].replace(',', '')  # 移除逗号
    #     lion_instance = Lion(
    #         no = row['no'],
    #         company_Name = row['company_Name'],  # 通常使用小写字母加下划线的形式来命名字段
    #         area = row['area'],
    #         title = row['title'],
    #         url = row['url'],
    #         trip_type = row['trip_type'],
    #         fromDate = row['fromDate'],  # 同样使用小写字母加下划线的形式
    #         trip_number = row['trip_number'],
    #         group_total = row['group_total'],
    #         saleable = row['saleable'],
    #         after_saleable = row['after_saleable'],
    #         group_state = row['group_state'],
    #         traffic_information = row['traffic_information'],
    #         trip_information = row['trip_information'],
    #         total_Date = row['total_Date'],
    #         # price = row['price'],
    #         price = price_str,
    #         hotel = row['hotel'],)

    return HttpResponse("新增成功")

def area(request): #地區分類
    global city, current_url
    results = None
    post_page_obj = None
    if request.method == 'GET':
        #用GET抓取區域分類
        city = request.GET["city"]
        if not Lion.objects.filter(area=city):
            return HttpResponseBadRequest("Missing 'city' parameter")
        print(city)
        #用GET抓取區域分類

        #根據當前的HTTP請求擷取網址
        current_url = request.build_absolute_uri()
        print(current_url)
        #根據當前的HTTP請求擷取網址

        #初始化表單
        form = PriceRangeForm()
        selected_options = request.POST.getlist('options')
        #初始化表單

        #篩選結果
        search_result_all_item = Lion.objects.filter(area=city).exclude(price=0).order_by('price')
        #篩選結果

        # 分頁功能
        paginator = Paginator(search_result_all_item, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        results = len(search_result_all_item)
        # 分頁功能

    else:
        return search_results(request)

    return render(request, 'trip/area_result.html', {current_url:'current_url','city':city,'form': form,"search_result_all_item":search_result_all_item,
                                                           "selected_options":selected_options,"results":results,
                                                           'page_obj': page_obj,'post_page_obj':post_page_obj
                                                           })


def search_results(request):
    global  selected_options, price1, price2, form, results_between_prices, current_url

    if request.method == 'POST':
        print("POST")
        # city = request.GET["city"]
        #天數表單篩選
        selected_options = request.POST.getlist('options')
        selected_options = [int(option) for option in selected_options]
        for option in selected_options:
            print(f"option:{option}")
        #天數表單篩選

        current_url = request.build_absolute_uri()
        print(current_url)

        #價格區間
        form = PriceRangeForm(request.POST)
        if form.is_valid():
            price1 = form.cleaned_data['price1']
            price2 = form.cleaned_data['price2']
            # day = form.cleaned_data['day']
        #價格區間

        # 确保 price1 小于 price2
        if price1 > price2:
            price1, price2 = price2, price1
        results_between_prices = Lion.objects.filter(area=city).filter(price__gt=price1, price__lt=price2).order_by('price')


    results = len(results_between_prices)


    if request.method == 'GET':
        # form = PriceRangeForm()
        current_url = request.build_absolute_uri()
        print(current_url)


    # 分頁功能
    paginator = Paginator(results_between_prices, 10)
    post_page_number = request.GET.get('page')
    post_page_obj = paginator.get_page(post_page_number)
    # 分頁功能


    return render(request, 'trip/search_result.html', {'city':city,'form': form,"results_between_prices":results_between_prices,
                                                           "selected_options":selected_options,"results":results,
                                                           'post_page_obj':post_page_obj
                                                           })


def add_to_itinerary(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        print(title)
        print(price)
        # 做一些檢查和處理，然後將資料儲存到資料庫
        Lion_save.objects.create(title=title, price=price)
        print(current_url)
        return redirect(current_url)
    else:
        return HttpResponse('僅接受POST請求')

def delete_from_itinerary(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        if item_id:
            item = get_object_or_404(Lion_save, id=item_id)
            item.delete()
            # print(current_url)
            return redirect("http://127.0.0.1:8000/myapp/personal_page/")
    else:
        return HttpResponse('僅接受POST請求')


def personal_page(request):

    if "username" in request.COOKIES.keys():

        results = Lion_save.objects.order_by('price')
        if request.method == 'POST':
            title = request.POST.get('title')
            price = request.POST.get('price')
            Lion_save.delete(title=title, price=price)
            # print(current_url)
            # return redirect(current_url)
        # else:
        #     return HttpResponse('僅接受POST請求')

        return render(request, 'trip/personal.html', {'results':results})

    else:

        return redirect("loginForm")


