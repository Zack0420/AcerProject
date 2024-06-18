from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator
from .models import Trip, User_save
from member.models import Member
from .forms import PriceRangeForm, PersonalPageForm, PeriodForm
import pandas as pd
import numpy as np
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
from dateutil.relativedelta import *




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
        username = request.COOKIES['username']
        results = User_save.objects.filter(username = username).order_by('date')
        data = []
        for i in results:
            plan = {}
            plan['username'] = i.username
            plan['title'] = i.title
            plan['travel_company'] = i.travel_company
            plan['area'] = i.area
            plan['price'] = i.price
            plan['date'] = i.date
            plan['departure_city'] = i.departure_city
            plan['duration'] = i.duration
            plan['remaining_quota'] = i.remaining_quota
            plan['url'] = i.url
            plan['days'] = []
            
            for key, value in eval(i.tour_schedule).items():
                temp = {}
                temp['day'] = key
                temp['schedule'] = list(value['schedual'])
                temp['hotel'] = list(value['posible_hotel'])
                plan['days'].append(temp)

            data.append(plan)

        return render(request, 'trip/personal_schedule.html', {"data": data})
    
    else:

        return redirect('login')

    

def user_save_delete(request):

    if request.method == "POST":

        personalForm = PersonalPageForm(request.POST)

        if personalForm.is_valid():

            username = personalForm.cleaned_data['username']
            title = personalForm.cleaned_data['title']
            company = personalForm.cleaned_data['company']
            date = personalForm.cleaned_data['date']
            
            plan = User_save.objects.get(username = username, title = title, travel_company = company, date = date)
            User_save.objects.get(id =plan.id).delete()

        else:

            personalForm = PersonalPageForm()

    return redirect("personal_page")

def sendemail(request):

    if request.method == "POST":
        personalForm = PersonalPageForm(request.POST)
        if personalForm.is_valid():
            username = personalForm.cleaned_data['username']
            title = personalForm.cleaned_data['title']
            company = personalForm.cleaned_data['company']
            date = personalForm.cleaned_data['date']
            print(username, repr(title), company, date)
            
            data = User_save.objects.get(username = username,travel_company = company, date = date, title = title)
            print(repr(data.title))
            plan = {}
            plan['username'] = data.username
            plan['title'] = data.title
            plan['travel_company'] = data.travel_company
            plan['area'] = data.area
            plan['price'] = data.price
            plan['date'] = data.date
            plan['departure_city'] = data.departure_city
            plan['duration'] = data.duration
            plan['remaining_quota'] = data.remaining_quota
            plan['url'] = data.url
            plan['days'] = []
        
            for key, value in eval(data.tour_schedule).items():
                temp = {}
                temp['day'] = key
                temp['schedule'] = list(value['schedual'])
                temp['hotel'] = list(value['posible_hotel'])
                plan['days'].append(temp)

            emailto = Member.objects.get(username = username).email
            html = get_template('trip/email.html')
            subject, from_email, to = 'Welcome to app', '2024acergroup1@gmail.com', emailto
            text_content = 'Verify your email!'
            html_content = '<a href = "http://127.0.0.1:8000/member/change_verifiction_status/%s">Pleask click here to verify your email!</p>'%username
            html_content = render_to_string('trip/email.html', {'plan':plan})
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        else:

            personalForm = PersonalPageForm()

    return redirect("personal_page")

def period_changed(request):

    if "username" in request.COOKIES.keys():
        if request.method == "POST":
            periodForm = PeriodForm(request.POST)
            if periodForm.is_valid():
                period = periodForm.cleaned_data['period']
                username = request.COOKIES['username']
                today = datetime.datetime.now().strftime("%Y/%m/%d")
                dt = datetime.datetime.strptime(today, "%Y/%m/%d")
                results = User_save.objects.filter(username = username).order_by('date')

                if period == "一周內":

                    after_a_week = dt + relativedelta(days =+7)
                    list_range = []
                
                    for n, i in enumerate(results):
                        data_date = datetime.datetime.strptime(i.date, "%Y/%m/%d")
                        if data_date < after_a_week and data_date >= dt:
                            list_range.append(n)
                    
                    results = results[list_range[0]:list_range[-1]+1]


                elif period == "一個月內":

                    after_a_month = dt + relativedelta(months =+1)
                    list_range = []

                    for n, i in enumerate(results):
                        data_date = datetime.datetime.strptime(i.date, "%Y/%m/%d")
                        if data_date < after_a_month and data_date >= dt:
                            list_range.append(n)
                    results = results[list_range[0]:list_range[-1]+1]

                elif period == "一年內":

                    after_a_year = dt + relativedelta(years =+1)
                    list_range = []

                    for n, i in enumerate(results):
                        data_date = datetime.datetime.strptime(i.date, "%Y/%m/%d")
                        if data_date < after_a_year and data_date >= dt:
                            list_range.append(n)
                    results = results[list_range[0]:list_range[-1]+1]

                data = []
                for i in results:
                    plan = {}
                    plan['username'] = i.username
                    plan['title'] = i.title
                    plan['travel_company'] = i.travel_company
                    plan['area'] = i.area
                    plan['price'] = i.price
                    plan['date'] = i.date
                    plan['departure_city'] = i.departure_city
                    plan['duration'] = i.duration
                    plan['remaining_quota'] = i.remaining_quota
                    plan['url'] = i.url
                    plan['days'] = []
                    
                    for key, value in eval(i.tour_schedule).items():
                        temp = {}
                        temp['day'] = key
                        temp['schedule'] = list(value['schedual'])
                        temp['hotel'] = list(value['posible_hotel'])
                        plan['days'].append(temp)

                    data.append(plan)

                return render(request, 'trip/personal_schedule.html', {"data": data})
            else:

                periodForm = PeriodForm()

    else:

        return redirect('login')


    
   



    
    
        

