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
# search = '台灣' #查詢地點:
    
# departure time1 = input("請輸入查詢日期區間:")
# departure time2 = input("請輸入查詢日期區間:")
current_date = datetime.now()
departure_time1 = current_date.strftime("%Y-%m-%d")

two_months_later = current_date + timedelta(days=60)
departure_time2 =  two_months_later.strftime("%Y-%m-%d")

search_Area_Url = []
titleList = [] #標題
UrlList = [] #網址

inside_titleList = [] #總共標題數
inside_urlList = [] #網址

priceList = [] #價錢
title_priceList = [] #外網址價錢

departure_DateList = [] #出發日期
tripDateList = [] #旅程天數
# fromCityList = [] #出發城市
full_trip_message_List = [] #旅遊行程(每日行程)
full_tripList = []#旅遊行程(每日行程)


trip_numList = [] #行程編號:行程1
tripGroupState1 = [] #成團狀況(團位) 
tripGroupState2 = [] #成團狀況(可售) 
tripGroupState3 = [] #成團狀況(補位) 
tripGroupState4 = [] #成團狀況:如成形show否則為空
transportation = [] #機票資訊 

hotelList = [] #住宿點
hotel_insideList= []
typeList = [] #旅遊公司名稱


title_count = 0
page = 1
checkDateFlag = True


# chrome_options = Options()
# chrome_options.add_argument("--headless=new")
# browser = webdriver.Chrome(options=chrome_options) #無頭模式
browser = webdriver.Chrome()

browser.get("https://travel.liontravel.com/search?DepartureID=&ArriveID=&GoDateStart="+departure_time1+"&GoDateEnd="+departure_time2+"&Keywords=") #抓取雄獅旅遊的網站
browser.maximize_window()
print(browser.current_url)

locator = (By.CLASS_NAME, 'buttons--CXG5i') #以x項精彩行程定位，以便等待js載入
next_locator = (By.XPATH, '//*[@id="root"]/div/div[4]') #以nextPage圖標定位
inside_locator = (By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[1]/div') #以列表顯示
date_locator = (By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/section[2]') #以第一項出發日期定位
title_locator = (By.CLASS_NAME, 'title--1dhv-') #以標題定位



try:
    WebDriverWait(browser, 10, 0.1).until(EC.presence_of_element_located(locator))
    soup = BeautifulSoup(browser.page_source, "html.parser")
    totals = soup.find_all("div", class_="ItemQty--kVIvw")#print出結果共有x項精彩行程
    for t in totals:
        total =  t.text.split("項")[0]#總共的項目數
    
    print("共有"+str(t.text))
    # print(int(total)%10) #總共
    click_times_check = int(total)
    
    # print()
    #用while迴圈抓取搜尋結果的標題與網址
    while True:
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        titles = soup.select("span.caption--mphmX") #行程標題
        lastPage_source = browser.page_source
        titleUrl = soup.find_all("a", class_="cardsList--2cG2D") #行程網址
        prices = soup.find_all("div", class_="sellPrice--3fg38") #行程價格

        for index,(title,url,price) in enumerate(zip(titles,titleUrl,prices)):
            title_count+=1
            # print(str(temp)+".", title.text, price.text+"人/起") #標題與價格
            titleList.append(title.text)
            title_priceList.append(price.text+"人/起")
            
            # print("https://travel.liontravel.com/"+url.get("href")) #網址
            # print()
            
            UrlList.append("https://travel.liontravel.com/"+url.get("href"))
            
            
            if title_count % 10 == 0:
                browser.find_element(By.CLASS_NAME,'Style__StyledPageStyle-sc-17tz2cz-1.kGjiOf.page.next').click()
                page += 1
                print("page = "+str(page))
                
            if title_count-click_times_check==0:
            # if title_count-10==0: #測試10筆
                checkDateFlag = False
                break
        if checkDateFlag == False:
            break
        
    #for迴圈抓取所需資訊
    for time in range(title_count): #例53項
            try:
                browser.get(UrlList[time])
                print(str(time+1)+".", titleList[time])
                print(UrlList[time])
                try:
                    WebDriverWait(browser,20, 0.1).until(EC.presence_of_element_located(inside_locator))  #以列表顯示
                except:
                    WebDriverWait(browser,20, 0.1).until(EC.visibility_of_element_located(inside_locator))  #以列表顯示
                #顯示共幾天
                WebDriverWait(browser, 10, 0.1).until(EC.visibility_of_all_elements_located(title_locator)) #以標題定位
                datecount = browser.find_element(By.CLASS_NAME,'days--3UNv4') #共幾天
                print(datecount.text)
                
                #確認顯示是否為列表顯示
                WebDriverWait(browser, 10, 0.1).until(EC.visibility_of_all_elements_located(inside_locator))
                check_List = browser.find_element(By.CLASS_NAME,'text--1L79t')
                if check_List.text == "列表顯示":
                    ActionChains(browser).click(check_List).perform()
                    # print(check_List.text)
                    WebDriverWait(browser, 10, 0.1).until(EC.visibility_of_all_elements_located(inside_locator))
                
                try:
                    main_bar = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/section[1]').find_elements(By.TAG_NAME, "div")
                except:
                    if check_List.text == "列表顯示":
                        ActionChains(browser).click(check_List).perform()
                        print(check_List.text)
                        WebDriverWait(browser, 10, 0.1).until(EC.presence_of_element_located(date_locator))
                        main_bar = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/section[1]').find_elements(By.TAG_NAME, "div")
                try:
                     #機票資訊
                  
                        
                    # 旅遊資訊  
                        all_trip_info = browser.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]').find_elements(By.TAG_NAME, "div") #列表顯示
                        for ati in all_trip_info:     
                            WebDriverWait(browser, 10, 0.1).until(EC.presence_of_element_located(date_locator))
                            fromDate = ati.find_elements(By.XPATH,'section[2]/div/div[1]') #出發日期o
                            trip_num = ati.find_elements(By.XPATH,'section[2]/div/div[2]') #行程編號o
                            trip_state_show = ati.find_elements(By.XPATH,'section[2]/div/div[3]') #若以成行show成行，若無為空o
                            sellable = ati.find_elements(By.XPATH,'section[2]/div/div[7]') #剩餘可賣o
                            totalsell = ati.find_elements(By.XPATH,'section[2]/div/div[8]') #總席次o
                            trip_state = ati.find_elements(By.XPATH,'section[2]/div/div[5]') #報名狀態o
                            price = ati.find_elements(By.XPATH,'section[2]/div/div[9]') #價格o
                            
                            
                            
                            # try:
                            #     count = 1
                            #     hotel_info = browser.find_elements(By.XPATH, '//*[@id="schedules"]/div[2]/div/div/div[3]/div[2]/div/span')
                            #     for hotel in hotel_info:
                            #         print("Day"+str(count)+": "+hotel.text)
                            #         hotelList.append("Day:"+str(count)+hotel.text)
                            #         count+=1
                            # except:
                            #     hotelList.append("無旅館資訊")
                            count = 1
                            for fd,tn,tss,sa,ts,tse,p in zip(fromDate, trip_num, trip_state_show, sellable, totalsell, trip_state, price):
                                # print(str(time+1)+".", titleList[time])
                                
                                
                                print(str(time+1)+".", titleList[time]) 
                                inside_titleList.append(titleList[time])#標題
                                
                                print(UrlList[time]) 
                                inside_urlList.append(UrlList[time])#連結
                                
                                #旅館資訊 
                                try:
                                    hotel_info = browser.find_elements(By.XPATH, '//*[@id="schedules"]/div[2]/div/div/div[3]/div[2]/div/span')
                                    for hotel in hotel_info:
                                        print("Day:"+str(count)+hotel.text)
                                        hotel_insideList.append("Day:"+str(count)+hotel.text)
                                        count+=1
                                    hotelList.append(hotel_insideList)
                                    hotel_insideList = []
                                except:
                                    hotelList.append("無住宿點")
                                    
                                #機票資訊
                                try:
                                    flying_and_from_info = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div[2]').find_elements(By.CLASS_NAME, "content--3WbP4") #航班與出發地點資訊
                                    for fai in flying_and_from_info:
                                        print(fai.text)
    
                                    transportation.append(fai.text) #交通資訊
                                        # ffi = flyingFromInfo.find_elements(By.XPATH, 'div/div[2]/h3') 
                                except:
                                    transportation.append("無交通資訊")
                                    
                                 #行程資料
                                try:
                                    full_trip_message = browser.find_element(By.XPATH,'//*[@id="schedules"]/div[2]').find_elements(By.CLASS_NAME,"wholeMode--1Joyg")
                                    for fulltrip in full_trip_message:
                                        fullfind =  fulltrip.find_elements(By.XPATH, 'div/div[2]/h3') #行程資訊
                                        for trip in fullfind:
                                            print(trip.text)
                                            full_tripList.append(trip.text)
                                    full_trip_message_List.append(full_tripList)
                                    full_tripList = []
    
                                except:
                                        full_trip_message_List.append("無行程資料")
                                
                                
                                print(fd.text,end="")
                                departure_DateList.append(fd.text) #日期
                                print(tn.text, tss.text, sa.text, ts.text, tse.text, p.text)
                                tripDateList.append(datecount.text) #遊玩天數
                                trip_numList.append(tn.text) #行程編號
                                tripGroupState1.append(ts.text) #成團狀況(團位).
                                tripGroupState2.append(sa.text) #成團狀況(可售)
                                tripGroupState3.append(tse.text) #成團狀況(補位)
                                tripGroupState4.append(tss.text)#成團狀況:如成形show否則為空
                                priceList.append(p.text) #價格
                                typeList.append("雄獅旅遊")
                                
                                
    
                    
                            #機票資訊
                            # try:
                            #     flying_and_from_info = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div[2]').find_elements(By.CLASS_NAME, "content--3WbP4") #航班與出發地點資訊
                            #     for faf in flying_and_from_info : 
                            #         print(faf.text) 
                            #         transportation.append(faf.text)
                            # except:
                            #         transportation.append("無交通資訊")
                            
                            
    
    
                                  
                except:
                        print("查無出發日=====all_trip_info2")
                        inside_titleList.append(titleList[time])
                        inside_urlList.append(UrlList[time])
                        departure_DateList.append("無資料")
                        tripDateList.append("無資料") #遊玩天數
                        trip_numList.append("無資料") #行程編號
                        tripGroupState1.append("無資料") #成團狀況(團位).
                        tripGroupState2.append("無資料") #成團狀況(可售)
                        tripGroupState3.append("無資料") #成團狀況(補位)
                        tripGroupState4.append("無資料")#成團狀況:如成形show否則為空
                        priceList.append("無資料")
                        typeList.append("雄獅旅遊")
                        full_trip_message_List.append("無行程資料")
                        hotelList.append("無旅館資訊") #0516 12/19test
                        transportation.append("無交通資訊")
            except:
                    print("查無網站")
                    inside_titleList.append(titleList[time])
                    inside_urlList.append(UrlList[time])
                    departure_DateList.append("查無網站")
                    tripDateList.append("查無網站") #遊玩天數
                    trip_numList.append("查無網站") #行程編號
                    tripGroupState1.append("查無網站") #成團狀況(團位).
                    tripGroupState2.append("查無網站") #成團狀況(可售)
                    tripGroupState3.append("查無網站") #成團狀況(補位)
                    tripGroupState4.append("查無網站")#成團狀況:如成形show否則為空
                    priceList.append("查無網站")
                    typeList.append("雄獅旅遊")
                    full_trip_message_List.append("查無網站")
                    hotelList.append("查無網站") #0516 12/19test
                    transportation.append("查無網站")
 





finally:
    # pass
    browser.quit()





data = pd.DataFrame({"旅遊公司名稱":typeList,
                     "標題:":inside_titleList,
                     "網址":inside_urlList,
                     "出發日期":departure_DateList,
                     "#行程編號:行程1":trip_numList,
                     "成團狀況(團位)":tripGroupState1,
                     "成團狀況(可售)":tripGroupState2,
                     "成團狀況(補位)":tripGroupState3,
                     "成團狀況(如成形show否則為空)":tripGroupState4,
                      "交通資訊 ":transportation,
                     "旅遊行程":full_trip_message_List,
                     "總天數":tripDateList,
                     "價格":priceList,
                     "住宿點":hotelList})
data.to_csv("旅遊搜尋_全部.csv",encoding="utf-8")

































