import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import DateValidation 
from datetime import datetime
import re
import time

current_datetime = datetime.now()

"""
    功能: 初始設定 ChromeOptions
    參數:
        maximize: 網頁視窗最大化
        incognito: 設置無痕模式
        headless: 設置無頭模式
        extension: 設置是否禁用Chrome之擴展功能。如果為True，則禁用。
        popup_blocking: 設置是否禁用瀏覽器之彈出窗口。如果為True，則禁用。
    備註: 無
"""
def init_driver(maximized = False, incognito = False, headless = False, extension = False, popup_blocking = False):
    
    chrome_opt = Options()
    
    if maximized:
        chrome_opt.add_argument("start-maximized")
        
    if incognito:
        chrome_opt.add_argument("--incognito")
        
    if headless:
        chrome_opt.add_argument("--headless")
    
    if extension:
        chrome_opt.add_argument("disable-extensions")
        
    if popup_blocking:
        chrome_opt.add_argument("disable-popup-blocking")
    
    driver = webdriver.Chrome(options = chrome_opt)
    print("driver設置完成")
    return driver

"""
    功能: 爬取可樂旅遊國內團體行程
    參數:
        StartTourDate: 出發時間，預設為當日
    備註: 無
"""
def domestic_traveling_plan_url(object, date = str(current_datetime.year)+'/'+str(current_datetime.month)+'/'+str(current_datetime.day + 1)):
    
    links = []
    controler = True
    url = 'https://www.colatour.com.tw/C10A_TourSell/C10A02_TourQuery.aspx?DepartureCity=*&RegionCode=O&StartTourDate='+date+'&TourType=全部&bound=in'
    object.get(url)
    
    try:
        
        object.find_element(By.ID, 'noTourData')
        
    except:
        print('No Tour Data')
        return 
    
    while controler:
        
        try:
            
            WebDriverWait(object, 10, 0.5).until(EC.visibility_of(object.find_element(By.ID, 'dataT-Main')))
            
        except:
            
            print('The element not found')
            return
        
        currentPage = object.find_element(By.CLASS_NAME, 'current').text
        lastPage = object.find_elements(By.XPATH, '//*[@id="PageSelector"]/ul/li')[-1].get_attribute('data-value')
        print(currentPage)
        
        if currentPage == lastPage:
            
            controler = False
       
        plans = object.find_elements(By.XPATH, '//*[@id="dataT-Main"]/ul/li')
            
        for i in plans[1:]:
                
            tourCode = i.find_element(By.CLASS_NAME, 'dataT-titleNum').text
            tourTime = str(current_datetime.year) + '/' + i.find_element(By.CLASS_NAME, 'dataT-date').find_element(By.TAG_NAME, 'span').text.split("(")[0]
            url = 'https://www.colatour.com.tw/C10A_TourSell/C10A13_TourItinerary.aspx?TourDate={}&TourCode={}'.format(tourTime, tourCode)
            links.append(url)
            
        ActionChains(object).click(object.find_element(By.XPATH, '//*[@id="tq-dataTourjs"]/div[4]/div[1]/btn[2]')).perform()
        
    with open('urls.txt', 'w', encoding='UTF-8') as file:
        
        for i in links:
            
            file.write(i)
            file.write('\n')
    
    return links

def import_url():
    
    with open('urls.txt', 'r', encoding="UTF-8") as file:
        
        urlList = file.read().split('\n')[:-1]
        return urlList

"""
    功能: 爬取國內團體行程詳細資訊
    參數:
        國內團體行程頁面url串列
    備註: 無
"""
def get_one_info(url):
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    
    response = requests.get(url, headers=headers)
    
    soup = bs(response.text, 'html.parser')
    
    info_dict = {}
    
    title = soup.find('div', {'class': 'tourtit-mdataTitle'}).text
    info_dict['title'] = title
    
    date = soup.find('div', {'class': 'mdataInfo-dateDetail'}).find_all('span')[0].text.split(' ')[0]
    info_dict['date'] = date
    
    departure_city = soup.find('div', {'class': 'mdataInfo-dateDetail'}).find_all('span')[0].text.split(' ')[1]
    info_dict['departure_city'] = departure_city
    
    duration = soup.find('div', {'class': 'mdataInfo-dateDetail'}).find_all('span')[1].text
    info_dict['duration'] = duration
    
    price = soup.find('a', {'class': 'iframe-itinerarySmall'}).text
    info_dict['price'] = price
    
    group_quota = soup.find('div', {'id': 'mdataInfo-dateDetail'}).find('span').find_all('span')[0].text.split(' ')[1]
    info_dict['group_quota'] = group_quota
    
    remaining_quota = soup.find('div', {'id': 'mdataInfo-dateDetail'}).find('span').find_all('span')[1].text.split(' ')[1]
    info_dict['remaining_quota'] = remaining_quota
    
    waiting = soup.find('div', {'id': 'mdataInfo-dateDetail'}).find('span').find_all('span')[2].text.split(' ')[1]
    info_dict['waitingList'] = waiting
    
    try:
        
        soup.find('div', {'class': 'touriti-flightOut'}).find('div', {'class':'ui-title'})
        
        go_date = soup.find('ul', {'class': 'flightR-go'}).find_all('div')[0].text.lstrip().rstrip()
        info_dict['go_date'] = go_date
        
        go_company = soup.find('ul', {'class': 'flightR-go'}).find_all('div')[1].find_all('span')[0].text
        info_dict['go_company'] = go_company
        
        go_flightNo = soup.find('ul', {'class': 'flightR-go'}).find_all('div')[1].find_all('span')[1].text
        info_dict['go_flightNo'] = go_flightNo
        
        go_departure_time = soup.find('ul', {'class': 'flightR-go'}).find_all('div')[2].find_all('span')[0].text
        info_dict['go_departure_time'] = go_departure_time
        
        go_departure_city = soup.find('ul', {'class': 'flightR-go'}).find_all('div')[2].find_all('span')[1].text
        info_dict['go_departure_city'] = go_departure_city
        
        go_arrive_time = soup.find('ul', {'class': 'flightR-go'}).find_all('div')[3].find_all('span')[0].text
        info_dict['go_arrive_time'] = go_arrive_time
        
        go_arrive_city = soup.find('ul', {'class': 'flightR-go'}).find_all('div')[3].find_all('span')[1].text
        info_dict['go_arrive_city'] = go_arrive_city
        
        back_date = soup.find('ul', {'class': 'flightR-back'}).find_all('div')[0].text.lstrip().rstrip()
        info_dict['back_date'] = back_date
        
        back_company = soup.find('ul', {'class': 'flightR-back'}).find_all('div')[1].find_all('span')[0].text
        info_dict['back_company'] = back_company
       
        back_flightNo = soup.find('ul', {'class': 'flightR-back'}).find_all('div')[1].find_all('span')[1].text
        info_dict['back_flightNo'] = back_flightNo
        
        back_departure_time = soup.find('ul', {'class': 'flightR-back'}).find_all('div')[2].find_all('span')[0].text
        info_dict['back_departure_time'] = back_departure_time
        
        back_departure_city = soup.find('ul', {'class': 'flightR-back'}).find_all('div')[2].find_all('span')[1].text
        info_dict['back_departure_city'] = back_departure_city
        
        back_arrive_time = soup.find('ul', {'class': 'flightR-back'}).find_all('div')[3].find_all('span')[0].text
        info_dict['back_arrive_time'] = back_arrive_time
        
        back_arrive_city = soup.find('ul', {'class': 'flightR-back'}).find_all('div')[3].find_all('span')[1].text
        info_dict['back_arrive_city'] = back_arrive_city
    
    except:
        
        info_dict['go_date'] = ""
        
        info_dict['go_company'] = ""
        
        info_dict['go_flightNo'] = ""
        
        info_dict['go_departure_time'] = ""
        
        info_dict['go_departure_city'] = ""
        
        info_dict['go_arrive_time'] = ""
        
        info_dict['go_arrive_city'] = ""
        
        info_dict['back_date'] = ""
        
        info_dict['back_company'] = ""
       
        info_dict['back_flightNo'] = ""
        
        info_dict['back_departure_time'] = ""
        
        info_dict['back_departure_city'] = ""
        
        info_dict['back_arrive_time'] = ""
        
        info_dict['back_arrive_city'] = ""
    
    
    if re.compile('自由行').search(title) != None:
        
        info_dict['type'] = "自由行"
        
    else:
        
        info_dict['type'] = "套裝行程"
        
    tour_schedual= {}
    
    for i in soup.find_all('div', {'class':'touriti-dlineBox'}):
         
        place_List = []
        
        hotel_List = []
        
        day = i.find('div', {'class': 'dlineTitle-day'}).text.replace('\n',' ').lstrip()
        
        for p in i.find('div', {'class': 'dlineTitle-place'}).find_all('p'):
            
            place_List.append(p.text)
        
        for h in i.find('div', {'class': 'dlineContent-hotel'}).find('ul').find_all('li'):
            
            hotel_List.append(h.text)
        
        
        tour_schedual[day] = {'schedual': place_List, 'posible_hotel': hotel_List}
    
    info_dict['tour_schedual'] = tour_schedual
    
    return info_dict

def get_all_plans_info():
    
    title_List = []
    date_List= []
    departure_city_List = []
    duration_List = []
    price_List = []
    group_quota_List = []
    remaining_quota_List = []
    waiting_List = []
    
    go_date_List = []
    go_company_List = []
    go_flightNo_List = []
    go_departure_time_List = []
    go_departure_city_List = []
    go_arrive_time_List = []
    go_arrive_city_List = []
    
    back_date_List = []
    back_company_List = []
    back_flightNo_List = []
    back_departure_time_List = []
    back_departure_city_List = []
    back_arrive_time_List = []
    back_arrive_city_List = []
    
    tour_schedual_List = []
    tour_type_List = []
    
    urlList = import_url()
    
    try:

        for index, url in enumerate(urlList):
            
            print(index + 1)
            
            try:
                info = get_one_info(url)
            
            except Exception as error:
                
                print(index+1)
                print(error)
                return 
            
            title_List.append(info['title'])
            date_List.append(info['date'])
            departure_city_List.append(info['departure_city'])
            duration_List.append(info['duration'])
            price_List.append(info['price'])
            group_quota_List.append(info['group_quota'])
            remaining_quota_List.append(info['remaining_quota'])
            waiting_List.append(info['waitingList'])
            
            go_date_List.append(info['go_date'])
            go_company_List.append(info['go_company'])
            go_flightNo_List.append(info['go_flightNo'])
            go_departure_time_List.append(info['go_departure_time'])
            go_departure_city_List.append(info['go_departure_city'])
            go_arrive_time_List.append(info['go_arrive_time'])
            go_arrive_city_List.append(info['go_arrive_city'])
            
            back_date_List.append(info['back_date'])
            back_company_List.append(info['back_company'])
            back_flightNo_List.append(info['back_flightNo'])
            back_departure_time_List.append(info['back_departure_time'])
            back_departure_city_List.append(info['back_departure_city'])
            back_arrive_time_List.append(info['back_arrive_time'])
            back_arrive_city_List.append(info['back_arrive_city'])
            tour_schedual_List.append(info['tour_schedual'])
            tour_type_List.append(info['type'])
            
            time.sleep(3)
    
    finally:
        
        all_info = pd.DataFrame({'title':title_List,
                                 'date':date_List,
                                 'departure_city':departure_city_List,
                                 'duration':duration_List,
                                 'price':price_List,
                                 'type':tour_type_List,
                                 'group_quota':group_quota_List,
                                 'remaining_quota':remaining_quota_List,
                                 'waiting_List':waiting_List,
                                 'go_date':go_date_List,
                                 'go_company':go_company_List,
                                 'go_flightNo':go_flightNo_List,
                                 'go_departure_time':go_departure_time_List,
                                 'go_departure_city':go_departure_city_List,
                                 'go_arrive_time':go_arrive_time_List,
                                 'go_arrive_city':go_arrive_city_List,
                                 'back_date':back_date_List,
                                 'back_company':back_company_List,
                                 'back_flightNo':back_flightNo_List,
                                 'back_departure_time':back_departure_time_List,
                                 'back_departure_city':back_departure_city_List,
                                 'back_arrive_time':back_arrive_time_List,
                                 'back_arrive_city':back_arrive_city_List,
                                 'tour_schedual': tour_schedual_List})
        
        all_info.to_csv('DomesticTravelInfo.csv', encoding="UTF8")
    
        return all_info

# driver = init_driver(headless=True)
# urls = domestic_traveling_plan_url(driver)
# driver.quit()

info = get_all_plans_info()
# urlList = import_url()
# info_dict = get_one_info(urlList[2])
    