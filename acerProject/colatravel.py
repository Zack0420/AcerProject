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
    
    content_area = soup.find('div', {'class':'wrap_itinerary touriti-highli'})
    
    temp_container = content_area.find_all('div', {'class':'touriti-highliTitle'})
    
    content_titles = [i.text.replace('\n', '') for i in temp_container]
    
    hotel_info = []
    
    if "住宿說明" in content_titles:
        
        hotel_info_area = content_area.find_all('div', {'class':'touriti-highliBox'})[content_titles.index('住宿說明')].find('div', {'class':'touriti-highliContent'})
        
        for i in hotel_info_area.find_all('li'):
            temp_dict = {}
            hotel_name = i.text.split('：')[0]
            hotel_description = i.text.split('：')[1].split('\n')[0]
            temp_dict[hotel_name] = hotel_description
            hotel_info.append(temp_dict)
        
    info_dict['hotel_info'] = hotel_info
    
    tour_timetable = []
    
    for i in soup.find_all('div', {'class':'touriti-dlineTitle'}):
        
        temp_dict = {}
        temp_list = []
        day = i.find('div', {'class':'dlineTitle-day'}).text.replace("\n", ' ').lstrip().replace(' ', ":")
        for j in i.find('div', {'class':'dlineTitle-place'}).find_all('p'):
            
            temp_list.append(j.text)
        
        temp_dict[day] = temp_list
        
        tour_timetable.append(temp_dict)
        
    info_dict['tour_timetable'] = tour_timetable
    
    return info_dict

def get_all_plans_info():
    urlList = import_url()
    
    for url in urlList:
        
        trip_info = get_one_info(url)
    
        break
    

    
# driver = init_driver(headless=True)
# urls = domestic_traveling_plan_url(driver)
# driver.quit()






    