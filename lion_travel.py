# -*- coding: utf-8 -*-
"""
Created on Fri May 10 10:33:44 2024

@author: Zack
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
from lxml import html
import pandas as pd
import requests
import re

# search = input("請輸入查詢地點:")
search = "新北" #查詢地點:
    
# departure time1 = input("請輸入查詢日期區間:")
# departure time2 = input("請輸入查詢日期區間:")
current_date = datetime.now()
departure_time1 = current_date.strftime("%Y-%m-%d")

two_months_later = current_date + timedelta(days=60)
departure_time2 =  two_months_later.strftime("%Y-%m-%d")


titleList = []
UrlList = []
priceList = []

temp = 0
page = 1
checkDateFlag = True


chrome_options = Options()
chrome_options.add_argument("--headless=new")
browser = webdriver.Chrome(options=chrome_options) #無頭模式
# browser = webdriver.Chrome()

browser.get("https://travel.liontravel.com/search?DepartureID=&ArriveID=&GoDateStart="+departure_time1+"&GoDateEnd="+departure_time2+"&Keywords="+search) #抓取雄獅旅遊的網站
browser.maximize_window()
# print(browser.current_url)

locator = (By.CLASS_NAME, 'buttons--CXG5i') #以x項精彩行程定位，以便等待js載入
next_locator = (By.XPATH, '//*[@id="root"]/div/div[4]') #以nextPage圖標定位
# inside_locator = (By.XPATH, '//*[@id="root"]/div/div[4]') #以頁面定位
inside_locator = (By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[1]/div') #以列表顯示
date_locator = (By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/section[2]') #以第一項出發日期定位




try:
    WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located(locator))
    # browser.find_element(By.TAG_NAME,'body').send_keys(Keys.END) #下拉到最底
    soup = BeautifulSoup(browser.page_source, "html.parser")
    totals = soup.find_all("div", class_="ItemQty--kVIvw")#print出結果共有x項精彩行程
    for t in totals:
        total =  t.text.split("項")[0]#總共的項目數
    
    # print("共有"+str(t.text))
    # print(int(total)%10) #總共
    click_times_check = int(total)
    
    # print()
    
    while True:
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        titles = soup.select("span.caption--mphmX") #行程標題
        lastPage_source = browser.page_source
        titleUrl = soup.find_all("a", class_="cardsList--2cG2D") #行程網址
        prices = soup.find_all("div", class_="sellPrice--3fg38") #行程價格
        

        for index,(title,url,price) in enumerate(zip(titles,titleUrl,prices)):
            temp+=1
            # print(str(temp)+".", title.text, price.text+"人/起") #標題與價格
            titleList.append(title.text)
            priceList.append(price.text+"人/起")
            
            # print("https://travel.liontravel.com/"+url.get("href")) #網址
            # print()
            
            UrlList.append("https://travel.liontravel.com/"+url.get("href"))
            
            
            if temp % 10 == 0:
                browser.find_element(By.CLASS_NAME,'Style__StyledPageStyle-sc-17tz2cz-1.kGjiOf.page.next').click()
                page += 1
                # print("page = "+str(page))
                
            if temp-click_times_check==0:
                checkDateFlag = False
                break
        if checkDateFlag == False:
            break
        
    for time in range(temp): #例53項
            browser.get(UrlList[time])
            # browser.get("https://travel.liontravel.com//detail?NormGroupID=75c7cf33-ec08-408b-874d-8933e146336d&GroupID=24TN611MAN-T&Platform=app")
            sleep(1.5)
            print(str(time+1)+".", titleList[time])
            all_items = browser.find_element(By.CLASS_NAME,'infos--1WOHM').find_elements(By.TAG_NAME, "li")
            # print(item.text)
            for item in all_items:
                print(item.text) #行程1到刷卡好康
                
            WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located(inside_locator))
            
            check_List = browser.find_element(By.CLASS_NAME,'text--1L79t')
            if check_List.text == "列表顯示":
                ActionChains(browser).click(check_List).perform()
                print(check_List.text)
                WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(date_locator))
            
            try:
                main_bar = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/section[1]').find_elements(By.TAG_NAME, "div")
            except:
                if check_List.text == "列表顯示":
                    ActionChains(browser).click(check_List).perform()
                    print(check_List.text)
                    WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located(date_locator))
                    main_bar = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/section[1]').find_elements(By.TAG_NAME, "div")
                
            try:
                all_trip_info = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]').find_elements(By.TAG_NAME, "div") #列表顯示
            except:
                print("無出發日")
                
            try:
                full_trip_message = browser.find_element(By.XPATH,'//*[@id="schedules"]/div[2]').find_elements(By.CLASS_NAME,"wholeMode--1Joyg") #行程資訊
            except:
                full_trip_message = browser.find_element(By.XPATH,'//*[@id="schedules"]/div[2]').find_element(By.CLASS_NAME,"wholeMode--1Joyg") #行程資訊
                
            hotel_info = browser.find_element(By.XPATH,'//*[@id="schedules"]/div[2]').find_elements(By.CLASS_NAME,"wholeMode--1Joyg") #旅館資訊
            
            date_count = browser.find_element(By.CSS_SELECTOR,'#root > div > div.group_wrapper > div > div.group_container_m > div.group_detail--apXYI.group_detail > div.info-wrapper--3VhKy > div:nth-child(2) > ul > li:nth-child(4) > span.days--3UNv4') #總共天數
            flying_and_from_info = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div[2]').find_elements(By.CLASS_NAME, "content--3WbP4") #航班與出發地點資訊
            
            
            for faf in flying_and_from_info : #機票資訊
                print(faf.text)
            print(date_count.text)#總共天數
            
            try:
                for mb in main_bar:
                    print(mb.text,end="  ") #出發日期 行程   成行狀態  可賣 席次 價格 
            except:
                if check_List.text == "列表顯示":
                    ActionChains(browser).click(check_List).perform()
                    print(check_List.text)
                    WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located(date_locator))
                    main_bar = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/section[1]').find_elements(By.TAG_NAME, "div")
                    for mb in main_bar:
                        print(mb.text,end="  ") #出發日期 行程   成行狀態  可賣 席次 價格 
                
            print()
            for ati in all_trip_info:
                try:
                    atf = ati.find_elements(By.XPATH,'section[2]/div/div')
                    count = 0
                    for at in atf:
                        print(at.text,end=" ")
                        count+=1
                        if count % 9==0:
                            print()
                except:
                    pass
            try:
                for ftm in full_trip_message:
                    ftmf = ftm.find_elements(By.XPATH, 'div/div[2]/h3')
                    for ft in ftmf:
                        print(ft.text)
                        print()
            except:
                pass

finally:
    pass
    # browser.quit()



data = pd.DataFrame({"標題:":titleList,
                     "網址:":UrlList,
                     "價格:":priceList})
try:
    data.to_excel("旅遊搜尋.xlsx",encoding="big5")
    
except:
    pass




































