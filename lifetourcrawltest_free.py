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
formatted_datetime = current_datetime.strftime('%Y/%m/%d %H:%M:%S').split(" ")[0]

def init_driver(maximized = False, incognito = False, headless = False, extension = False, popup_blocking = False, set_window_size= True,set_window_size_2= True):
    
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
    
    if set_window_size:
        driver.maximize_window()
        # print(driver.get_window_size())
    
    print("driver設置完成")
    return driver
browser = init_driver(maximized = True, headless=False)#計數器
tour_data_count = 0
# 讀取每個網址進去
# for url in newurls:
url = "https://package.lifetour.com.tw/detail/KIXF2MMTPE12#KIXF5MM24525T01"
data = {}
all_handles = browser.window_handles
first_window_handle = all_handles[0]
browser.switch_to.window(first_window_handle)
browser.execute_script("window.open('" + url + "', '_blank');")
all_handles = browser.window_handles
new_window_handle = all_handles[-1]
browser.switch_to.window(new_window_handle)

browser.find_element(By.TAG_NAME,'body').send_keys(Keys.SPACE)
time.sleep(0.2)
try:
    WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="calendar"]/div[3]/ul')))
except Exception as error:
    print(error)

#湯
soup = bs(browser.page_source, 'html.parser')

#抓取的內容
data["company"] = "五福旅遊"
data["title"] = soup.select_one("div.prod-name").text.strip()
data["date"] = soup.find("div", string="出發日期").find_next_sibling("div").text.strip()
try:
    data["departure_city"] = soup.find("div", string="出發機場").find_next_sibling("div").text.strip()
except:
    pass
data["duration"] = soup.find("div", string="旅遊天數").find_next_sibling("div").text.strip()
price = soup.select_one("div.price-bar")
for div in price.find_all("div")[1:2]:
    data["price"] = div.text
data["type"] = "套裝行程"#
data["tourist_destination"] = soup.find("div", string="旅遊地點").find_next_sibling("h2").text.strip()
# try:
#     statusList = soup.find("ul", class_="wrap-status")
#     for li in statusList.find_all("li"):
#         key = li.find("span").text
#         value = li.find("div").text
#         data[key] = value
try:
    statusList = soup.find("ul", class_="wrap-status")
    for li in statusList.find_all("li"):
        try:
            
            key = li.find("span").text.strip()
            if key == "可售人數":
                data["remaining_quota"] = li.find("div").text.strip()
            elif key == "成行人數":
                data["get_group成行人數"] = li.find("div").text.strip()
            elif key == "團位":
                data["group_quota"] = li.find("div").text.strip()
            elif key == "成團狀況":
                data["waiting_List成團狀況"] = li.find("div").text.strip()
        except:
            pass

except:
    data["remaining_quota"] = ""
    data["get_group成行人數"] = ""
    data["group_quota"] = ""
    data["waiting_List成團狀況"] = ""
# 取得去程航班資訊
go_flight_section = soup.find("section", {"id": "airportInfo"})
if go_flight_section:
    go_flight_info = go_flight_section.find_all("div", class_="wrap-flyInfo")
    if go_flight_info:
        # 去程航班資訊
        go_flight = go_flight_info[0]
        data["go_date"] = go_flight.find("div", class_="date").text.strip()
        data["go_departure_city"] = go_flight.find("div", class_="airport").find_all("span")[0].text.strip()
        data["go_arrive_city"] = go_flight.find("div", class_="airport").find_all("span")[1].text.strip()
        data["go_departure_time"] = go_flight.find("div", class_="fly-port").find_all("b")[0].text.strip()
        data["go_arrive_time"] = go_flight.find("div", class_="fly-port").find_all("b")[1].text.strip()
        data["go_company"] = go_flight.find("div", class_="airplanInfo").find("div", class_="text").find_all("span")[0].text.strip()
        data["go_flightNo"] = go_flight.find("div", class_="airplanInfo").find("div", class_="text").find_all("span")[1].text.strip()

        # 回程航班資訊
        back_flight = go_flight_info[1]
        data["back_date"] = back_flight.find("div", class_="date").text.strip()
        data["back_departure_city"] = back_flight.find("div", class_="airport").find_all("span")[0].text.strip()
        data["back_arrive_city"] = back_flight.find("div", class_="airport").find_all("span")[1].text.strip()
        data["back_departure_time"] = back_flight.find("div", class_="fly-port").find_all("b")[0].text.strip()
        data["back_arrive_time"] = back_flight.find("div", class_="fly-port").find_all("b")[1].text.strip()
        data["back_company"] = back_flight.find("div", class_="airplanInfo").find("div", class_="text").find_all("span")[0].text.strip()
        data["back_flightNo"] = back_flight.find("div", class_="airplanInfo").find("div", class_="text").find_all("span")[1].text.strip()

# 取得行程資訊
schedule_section = soup.find("section", {"id": "tripSpec"})
if schedule_section:
    data["tour_schedual"] = schedule_section.text.strip()

# 網頁URL
data["tour_page_url"] = url


#顯示抓取的字典內容
for key, value in list(data.items()):
    print(f"{key} : {value}")
#放進tourDatas[]
# tour_datas.append(data)

#印出當前完成第幾筆資料
tour_data_count += 1
# print(f"有 {len(newurls)} 筆行程，已完成第{tour_data_count}筆資料")
browser.quit()
# all_handles = browser.window_handles
# new_window_handle = all_handles[-1]
# browser.switch_to.window(new_window_handle)
'''
    #存到csv
    df = pd.DataFrame(tour_datas)
    # df.to_csv(f'travel_data_{out_region_options[out_region_input-1]}{zone_options[int(zone_input)-1]}.csv', index=False, encoding='utf_8_sig')
    # departur_name = departure_options[int(departure_index)-1]
    # sanitized_departur_name = sanitize_filename(departur_name)
    # file_name = f"travel_data_出發地{sanitized_departur_name}-不限目的地.csv"
    file_name = "lifetour_out_domestic_itinerary.csv"
    if df.empty:
        print(f"{file_name}沒有資料")
    else:
        df.to_csv(file_name, index=False, encoding='utf_8_sig')
        print(f'文件已保存為: {file_name}')
'''