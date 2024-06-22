# -*- coding: utf-8 -*-
"""
Created on Wed May 29 19:52:26 2024

@author: Zack
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import time
import re

# 初始化資料
current_date = datetime.now()
departure_time1 = current_date.strftime("%Y-%m-%d")
two_months_later = current_date + timedelta(days=90)
departure_time2 = two_months_later.strftime("%Y-%m-%d")

# 定義變量
titleList = []
UrlList = []
inside_titleList = []
inside_urlList = []
trip_typeList = []
priceList = []
title_priceList = []
departure_DateList = []
tripDateList = []
full_trip_message_List = []
full_tripList = []
trip_numList = []

tripGroupState1 = []
tripGroupState2 = []
tripGroupState3 = []
tripGroupState4 = []
transportation = []

tour_schedual = {}
tour_schedual_List = []
hotelList = []
hotel_insideList = []
travel_company = []
typeList = []
areaList = []

# 定義定位器
locator = (By.CLASS_NAME, 'buttons--CXG5i')
next_locator = (By.XPATH, '//*[@id="root"]/div/div[4]')
inside_locator = (By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[1]/div')
date_locator = (By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/section[2]') #以第一項出發日期定位
title_locator = (By.CLASS_NAME, 'title--1dhv-')
trip_locator = (By.XPATH, '//*[@id="schedules"]/div[2]/div[2]/div')


def setup_browser():
    """ 初始化瀏覽器 """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(options=chrome_options)
    # return webdriver.Chrome()

def fetch_page_data(browser, total):
    """ 抓取當前頁面的數據 """
    title_count = 0
    page = 1
    while True:
        soup = BeautifulSoup(browser.page_source, "html.parser")
        titles = soup.select("span.caption--mphmX")
        titleUrls = soup.find_all("a", class_="cardsList--2cG2D")
        prices = soup.find_all("div", class_="sellPrice--3fg38")

        try:
            WebDriverWait(browser, 20, 0.1).until(EC.presence_of_element_located(locator))
            for title, url, price in zip(titles, titleUrls, prices):
                title_count += 1
                titleList.append(title.text)
                # title_priceList.append(price.text)不需要
                UrlList.append("https://travel.liontravel.com/" + url.get("href"))
                
                if title_count % 10 == 0:
                    browser.find_element(By.CLASS_NAME,'Style__StyledPageStyle-sc-17tz2cz-1.kGjiOf.page.next').click()
                    page += 1
                    # print(f"page = {page}")
                    # print(total)
                    # print(title_count)
                    
                if total-title_count == 0:
                    return fetch_inside_information(browser)
                    
        except Exception as e:
            print(f"Error in pagination: {str(e)}")
            return fetch_inside_information(browser)

def fetch_inside_information(browser):
    """ 抓取內頁的詳細信息 """
    try:
        for index, url in enumerate(UrlList):
            browser.get(url)
            WebDriverWait(browser, 20, 0.1).until(EC.presence_of_element_located(date_locator))
            # print(f"{index + 1}. {titleList[index]}")
            # print(browser.current_url)
            
            WebDriverWait(browser, 20, 0.1).until(EC.presence_of_element_located(inside_locator))
            datecount = browser.find_element(By.CLASS_NAME, 'days--3UNv4')
            check_List = browser.find_element(By.CLASS_NAME, 'text--1L79t')
            # print(datecount.text)
            
            #如果是日曆顯示，切換為列表顯示
            if check_List.text == "列表顯示":
                ActionChains(browser).click(check_List).perform()
                
                
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/section[1]')))
            all_trip_info = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/div[3]/div/div[2]/div/div[2]').find_elements(By.TAG_NAME, "div") #列表顯示
            for trip_info in all_trip_info:
                WebDriverWait(browser, 20, 0.2).until(EC.presence_of_element_located(date_locator))
                fromDate = trip_info.find_elements(By.XPATH, 'section[2]/div/div[1]') #出發日期
                trip_num = trip_info.find_elements(By.XPATH, 'section[2]/div/div[2]') #行程編號
                trip_state_show = trip_info.find_elements(By.XPATH, 'section[2]/div/div[3]') #若以成行show成行，若無為空
                sellable = trip_info.find_elements(By.XPATH, 'section[2]/div/div[7]') #剩餘可賣
                totalsell = trip_info.find_elements(By.XPATH, 'section[2]/div/div[8]') #總席次
                trip_state = trip_info.find_elements(By.XPATH, 'section[2]/div/div[5]') #報名狀態
                price = trip_info.find_elements(By.XPATH, 'section[2]/div/div[9]') #價格
                tripType = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div[1]/div[1]/img').get_attribute("alt") #旅遊類型查詢
                
                count = 1
                for fd, tn, tss, sa, ts, tse, p in zip(fromDate, trip_num, trip_state_show, sellable, totalsell, trip_state, price):
                    #標題
                    # print(f"{index + 1}. {titleList[index]}")
                    
                    #連結
                    # print(url)
                    
                    # 旅遊類型查詢不需要
                    # print(tripType)

                        
                    # 行程資料與旅館合併
                    full_tripList = []
                    hotel_insideList = []
                    tour_schedual = {}
                    try:
                        WebDriverWait(browser, 20, 0.2).until(EC.presence_of_element_located(trip_locator))
                        full_trip_message = browser.find_element(By.XPATH, '//*[@id="schedules"]/div[2]').find_elements(By.CLASS_NAME, "wholeMode--1Joyg")
                        hotel_info = browser.find_elements(By.XPATH, '//*[@id="schedules"]/div[2]/div/div/div[3]/div[2]/div/span')
                        #行程資訊
                        for fulltrip in full_trip_message:
                            fullfind = fulltrip.find_elements(By.XPATH, 'div/div[2]/h3') 
                            for trip, hotel in zip(fullfind, hotel_info):
                                # print(f"D{count}{trip.text}")
                                # print(f"D{count}{hotel.text}")
                                full_tripList.append(f"D{count}{trip.text}")
                                hotel_insideList.append(f"D{count}{hotel.text}")
                                # print(f"D{count} {trip.text} {hotel.text}", end="")
                                tour_schedual[f"D{count}"] = {'schedual': [trip.text], 'posible_hotel': [hotel.text]}
                                count += 1
                                
                    except NoSuchElementException:
                        WebDriverWait(browser, 20, 0.2).until(EC.presence_of_element_located(trip_locator))
                        full_trip_message = browser.find_element(By.XPATH, '//*[@id="schedules"]/div[2]').find_elements(By.CLASS_NAME, "wholeMode--1Joyg")
                        for fulltrip in full_trip_message:
                            fullfind = fulltrip.find_elements(By.XPATH, 'div/div[2]/h3') #行程資訊
                            for trip in fullfind:
                                # print(f"D{count}{trip.text} NO~~~posible_hotel")
                                tour_schedual[f"D{count}"] = {'schedual': [trip.text], 'posible_hotel': [""]}
                                count += 1
                    # 出發資訊
                    try:
                        flying_and_from_info = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div[2]').find_element(By.XPATH, "div[2]") #出發地點資訊
                        flying_and_from_info = flying_and_from_info.text.replace('\n', ' ')
                        # print(flying_and_from_info)
                        
                        
                        transportation.append(flying_and_from_info) #出發資訊
                    except:
                          transportation.append("")
                          
                                
                    full_trip_message_List.append(full_tripList)
                    hotelList.append(hotel_insideList)
                    tour_schedual_List.append(tour_schedual)


                    #內頁的title/url/typeList 
                    inside_titleList.append(titleList[index])
                    inside_urlList.append(url)
                    trip_typeList.append(tripType)
                    
                    # 日期date
                    # print(fd.text, end="")
                    clean_date_str = re.sub(r"\s*\(.*?\)", "", fd.text)
                    departure_DateList.append(clean_date_str) 
                    # print(tn.text, tss.text, sa.text, ts.text, tse.text, p.text)
                    
                    # 總天數
                    need_re = datecount.text 
                    match = re.findall(r'\d+', need_re)[0]
                    tripDateList.append(match) #遊玩天數
                    
                    trip_numList.append(tn.text) #行程編號
                    tripGroupState1.append(ts.text) #成團狀況(團位)
                    tripGroupState2.append(sa.text + "人") #成團狀況(可售)
                    tripGroupState3.append(tse.text) #成團狀況(補位)
                    tripGroupState4.append(tss.text) #成團狀況:如成形show否則為空
                    
                    # 價格
                    need_re = p.text
                    numeric_part = re.sub(r"[^\d]", "", need_re)
                    priceList.append(numeric_part)
                    
                    areaList.append(area)
                    travel_company.append("雄獅旅遊")

    except Exception as e:
        print(f"Error fetching information for {url}: {str(e)}")
        inside_titleList.append(titleList[index])
        inside_urlList.append(url)
        trip_typeList.append("")
        departure_DateList.append("")
        tripDateList.append("")
        trip_numList.append("")
        tripGroupState1.append("")
        tripGroupState2.append("")
        tripGroupState3.append("")
        tripGroupState4.append("")
        priceList.append("")
        typeList.append("")
        areaList.append(area)
        full_trip_message_List.append("")
        hotelList.append("")
        transportation.append("")
        travel_company.append("雄獅旅遊")
        tour_schedual_List.append("")
            
    UrlList.clear()   
    titleList.clear()

def main():
    browser = setup_browser()
    global area    

    browser_url = [ ("https://travel.liontravel.com/search?DepartureID=&ArriveID=--4,&GoDateStart=" + departure_time1 + "&GoDateEnd=" + departure_time2 + "&Keywords=&TravelType=1&IsSold=true&Platform=APP", "其他"),
                    ("https://travel.liontravel.com/search?DepartureID=&ArriveID=--6,&GoDateStart=" + departure_time1 + "&GoDateEnd=" + departure_time2 + "&Keywords=&TravelType=1&IsSold=true&Platform=APP", "東北亞"),
                    ("https://travel.liontravel.com/search?DepartureID=&ArriveID=--2,&GoDateStart=" + departure_time1 + "&GoDateEnd=" + departure_time2 + "&Keywords=&TravelType=1&IsSold=true&Platform=APP", "大洋洲"),
                    ("https://travel.liontravel.com/search?DepartureID=&ArriveID=--5,&GoDateStart=" + departure_time1 + "&GoDateEnd=" + departure_time2 + "&Keywords=&TravelType=1&IsSold=true&Platform=APP", "大陸港澳"),
                    ("https://travel.liontravel.com/search?DepartureID=&ArriveID=--7,&GoDateStart=" + departure_time1 + "&GoDateEnd=" + departure_time2 + "&Keywords=&TravelType=1&IsSold=true&Platform=APP", "東南亞"),
                    ("https://travel.liontravel.com/search?DepartureID=&ArriveID=--3,&GoDateStart=" + departure_time1 + "&GoDateEnd=" + departure_time2 + "&Keywords=&TravelType=1&IsSold=true&Platform=APP", "歐洲"),
                    ("https://travel.liontravel.com/search?DepartureID=&ArriveID=--1,&GoDateStart=" + departure_time1 + "&GoDateEnd=" + departure_time2 + "&Keywords=&TravelType=1&IsSold=true&Platform=APP", "美洲"),
                    ("https://travel.liontravel.com/search?DepartureID=&ArriveID=--9,&GoDateStart=" + departure_time1 + "&GoDateEnd=" + departure_time2 + "&Keywords=&TravelType=1&IsSold=true&Platform=APP", "台灣"),]
    try:
        for url, area in browser_url:
            browser.get(url)
            # print(f"成功訪問 {area}")
            # print(browser.current_url)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(locator))
            soup = BeautifulSoup(browser.page_source, "html.parser")
            total = int(soup.find("div", class_="ItemQty--kVIvw").text.split("項")[0])
            # print(f"{total}項精彩行程")
            fetch_page_data(browser, total)
                
            data = pd.DataFrame({
                "travel_company": travel_company,
                "area": areaList,
                "title": inside_titleList,
                "price": priceList,
                "date": departure_DateList,
                "departure_city": transportation, #出發地
                "duration": tripDateList,
                "remaining_quota": tripGroupState2,
                "tour_schedule": tour_schedual_List,
                "url": inside_urlList,
            })
            
            # data.to_csv("liontrip_0620{area}.csv", encoding="utf-8")

    finally:
        browser.quit()
        
        return data


