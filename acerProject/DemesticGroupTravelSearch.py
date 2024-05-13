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
from datetime import datetime
import re
import time

current_datetime = datetime.now()

"""
    描述: 初始設定 ChromeOptions
    輸入:
        maximize: 網頁視窗最大化
        incognito: 設置無痕模式
        headless: 設置無頭模式
        extension: 設置是否禁用Chrome之擴展功能。如果為True，則禁用。
        popup_blocking: 設置是否禁用瀏覽器之彈出窗口。如果為True，則禁用。
    輸出:
        chrome webdriver
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
    描述: 點選查詢表單並
    輸入: 
         bound: 輸入in或out
         travel_type: 輸入不限、團體旅遊、團體自由行(還沒做)
         Departure_city:輸入出發城市
         Region: 目的地
         Departure_date: 出發日期
    輸出:
        return links list
    備註: 無
"""
#travel_type available
def group_travel_search():
    
    #設定webdriver
    browser = init_driver(maximized = True, headless=True)
    
    #載入頁面
    browser.get('https://www.colatour.com.tw/home/')
    
    #等待搜尋條載入
    try:
        WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[3]')))
    except Exception as error:
        print(error)
        return
    
    bound = input("國內、國外(輸入in或out): ")
    
    if bound == 'in':
        
        #點擊國內按鈕
        bound_in_button = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[1]/div/div/button[2]')
        ActionChains(browser).click(bound_in_button).perform()
        
        #選擇旅遊型態
        travel_type_options = [t.text for t in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[1]/div/ul/li')]
        print("請選擇以下旅遊型態: ")
        for index, o in enumerate(travel_type_options):
            print(str(index+1)+" "+o)
        travel_type_input = input("選擇旅遊型態代號: ")
        if eval(travel_type_input) > len(travel_type_options):
            print("選項不存在")
        else:
            travel_type_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[1]/div/ul/li[{}]/label/input'.format(travel_type_input))
            travel_type_locator.click()
        
        
        
        #選擇是否只顯示可報名
        available_input = input("是否只顯示可報名選項(是/否)?")
        if available_input == '否':
            available_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[3]/label/input')
            available_locator.click()
        elif available_input == '是':
            pass
        
        else:
            print('選項不存在')
        #--------------------------------------------------------------------
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
        
        #抓取表單內容
        departure_options = [city.text for city in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]/ul/li')]
        
        #輸入出發地
        print("請選擇以下出發地: ")
        for index, o in enumerate(departure_options):
            print(str(index+1)+" "+o)
        departure_city_input = input("選擇出發地代號: ")
        if eval(departure_city_input) > len(departure_options):
            print("選項不存在")
        else:
            #依輸入點選出發地
            departure_city_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]/ul/li[{}]'.format(departure_city_input))
            ActionChains(browser).click(departure_city_locator).perform()
        #--------------------------------------------------------------------
          
        #點擊地區表單
        region_select_form = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]')
        ActionChains(browser).click(region_select_form).perform()
        
        #等待地區表單出現
        try:
            WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/section')))
        except Exception as error:
            print(error)
        
        #抓取表單內容
        region_options = [region.text for region in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/section/div')]
       
        #輸入區域
        print("請選擇以下地區: ")
        for index, o in enumerate(region_options):
            print(str(index+1)+" "+o)
        region_input = input("選擇地區代號: ")
        if eval(region_input) > len(region_options):
            print("選項不存在")
        else:
            #依輸入點選區域
            region_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/section/div[{}]'.format(region_input))
            ActionChains(browser).click(region_locator).perform()
        #--------------------------------------------------------------------
        
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
        
        #輸入日期
        date_input = input("輸入出發日期(yyyy/mm/dd): ")
        
        #檢查日期格式
        if re.compile('\d{4}/\d{2}/\d{2}').match(date_input) != None:
            
            #拆分日期
            year = date_input.split("/")[0]
            month = date_input.split("/")[1].lstrip('0')
            day = date_input.split("/")[2].lstrip('0')
            
            #檢查年分是否可選
            if year in year_options:
                
                #取得年分表單位置並點擊
                year_list_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div')
                ActionChains(browser).click(year_list_locator).perform()
                
                #等待年份表單出現
                try:
                    WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul')))
                except Exception as error:
                    print(error)
                
                #取得輸入年份選項位置並點擊
                year_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul/li[{}]'.format(year_options.index(year)+1))
                ActionChains(browser).click(year_locator).perform()
                
                #抓取可選月份
                month_options = [month.get_attribute('value') for month in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul/li')]
                
                #檢查月份是否可選
                if month in month_options:
                    
                    #取得月份表單位置並點擊
                    month_list_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div')
                    ActionChains(browser).click(month_list_locator).perform()
                    
                    #等待月份表單出現
                    try:
                        WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul')))
                    except Exception as error:
                        print(error)
                    
                    #取得輸入月份選項位置並點擊
                    month_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul/li[{}]'.format(month_options.index(month)+1))
                    ActionChains(browser).click(month_locator).perform()
                    
                    #取得可選日
                    day_options = [month.text for month in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div')]
                    
                    #檢查日期是否過期
                    if eval(day) > current_datetime.day:
                        
                        #檢查輸入日期選項位置並點擊
                        day_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[{}]'.format(day_options.index(day)+1))
                        ActionChains(browser).click(day_locator).perform()
                    
                    else:
                        
                        print("請選擇" + '(' + str(day_options)[current_datetime.day].replace('[', '').replace(']', '').replace("'", '').replace(',', ' ').lstrip().rstrip().replace('  ', ',') + ')' + ": ")
                        
                else:
                    
                    print("請選擇" + str(month_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
                    
            else:
                print("請選擇" + str(year_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
        else:
            
            print("格式錯誤!")
        #--------------------------------------------------------------------
        
        #等待日期表單消失
        try:
            WebDriverWait(browser, 10, 0.5).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div')))
        except Exception as error:
            print(error)
            
        #點擊搜索按鈕
        browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[3]/button').click()
        #--------------------------------------------------------------------
        
        
        links = []
        controler = True
        
        #檢查是否有查詢結果
        try:
            
            browser.find_element(By.ID, 'noTourData')
            
        except:
            print('No Tour Data')
            return 
        
        while controler:
            
            #等待查詢結果出現
            try:
                
                WebDriverWait(browser, 10, 0.5).until(EC.visibility_of(browser.find_element(By.ID, 'dataT-Main')))
                
            except:
                
                print('The element not found')
                return
            
            #取得現在頁數與最後一頁，用於判斷while迴圈
            currentPage = browser.find_element(By.CLASS_NAME, 'current').text
            lastPage = browser.find_elements(By.XPATH, '//*[@id="PageSelector"]/ul/li')[-1].get_attribute('data-value')
            print(currentPage)
            
            #當現在頁數等於最後一頁時controler設為false
            if currentPage == lastPage:
                
                controler = False
           
            #取得結果列表
            plans = browser.find_elements(By.XPATH, '//*[@id="dataT-Main"]/ul/li')
            
            #取得結果列表中每一項結果的網址
            for i in plans[1:]:
                tourCode = i.find_element(By.CLASS_NAME, 'dataT-titleNum').text
                tourTime = str(current_datetime.year) + '/' + i.find_element(By.CLASS_NAME, 'dataT-date').find_element(By.TAG_NAME, 'span').text.split("(")[0]
                url = 'https://www.colatour.com.tw/C10A_TourSell/C10A13_TourItinerary.aspx?TourDate={}&TourCode={}'.format(tourTime, tourCode)
                links.append(url)
            
            #點擊下一頁 
            ActionChains(browser).click(browser.find_element(By.XPATH, '//*[@id="tq-dataTourjs"]/div[4]/div[1]/btn[2]')).perform()
        
        browser.close()
        browser.quit()
        return links
        
    elif bound == 'out':
        
        #點擊國外按鈕
        bound_out_button = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[1]/div/div/button[1]')
        ActionChains(browser).click(bound_out_button).perform()
        
        # #--------------------------------------------------------------------
        
        #選擇旅遊型態
        travel_type_options = [t.text for t in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[1]/div/ul/li')]
        print("請選擇以下旅遊型態: ")
        for index, o in enumerate(travel_type_options):
            print(str(index+1)+" "+o)
        travel_type_input = input("選擇旅遊型態代號: ")
        if eval(travel_type_input) > len(travel_type_options):
            print("選項不存在")
        else:
            travel_type_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[1]/div/ul/li[{}]/label/input'.format(travel_type_input))
            travel_type_locator.click()
        
        
        
        #選擇是否只顯示可報名
        available_input = input("是否只顯示可報名選項(是/否)?")
        if available_input == '否':
            available_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[3]/label/input')
            available_locator.click()
        elif available_input == '是':
            pass
        
        else:
            print('選項不存在')
        #--------------------------------------------------------------------
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
        
        #抓取表單內容
        departure_options = [city.text for city in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]/ul/li')]
        
        #輸入出發地
        print("請選擇以下出發地: ")
        for index, o in enumerate(departure_options):
            print(str(index+1)+" "+o)
        departure_city_input = input("選擇出發地代號: ")
        if eval(departure_city_input) > len(departure_options):
            print("選項不存在")
        else:
            #依輸入點選出發地
            departure_city_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[1]/ul/li[{}]'.format(departure_city_input))
            ActionChains(browser).click(departure_city_locator).perform()
        #--------------------------------------------------------------------
          
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
        
        print("請選擇以下區域: ")
        for index, o in enumerate(region_options):
            
            print(str(index+1)+" "+o)
        
        #輸入地區
        region_input = input('輸入代碼: ' )
        
        if eval(region_input) > len(region_options) :
            
            print('選項不存在')
        
        else:
            #依輸入點選區域
            region_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/header/ul/li[{}]'.format(region_input))
            ActionChains(browser).click(region_locator).perform()
            
            #抓取國家選項
            country_container = browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/div')
            destination_options = {}
            country_block = {}
            
            for index, item in enumerate(country_container):
                
                for c_index, country in enumerate(item.find_elements(By.XPATH, 'div')):
                    
                    country_name = country.find_element(By.XPATH, 'h4').text
                    city_options = [city.text for city in country.find_elements(By.XPATH, 'ul/li')]
                    destination_options[country_name] = city_options
                    country_block[country_name] = [str(index+1), str(c_index+1)]
                    
                 
                    
            print("請選擇以下國家: ")
            for index, o in enumerate(destination_options.keys()):
                
                print(str(index+1)+" "+o)
            
            #輸入國家
            country_input = input('輸入代碼: ' )
            
            if eval(country_input) > len(destination_options.keys()) :
                
                print('選項不存在')
                
            else:
                
                print("請選擇以下城市: ")
                for index, o in enumerate(list(destination_options.values())[eval(country_input)-1]):
                    
                    print(str(index+1)+" "+o)
                
            #輸入城市
            city_input = input('輸入代碼: ' )
                
            if eval(city_input) > len(list(destination_options.values())[eval(country_input)-1]):
                    
                print('選項不存在')
            
            #點擊選項
            destination_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[1]/div[3]/div/main/div[{}]/div[{}]/ul/li[{}]'.format(country_block[list(destination_options.keys())[eval(country_input)-1]][0], country_block[list(destination_options.keys())[eval(country_input)-1]][1], city_input))
            ActionChains(browser).click(destination_locator).perform()
            
        #--------------------------------------------------------------------
        
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
        
        #輸入日期
        date_input = input("輸入出發日期(yyyy/mm/dd): ")
        
        #檢查日期格式
        if re.compile('\d{4}/\d{2}/\d{2}').match(date_input) != None:
            
            #拆分日期
            year = date_input.split("/")[0]
            month = date_input.split("/")[1].lstrip('0')
            day = date_input.split("/")[2].lstrip('0')
            
            #檢查年分是否可選
            if year in year_options:
                
                #取得年分表單位置並點擊
                year_list_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div')
                ActionChains(browser).click(year_list_locator).perform()
                
                #等待年份表單出現
                try:
                    WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul')))
                except Exception as error:
                    print(error)
                
                #取得輸入年份選項位置並點擊
                year_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/ul/li[{}]'.format(year_options.index(year)+1))
                ActionChains(browser).click(year_locator).perform()
                
                #抓取可選月份
                month_options = [month.get_attribute('value') for month in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul/li')]
                
                #檢查月份是否可選
                if month in month_options:
                    
                    #取得月份表單位置並點擊
                    month_list_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div')
                    ActionChains(browser).click(month_list_locator).perform()
                    
                    #等待月份表單出現
                    try:
                        WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul')))
                    except Exception as error:
                        print(error)
                    
                    #取得輸入月份選項位置並點擊
                    month_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/ul/li[{}]'.format(month_options.index(month)+1))
                    ActionChains(browser).click(month_locator).perform()
                    
                    #取得可選日
                    day_options = [month.text for month in browser.find_elements(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div')]
                    
                    #檢查日期是否過期
                    if eval(day) > current_datetime.day:
                        
                        #檢查輸入日期選項位置並點擊
                        day_locator = browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[{}]'.format(day_options.index(day)+1))
                        ActionChains(browser).click(day_locator).perform()
                    
                    else:
                        
                        print("請選擇" + '(' + str(day_options)[current_datetime.day].replace('[', '').replace(']', '').replace("'", '').replace(',', ' ').lstrip().rstrip().replace('  ', ',') + ')' + ": ")
                        
                else:
                    
                    print("請選擇" + str(month_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
                    
            else:
                print("請選擇" + str(year_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
        else:
            
            print("格式錯誤!")
        #--------------------------------------------------------------------
        
        #等待日期表單消失
        try:
            WebDriverWait(browser, 10, 0.5).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="searchbar"]/div/div[2]/div[2]/div')))
        except Exception as error:
            print(error)
            
        #點擊搜索按鈕
        browser.find_element(By.XPATH, '//*[@id="searchbar"]/div/div[3]/button').click()
        #--------------------------------------------------------------------
        
        
        links = []
        controler = True
        
        #檢查是否有查詢結果
        try:
            
            browser.find_element(By.ID, 'noTourData')
            
        except:
            print('No Tour Data')
            return 
        
        while controler:
            
            #等待查詢結果出現
            try:
                
                WebDriverWait(browser, 10, 0.5).until(EC.visibility_of(browser.find_element(By.ID, 'dataT-Main')))
                
            except:
                
                print('The element not found')
                return
            
            #取得現在頁數與最後一頁，用於判斷while迴圈
            currentPage = browser.find_element(By.CLASS_NAME, 'current').text
            lastPage = browser.find_elements(By.XPATH, '//*[@id="PageSelector"]/ul/li')[-1].get_attribute('data-value')
            print(currentPage)
            
            #當現在頁數等於最後一頁時controler設為false
            if currentPage == lastPage:
                
                controler = False
           
            #取得結果列表
            plans = browser.find_elements(By.XPATH, '//*[@id="dataT-Main"]/ul/li')
            
            #取得結果列表中每一項結果的網址
            for i in plans[1:]:
                tourCode = i.find_element(By.CLASS_NAME, 'dataT-titleNum').text
                tourTime = str(current_datetime.year) + '/' + i.find_element(By.CLASS_NAME, 'dataT-date').find_element(By.TAG_NAME, 'span').text.split("(")[0]
                url = 'https://www.colatour.com.tw/C10A_TourSell/C10A13_TourItinerary.aspx?TourDate={}&TourCode={}'.format(tourTime, tourCode)
                links.append(url)
            
            #點擊下一頁 
            ActionChains(browser).click(browser.find_element(By.XPATH, '//*[@id="tq-dataTourjs"]/div[4]/div[1]/btn[2]')).perform()
        
        browser.close()
        browser.quit()
        return links

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
                                 'tour_schedual': tour_schedual_List})
        
        all_info.to_csv('DomesticTravelInfo.csv', encoding="UTF8")
    
    return all_info
links = group_travel_search()
info = get_all_plans_info(links)


        




