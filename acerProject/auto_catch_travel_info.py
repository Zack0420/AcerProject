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
from datetime import datetime, timedelta
import re
import time

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

def get_urlList(object):
    
    links = set()
    controler = True
    
    
    while controler:
        
        #等待查詢結果出現
        try:
            
            WebDriverWait(object, 10, 0.5).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="dataT-Main"]/ul/li')))
            
        except Exception as e:
            print(e)
            return
        
        #取得現在頁數與最後一頁，用於判斷while迴圈
        currentPage = object.find_element(By.CLASS_NAME, 'current').text
        lastPage = object.find_elements(By.XPATH, '//*[@id="PageSelector"]/ul/li')[-1].get_attribute('data-value')
        print("頁數: ", currentPage)
        
        #當現在頁數等於最後一頁時controler設為false
        if currentPage == lastPage:
            
            controler = False
       
        #取得結果列表
        plans = object.find_elements(By.XPATH, '//*[@id="dataT-Main"]/ul/li')
        
        #取得結果列表中每一項結果的網址
        for i in plans[1:]:
            tourCode = i.find_element(By.CLASS_NAME, 'dataT-titleNum').text
            tourTime = str(datetime.now().year) + '/' + i.find_element(By.CLASS_NAME, 'dataT-date').find_element(By.TAG_NAME, 'span').text.split("(")[0]
            url = 'https://www.colatour.com.tw/C10A_TourSell/C10A13_TourItinerary.aspx?TourDate={}&TourCode={}'.format(tourTime, tourCode)
            links.add(url)
        
        #點擊下一頁 
        ActionChains(object).click(object.find_element(By.XPATH, '//*[@id="tq-dataTourjs"]/div[4]/div[1]/btn[2]')).perform()
    
    return links

def get_one_info(url):
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    
    response = requests.get(url, headers=headers)
    
    soup = bs(response.text, 'html.parser')
    
    info_dict = {}
    
    try:
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
        
    except Exception as e:
        print(e)
        info_dict = {}
        info_dict['title'] = ""
        
        info_dict['date'] = ""
        
        info_dict['departure_city'] =""
        
        info_dict['duration'] = ""
        
        info_dict['price'] = ""
        
        info_dict['group_quota'] = ""
        
        info_dict['remaining_quota'] = ""
        
        info_dict['waitingList'] = ""
        
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
        
        info_dict['type'] = ""
        
        info_dict['tour_schedual'] = ""
        
        return info_dict
    
    return info_dict

def get_all_plans_info(urlList):
    
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
    count = 0
    
    try:

        
        while True:
            
            if count < len(urlList):
                print(count + 1)
            
                try:
                    info = get_one_info(urlList[count])
                    
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
                    
                    count += 1
                except Exception as error:
                    
                    time.sleep(3)
                    print(error)
                    continue
            
            else:
                
                break
          
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
                                 'tour_schedual': tour_schedual_List,
                                 'tour_page_url': urlList})
        
        all_info.to_csv('DomesticTravelInfo.csv', encoding="UTF8")
    
    return all_info

def get_search_result_urlList():
    
    urlList = set()
    
    tomorrow = datetime.now() + timedelta(1)
    
    #設定webdriver
    browser = init_driver(maximized = True)
    browser.get('https://www.colatour.com.tw/home/')
    
    #等待搜尋條載入
    try:
        WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[3]')))
    except Exception as error:
        print(error)
        return
    
    bound_type = ['in','out']
    #-----------------------------------------------------------------------------------------------------------------------
    for bound in bound_type:
        
        if bound == "in":
            #點擊國內按鈕
            bound_in_button = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[1]/div/div/button[2]')
            ActionChains(browser).click(bound_in_button).perform()
            
            #點擊出發地表單
            departure_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]')
            ActionChains(browser).click(departure_select_form).perform()
            
            #等待出發地表單出現
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]/ul')))
            except Exception as error:
                print(error)
                browser.close()
                browser.quit()                                                
    
            departure_city_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]/ul/li[1]')
            ActionChains(browser).click(departure_city_locator).perform()
            #-----------------------------------------------------------------------------------------------------------------------
            
            #點擊地區表單
            region_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]')
            ActionChains(browser).click(region_select_form).perform()
            
            #等待地區表單出現
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/section')))
            except Exception as error:
                print(error)
            
            region_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/section/div[1]')
            ActionChains(browser).click(region_locator).perform()
            #-----------------------------------------------------------------------------------------------------------------------
            
            #點擊出發日期表單
            time_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]')
            ActionChains(browser).click(time_select_form).perform()
                
            #等待日期表單出現
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div')))
            except Exception as error:
                print(error)
            
            #抓取可選年分
            year_options = [year.get_attribute('value') for year in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul/li')]
           
            #取得年分表單位置並點擊
            year_list_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div')
            ActionChains(browser).click(year_list_locator).perform()
                    
            #等待年份表單出現
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul')))
            except Exception as error:
                print(error)
                    
            #取得輸入年份選項位置並點擊
            year_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul/li[{}]'.format(year_options.index(str(tomorrow.year))+1))
            ActionChains(browser).click(year_locator).perform()
                    
            #抓取可選月份
            month_options = [month.get_attribute('value') for month in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul/li')]
                    
           
            #取得月份表單位置並點擊
            month_list_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div')
            ActionChains(browser).click(month_list_locator).perform()
                        
            #等待月份表單出現
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul')))
            except Exception as error:
                print(error)
                        
            #取得輸入月份選項位置並點擊
            month_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul/li[{}]'.format(month_options.index(str(tomorrow.month))+1))
            ActionChains(browser).click(month_locator).perform()
                        
            #取得可選日
            day_options = [month.text for month in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div')]
                        
            #檢查輸入日期選項位置並點擊
            day_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[{}]'.format(day_options.index(str(tomorrow.day))+1))
            ActionChains(browser).click(day_locator).perform()
                        
            #--------------------------------------------------------------------
            
            #等待日期表單消失
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div')))
            except Exception as error:
                print(error)
                
            #--------------------------------------------------------------------
            #點擊搜索按鈕
            search_button = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[3]/button')
            ActionChains(browser).click(search_button).perform()
            page_urlList = get_urlList(browser)
            urlList = urlList.union(page_urlList)
            
            browser.back()
            #等待搜尋條載入
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[3]')))
            except Exception as error:
                print(error)
                return
            
        else:
            
            #點擊國外按鈕
            bound_out_button = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[1]/div/div/button[1]')
            ActionChains(browser).click(bound_out_button).perform()
            
            #點擊目的地表單
            region_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]')
            ActionChains(browser).click(region_select_form).perform()
            
            #等待目的地表單出現
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div')))
            except Exception as error:
                print(error)
            
            #抓取地區
            region_options = [region.text for region in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/header/ul/li')]
           
            #點擊目的地表單
            region_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]')
            ActionChains(browser).click(region_select_form).perform()
                
            for region in region_options:
                
                #點擊目的地表單
                region_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]')
                ActionChains(browser).click(region_select_form).perform()
                
                #等待目的地表單出現
                try:
                    WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div')))
                except Exception as error:
                    print(error)
                    
                #依輸入點選區域
                region_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/header/ul/li[{}]'.format(region_options.index(region)+1))
                ActionChains(browser).click(region_locator).perform()
                
                for b_index, block in enumerate(browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/div')):
                    for c_index, country in enumerate(browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/div[{}]/div'.format(b_index + 1))):
                        
                        print(region, b_index, c_index)
                        destination_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/div[{}]/div[{}]/ul/li[1]'.format(b_index + 1, c_index + 1))
                        ActionChains(browser).click(destination_locator).perform()
                        
                        #點擊出發地表單
                        departure_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]')
                        ActionChains(browser).click(departure_select_form).perform()
                        
                        #等待出發地表單出現
                        try:
                            WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]/ul')))
                        except Exception as error:
                            print(error)
                            browser.close()
                            browser.quit()                                                
                
                        departure_city_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]/ul/li[1]')
                        ActionChains(browser).click(departure_city_locator).perform()
                        
                        #點擊出發日期表單
                        time_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]')
                        ActionChains(browser).click(time_select_form).perform()
                            
                        #等待日期表單出現
                        try:
                            WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div')))
                        except Exception as error:
                            print(error)
                        
                        #抓取可選年分
                        year_options = [year.get_attribute('value') for year in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul/li')]
                       
                        #取得年分表單位置並點擊
                        year_list_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div')
                        ActionChains(browser).click(year_list_locator).perform()
                                
                        #等待年份表單出現
                        try:
                            WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul')))
                        except Exception as error:
                            print(error)
                                
                        #取得輸入年份選項位置並點擊
                        year_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul/li[{}]'.format(year_options.index(str(tomorrow.year))+1))
                        ActionChains(browser).click(year_locator).perform()
                                
                        #抓取可選月份
                        month_options = [month.get_attribute('value') for month in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul/li')]
                                
                       
                        #取得月份表單位置並點擊
                        month_list_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div')
                        ActionChains(browser).click(month_list_locator).perform()
                                    
                        #等待月份表單出現
                        try:
                            WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul')))
                        except Exception as error:
                            print(error)
                                    
                        #取得輸入月份選項位置並點擊
                        month_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul/li[{}]'.format(month_options.index(str(tomorrow.month))+1))
                        ActionChains(browser).click(month_locator).perform()
                                    
                        #取得可選日
                        day_options = [month.text for month in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div')]
                                    
                        #檢查輸入日期選項位置並點擊
                        day_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[{}]'.format(day_options.index(str(tomorrow.day))+1))
                        ActionChains(browser).click(day_locator).perform()
                                    
                        #--------------------------------------------------------------------
                        
                        #等待日期表單消失
                        try:
                            WebDriverWait(browser, 10, 0.5).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div')))
                        except Exception as error:
                            print(error)
                            
                        #--------------------------------------------------------------------
                        #點擊搜索按鈕
                        search_button = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[3]/button')    
                        ActionChains(browser).click(search_button).perform()
                        page_urlList = get_urlList(browser)
                        urlList = urlList.union(page_urlList)
                        browser.back()
                        
                        #等待搜尋條載入
                        try:
                            WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[3]')))
                        except Exception as error:
                            print(error)
                            return
                        
                        #點擊國外按鈕
                        bound_out_button = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[1]/div/div/button[1]')
                        ActionChains(browser).click(bound_out_button).perform()
                        
                        #點擊目的地表單
                        region_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]')
                        ActionChains(browser).click(region_select_form).perform()
                        
                        #等待目的地表單出現
                        try:
                            WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div')))
                        except Exception as error:
                            print(error)
                            
                        #依輸入點選區域
                        region_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/header/ul/li[{}]'.format(region_options.index(region)+1))
                        ActionChains(browser).click(region_locator).perform()
                            
                    
                #點擊目的地表單
                region_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]')
                ActionChains(browser).click(region_select_form).perform()
                                                  
    browser.close()
    browser.quit()                           
    return urlList

urlList = list(get_search_result_urlList())
info = get_all_plans_info(urlList)
