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
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import re
import time

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%Y/%m/%d %H:%M:%S').split(" ")[0]
faillinks_list = []

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
def init_driver(maximized = False, incognito = False, headless = False, extension = False, popup_blocking = False, set_window_size= True):
    
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
        driver.set_window_size(1920, 1080)

    print("driver設置完成")
    return driver

"""
    描述: 剔除無效的字元
    備註: 無
"""
invalid_chars = ':/\?%*|"<>．'  # 定義一組無效字元
def sanitize_filename(filename):
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


'''
    描述: 確認元素存在並可見，執行點擊
    備註: 無
'''
def click_element(driver, element):
    try:
        # 確認元素存在於 DOM 中
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        # 確認元素在視窗中可見
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, element)))
        elem = driver.find_element(By.XPATH, element)
        
        # 將元素滾動到視窗中
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        
        ActionChains(driver).click(elem).perform()
        # print("點擊元素成功")
    except Exception as e:
        print(f"點擊元素失敗: {e}")

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
def group_travel_search_in():
    tour_datas = []
    #設定webdriver
    browser = init_driver(maximized = True, headless=False)
    
    #載入頁面
    browser.get('https://www.lifetour.com.tw/')
    
    #等待搜尋條載入
    try:
        WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]')))
    except Exception as error:
        print(error)
        return
    
    # #點擊國內按鈕
    click_element(browser, '//*[@id="searchPanel"]/div[3]/div[2]')

     # --------------------------------------------------------------------
     # 點擊出發地表單
    click_element(browser, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div')

    #抓取表單內容
    departure_options = [city.text for city in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li')]
    print(departure_options)
    #迴圈跑出發地
    for departure_index, departure_option in enumerate(departure_options, start = 1):
        print(departure_index,departure_option)
        #維持在最初頁面
        all_handles = browser.window_handles
        first_window_handle = all_handles[0]
        browser.switch_to.window(first_window_handle)
        #點擊出發地格
        if departure_index != 1:
            click_element(browser, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div')
        # 選擇出發地
        click_element(browser, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li[{}]'.format(str(departure_index)))
        
        #點擊地區表單
        click_element(browser, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[2]')
        
        #選擇台灣-不限目的地
        click_element(browser, '//*[@id="search-tab-0"]/div[1]/div[2]/a[1]')


        #--------------------------------------------------------------------
        #點擊出發日期表單
        click_element(browser,'//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[1]')

        #抓取可選年份
        year_options = [year.get_attribute('value').split("/")[1] for year in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/div/select[2]/option')]
        #輸入出發日期
        date_input = formatted_datetime
        #檢查日期格式
        if re.compile('\d{4}/\d{2}/\d{2}').match(date_input) != None:
            #拆分日期
            year = date_input.split("/")[0]
            month = date_input.split("/")[1].lstrip('0')
            day = date_input.split("/")[2].lstrip('0')
            # #檢查年分是否可選
            if year in year_options:
                #取得輸入年份選項位置並點擊
                year_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇年份"]')
                # 使用 ActionChains 模擬點擊年份下拉選單
                actions = ActionChains(browser)
                actions.move_to_element(year_list_locator).click().perform()
                # 選擇年份
                select = Select(year_list_locator)
                select.select_by_visible_text(year)
                #抓取可選月份
                month_options = [month.get_attribute('value') for month in browser.find_elements(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]/option')]
                # 檢查月份是否可選 
                if month in [m.split("/")[0] for m in month_options]:
                    # 取得月份表單位置並點擊
                    month_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]')
                    ActionChains(browser).click(month_list_locator).perform()
                    # 選擇月份
                    select = Select(month_list_locator)
                    option_value = month + '/' + year
                    select.select_by_value(option_value)
                    try:
                        WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table')))
                    except Exception as error:
                        print(error)
                    #取得可選日
                    week_List = []
                    day_options = []
                    week_numbers = [week_numbers.text for week_numbers in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr')]
                    # print(week_numbers)
                    for i in range(len(week_numbers)+1):
                        day_option = [day.text for day in browser.find_elements(By.XPATH, '//div[@id="searchPanel"]//div[contains(@class,"datepick-month-row")]//table//tr[{}]/td'.format(i)) if day.text.strip()]
                        day_options.extend(day_option)
                    # print(day_options)
                    for i in range(len(week_numbers)):
                        week_options = [week.text for week in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td'.format(i+1))]
                        # print(week_options)
                        week_List.append(week_options)
                        # 檢查日期是否過期
                    if eval(day) >= current_datetime.day:
                        for i in range(len(week_List)):
                            for j in range(len(week_List[i])):
                                if week_List[i][j] == day:
                                    # print(i, j)
                                    #檢查輸入日期選項位置並點擊
                                    click_element(browser, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td[{}]'.format(i+1,j+1))

                    else:
                        print("請選擇" + '(' + str(day_options)[current_datetime.day].replace('[', '').replace(']', '').replace("'", '').replace(',', ' ').lstrip().rstrip().replace('  ', ',') + ')' + ": ")
                else:
                    print("請選擇" + str(month_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
            else:
                print("請選擇" + str(year_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
        else:
            print("格式錯誤!")
        
        # --------------------------------------------------------------------
        #關閉截止日表單
        close_deadline = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[3]/a[2]')
        ActionChains(browser).click(close_deadline).perform()
        # --------------------------------------------------------------------
        #點擊搜索按鈕
        click_element(browser, '//*[@id="btn_search_pc"]')
        
        #--------------------------------------------------------------------
        #轉移到新分頁
        window_handles = browser.window_handles
        browser.switch_to.window(window_handles[-1])
        
        #等待頁面跳轉
        try:
            WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SearchList"]')))
        except Exception as error:
            print(error)
        
        #畫面移到最底
        # 獲取頁面高度
        last_height = browser.execute_script("return document.body.scrollHeight")
        
        while True:
            # 滾動到底部
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # 等待頁面加載新內容
            time.sleep(1)
            
            # 計算新的頁面高度並和之前的高度對比
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        #抓所有行程網址
        tour_links = [tour_link.get_attribute("href") for tour_link in browser.find_elements(By.XPATH, '//div[contains(@class, "item-list")]/div/a')]
        print(f"有 {len(tour_links)} 筆區域行程網址")
        browser.close()
        #--------------------------------------------------------------------
        #開連結網址
        datesList = []
        setnumList = []
        newurls = []
        tour_links_count = 0
        
        for links in tour_links:
            try:
                browser.switch_to.window(first_window_handle)
                browser.execute_script("window.open('" + links + "', '_blank');")
                all_handles = browser.window_handles
                new_window_handle = all_handles[-1]
                browser.switch_to.window(new_window_handle)
                time.sleep(0.5)
                #往後點擊最多5個的月份，讓行程跑完
                previous_month = ""
                count = 0
                while count < 6:
                    try:
                        # 抓取按鈕月份
                        current_month = browser.find_element(By.XPATH, '//*[@id="calendar"]/div[2]/div[1]/span').text
                        if current_month == previous_month:
                            break
                        previous_month = current_month
                        # 等待 "下個月" 按钮可
                        next_month = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="calendar"]/div[2]/a[2]')))
                        # 點擊 "下個月" 按钮
                        ActionChains(browser).move_to_element(next_month).click().perform()
                        time.sleep(0.2)
                        count += 1
                    except TimeoutException:
                        print("等待超時，停止迴圈")
                        break
                if count == 6:
                    print("已經迴圈6次，停止迴圈")
                
                # 抓有成團的id
                group_id = links.split("/")[-1].split("#")[0]
                
                # 解析頁面內容
                soup = bs(browser.page_source, 'html.parser')
                
                # 整理每個成團的網址
                for li in soup.find_all('li', attrs={'data-mcode': group_id}):
                    if li.get('data-more') == "true":
                        pass
                    else:
                        datesList.append(li['data-date'])
                        setnum = li['data-scode']
                        setnumList.append(setnum)
                        newurls.append(links.split("#")[0] + "#" + setnum)
                
                tour_links_count += 1
                print(f"已完成第{tour_links_count}筆資料")
            
            except Exception as error:
                print(f"處理 {links} 時發生錯誤: {error}")
                continue
            browser.close() 
        print(f"有 {len(newurls)} 筆行程")
        
        #--------------------------------------------------------------------
        #計數器
        tour_data_count = 0
        # 讀取每個網址進去
        for url in newurls:
            data = {}
            # all_handles = browser.window_handles
            # new_window_handle = all_handles[-1]
            browser.switch_to.window(first_window_handle)
            browser.execute_script("window.open('" + url + "', '_blank');")
            all_handles = browser.window_handles
            new_window_handle = all_handles[-1]
            browser.switch_to.window(new_window_handle)
            
            browser.find_element(By.TAG_NAME,'body').send_keys(Keys.SPACE)
            time.sleep(0.4)
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="calendar"]/div[3]/ul')))
            except Exception as error:
                print(error)
            
            #湯
            soup = bs(browser.page_source, 'html.parser')

            #抓取的內容
            data["company"] = "五福旅遊"
            data["region"] = departure_option
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
            schedule_section = soup.find("section", {"id": "schedule"})
            # if schedule_section:
            #     data["tour_schedual"] = schedule_section.text.strip()
            if schedule_section:
                tour_schedule = {}
                day_count = 1
                for day_schedule in schedule_section.find_all("div", class_="schedule-box"):
                    hotel_info = day_schedule.find("div", class_="wrap-hotel")
                    if hotel_info:
                        hotel_name = [hotel_info.find("div", class_="text").text.strip()]
                    else:
                        hotel_name = []

                    # 使用相對路徑選取包含行程資訊的文本內容
                    schedule_xpath = day_schedule.find("div", class_="default-text")
                    if schedule_xpath:
                        schedule_text = schedule_xpath.get_text(separator="\n").strip()
                        # 清理文本，移除多餘的空白字符和轉義字符
                        schedule_text = ' '.join(schedule_text.split()).replace('\u3000', '')
                    else:
                        schedule_text = ""

                    schedule = [part.strip() for part in schedule_text.split("＞") if part.strip()]

                    tour_schedule[f"D{day_count}"] = {"schedule": schedule, "possible_hotel": hotel_name}
                    day_count += 1

                data["tour_schedule"] = tour_schedule

            # 網頁URL
            data["tour_page_url"] = url
            #顯示抓取的字典內容
            # for key, value in list(data.items()):
            #     print(f"{key} : {value}")
            #放進tourDatas[]
            tour_datas.append(data)
            
            #印出當前完成第幾筆資料
            tour_data_count += 1
            print(f"有 {len(newurls)} 筆行程，已完成第{tour_data_count}筆資料")
            browser.close()
    
    return pd.DataFrame(tour_datas)
    # #存到csv
    # df1 = pd.DataFrame(tour_datas)
    # file_name = "lifetour_in.csv"
    # if df1.empty:
    #     print(f"{file_name}沒有資料")
    # else:
    #     df1.to_csv(file_name, index=False, encoding='utf_8_sig')
    #     print(f'文件已保存為: {file_name}')


#travel_type available
def group_travel_search_out():
    tour_datas = []
    #設定webdriver
    browser = init_driver(maximized = True, headless=False)

    #載入頁面
    browser.get('https://www.lifetour.com.tw/')

    browser.find_element(By.TAG_NAME,'body').send_keys(Keys.SPACE)
    
    #等待搜尋條載入
    try:
        WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]')))
    except Exception as error:
        print(error)
        return
    #預設是國外不用點
    # --------------------------------------------------------------------
    # 點擊出發地表單
    departure_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div')
    ActionChains(browser).click(departure_select_form).perform()
    # 等待出發地表單出現
    try:
        WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul')))
    except Exception as error:
        print(error)
        browser.close()
        browser.quit()
    
    #抓取表單內容
    departure_options = [city.text for city in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li')]
    #迴圈跑出發地
    for departure_index, departure_option in enumerate(departure_options, start = 1):
        if departure_index in [2,3]:
            pass
        # elif departure_index in [7]:
        #     pass
        else:
            print(departure_index,departure_option)
            #載入頁面
            all_handles = browser.window_handles
            first_window_handle = all_handles[0]
            browser.switch_to.window(first_window_handle)
            #點擊國內按鈕
            bound_in_button = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[3]/div[2]')
            ActionChains(browser).click(bound_in_button).perform()
            departure_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div')
            ActionChains(browser).click(departure_select_form).perform()
            #點擊國外按鈕
            bound_in_button = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[3]/div[1]')
            ActionChains(browser).click(bound_in_button).perform()
            # browser.find_element(By.TAG_NAME,'body').send_keys(Keys.SPACE)
            # 點擊出發地表單
            departure_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div')
            ActionChains(browser).click(departure_select_form).perform()
            # 等待出發地表單出現
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul')))
            except Exception as error:
                print(error)
            departure_input = str(departure_index)
            departure_city_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li[{}]'.format(departure_input))
            ActionChains(browser).click(departure_city_locator).perform()
            
            # 點擊地區表單
            region_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[2]')
            ActionChains(browser).click(region_select_form).perform()
            #等待地區表單出現
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="popupMenuPanel"]/div[2]')))
            except Exception as error:
                print(error)
            #點擊洲的列表選單
            continents_options = [continent.text for continent in browser.find_elements(By.XPATH, '//*[@id="popupMenuPanel"]/div[2]/div[2]/div/a')]
            for continents_index, continents_option in enumerate(continents_options, start = 1):
                print(continents_option)
                # if continents_index != "1":
                all_handles = browser.window_handles
                first_window_handle = all_handles[0]
                browser.switch_to.window(first_window_handle)
                region_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[2]')
                ActionChains(browser).click(region_select_form).perform()
                continents_select_form = browser.find_element(By.XPATH, '//*[@id="popupMenuPanel"]/div[2]/div[2]/div/a[{}]'.format(continents_index))
                time.sleep(0.1)
                ActionChains(browser).click(continents_select_form).perform()
                # else:
                #     pass
                # 抓取內部表單內容
                region_options = [out_region.text for out_region in browser.find_elements(By.XPATH, '//div[@class="item-head"]/a') if out_region.text]
                for  region_index, region_option in enumerate(region_options, start = 1):
                    print(region_option)
                    all_handles = browser.window_handles
                    first_window_handle = all_handles[0]
                    browser.switch_to.window(first_window_handle)
                    option_element = browser.find_element(By.XPATH, f'//div[@class="item-head"]/a[text()="{region_options[region_index-1]}"]')
                    actions = ActionChains(browser)
                    time.sleep(0.1)
                    actions.move_to_element(option_element)
                    browser.execute_script('arguments[0].click()',option_element)
                    #--------------------------------------------------------------------
                    #點擊出發日期表單
                    time_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[1]')
                    ActionChains(browser).click(time_select_form).perform()
                    #等待日期表單出現
                    try:
                        WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div')))
                    except Exception as error:
                        print(error)
                    #抓取可選年份
                    year_options = [year.get_attribute('value').split("/")[1] for year in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/div/select[2]/option')]
                    #輸入出發日期
                    date_input = formatted_datetime
                    #檢查日期格式
                    if re.compile('\d{4}/\d{2}/\d{2}').match(date_input) != None:
                        #拆分日期
                        year = date_input.split("/")[0]
                        month = date_input.split("/")[1].lstrip('0')
                        day = date_input.split("/")[2].lstrip('0')
                        # #檢查年分是否可選
                        if year in year_options:
                            #取得輸入年份選項位置並點擊
                            year_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇年份"]')
                            # 使用 ActionChains 模擬點擊年份下拉選單
                            actions = ActionChains(browser)
                            actions.move_to_element(year_list_locator).click().perform()
                            # 選擇年份
                            select = Select(year_list_locator)
                            select.select_by_visible_text(year)
                            #抓取可選月份
                            month_options = [month.get_attribute('value') for month in browser.find_elements(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]/option')]
                            # 檢查月份是否可選 
                            if month in [m.split("/")[0] for m in month_options]:
                                # 取得月份表單位置並點擊
                                month_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]')
                                ActionChains(browser).click(month_list_locator).perform()
                                # 選擇月份
                                select = Select(month_list_locator)
                                option_value = month + '/' + year
                                select.select_by_value(option_value)
                                try:
                                    WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table')))
                                except Exception as error:
                                    print(error)
                                #取得可選日
                                week_List = []
                                day_options = []
                                week_numbers = [week_numbers.text for week_numbers in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr')]
                                # print(week_numbers)
                                for i in range(len(week_numbers)+1):
                                    day_option = [day.text for day in browser.find_elements(By.XPATH, '//div[@id="searchPanel"]//div[contains(@class,"datepick-month-row")]//table//tr[{}]/td'.format(i)) if day.text.strip()]
                                    day_options.extend(day_option)
                                # print(day_options)
                                for i in range(len(week_numbers)):
                                    week_options = [week.text for week in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td'.format(i+1))]
                                    # print(week_options)
                                    week_List.append(week_options)
                                    # 檢查日期是否過期
                                if eval(day) >= current_datetime.day:
                                    for i in range(len(week_List)):
                                        for j in range(len(week_List[i])):
                                            if week_List[i][j] == day:
                                                # print(i, j)
                                                #檢查輸入日期選項位置並點擊
                                                day_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td[{}]'.format(i+1,j+1))
                                                ActionChains(browser).click(day_locator).perform()#//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[5]/td[2]
                                else:
                                    print("請選擇" + '(' + str(day_options)[current_datetime.day].replace('[', '').replace(']', '').replace("'", '').replace(',', ' ').lstrip().rstrip().replace('  ', ',') + ')' + ": ")
                            else:
                                print("請選擇" + str(month_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
                        else:
                            print("請選擇" + str(year_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
                    else:
                        print("格式錯誤!")
                    # --------------------------------------------------------------------
                    #關閉截止日表單
                    close_deadline = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[3]/a[2]')
                    ActionChains(browser).click(close_deadline).perform()
                    
                    #點擊搜索按鈕
                    # browser.find_element(By.XPATH, '//*[@id="btn_search_pc"]').click()
                    search_button = browser.find_element(By.XPATH, '//*[@id="btn_search_pc"]')
                    
                    # 使用 execute_script 模擬點擊按鈕
                    browser.execute_script("arguments[0].click();", search_button)
                    #--------------------------------------------------------------------
                    #轉移到新分頁
                    window_handles = browser.window_handles
                    browser.switch_to.window(window_handles[-1])
                    
                    #等待頁面跳轉
                    try:
                        WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SearchList"]')))
                    except Exception as error:
                        print(error)
                    
                    #畫面移到最底
                    # 獲取頁面高度
                    last_height = browser.execute_script("return document.body.scrollHeight")
                    
                    while True:
                        # 滾動到底部
                        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        
                        # 等待頁面加載新內容
                        time.sleep(1)
                        
                        # 計算新的頁面高度並和之前的高度對比
                        new_height = browser.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height
                    
                    #抓所有行程網址
                    tour_links = [tour_link.get_attribute("href") for tour_link in browser.find_elements(By.XPATH, '//div[contains(@class, "item-list")]/div/a')]
                    print(f"有 {len(tour_links)} 筆區域行程網址")
                    browser.close()
                    #--------------------------------------------------------------------
                    #開連結網址
                    
                    datesList = []
                    setnumList = []
                    newurls = []
                    tour_links_count = 0
                    
                    for links in tour_links:
                        try:
                            browser.switch_to.window(first_window_handle)
                            browser.execute_script("window.open('" + links + "', '_blank');")
                            all_handles = browser.window_handles
                            new_window_handle = all_handles[-1]
                            browser.switch_to.window(new_window_handle)
                            time.sleep(0.5)
                            #往後點擊最多5個的月份，讓行程跑完
                            previous_month = ""
                            count = 0
                            while count < 6:
                                try:
                                    # 抓取按鈕月份
                                    current_month = browser.find_element(By.XPATH, '//*[@id="calendar"]/div[2]/div[1]/span').text
                                    if current_month == previous_month:
                                        break
                                    previous_month = current_month
                                    # 等待 "下個月" 按钮可
                                    next_month = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="calendar"]/div[2]/a[2]')))
                                    # 點擊 "下個月" 按钮
                                    ActionChains(browser).move_to_element(next_month).click().perform()
                                    time.sleep(0.2)
                                    count += 1
                                except TimeoutException:
                                    print("等待超時，停止迴圈")
                                    break
                            if count == 6:
                                print("已經迴圈6次，停止迴圈")
                            
                            # 抓有成團的id
                            group_id = links.split("/")[-1].split("#")[0]
                            
                            # 解析頁面內容
                            soup = bs(browser.page_source, 'html.parser')
                            
                            # 整理每個成團的網址
                            for li in soup.find_all('li', attrs={'data-mcode': group_id}):
                                if li.get('data-more') == "true":
                                    pass
                                else:
                                    datesList.append(li['data-date'])
                                    setnum = li['data-scode']
                                    setnumList.append(setnum)
                                    newurls.append(links.split("#")[0] + "#" + setnum)
                            
                            tour_links_count += 1
                            print(f"已完成第{tour_links_count}筆資料")
                        
                        except Exception as error:
                            print(f"處理 {links} 時發生錯誤: {error}")
                            faillinks_list.append(links)
                            continue
                        browser.close() 
                    print(f"有 {len(newurls)} 筆行程")
                    #--------------------------------------------------------------------
                    #計數器
                    tour_data_count = 0
                    # 讀取每個網址進去
                    for url in newurls:
                        data = {}
                        # all_handles = browser.window_handles
                        # new_window_handle = all_handles[-1]
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
                        data["region"] = region_option
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
                        schedule_section = soup.find("section", {"id": "schedule"})
                        # if schedule_section:
                        #     data["tour_schedual"] = schedule_section.text.strip()
                        if schedule_section:
                            tour_schedual = {}
                            day_count = 1
                            for day_schedule in schedule_section.find_all("div", class_="schedule-box"):
                                day_title = day_schedule.find("h3", class_="head").text.strip()
                                hotel_info = day_schedule.find("div", class_="wrap-hotel")
                                if hotel_info:
                                    hotel_name = [hotel_info.find("div", class_="text").text.strip()]
                                else:
                                    hotel_name = []
                                
                                schedual = [part.strip() for part in day_title.split("＞") if part.strip()]
                                sub_titles = day_schedule.find_all("span", {"style": "font-family: 微軟正黑體;color:#0000FF;"})
                                sub_titles = [sub_title.text.strip() for sub_title in sub_titles]
                                schedual.extend(sub_titles)
                                
                                tour_schedual[f"D{day_count}"] = {"schedual": schedual, "posible_hotel": hotel_name}
                                day_count += 1
                            
                            data["tour_schedual"] = tour_schedual
                        # 網頁URL
                        data["tour_page_url"] = url
                        #顯示抓取的字典內容
                        # for key, value in list(data.items()):
                        #     print(f"{key} : {value}")
                        #放進tourDatas[]
                        tour_datas.append(data)
                        
                        #印出當前完成第幾筆資料
                        tour_data_count += 1
                        print(f"有 {len(newurls)} 筆行程，已完成第{tour_data_count}筆資料")
                        browser.close()
    return pd.DataFrame(tour_datas)
    #存到csv
    # df2 = pd.DataFrame(tour_datas)
    # file_name = "lifetour_out.csv"
    # if df2.empty:
    #     print(f"{file_name}沒有資料")
    # else:
    #     df2.to_csv(file_name, index=False, encoding='utf_8_sig')
    #     print(f'文件已保存為: {file_name}')
    # print()

def group_travel_search_free():
    tour_datas = []
    # 設定webdriver
    browser = init_driver(maximized=True, headless=False)
    
    # 載入頁面
    browser.get('https://www.lifetour.com.tw/')
    
    # 等待搜尋條載入
    try:
        WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]')))
    except Exception as error:
        print(error)
        return
    
    # 點擊自由行按鈕
    click_element(browser, '//*[@id="searchbox"]/div[1]/a[2]')

    # 點擊出發地表單
    click_element(browser, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div')
    # 點擊不限地區出發
    departure_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li[1]')
    ActionChains(browser).click(departure_select_form).perform()
    # 點擊洲的列表選單
    click_element(browser, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[2]')
    continents_options = [continent.text for continent in browser.find_elements(By.XPATH, '//*[@id="popupMenuPanel"]/div[2]/div[2]/div/a')]
    print(continents_options)
    for continents_index, continents_option in enumerate(continents_options, start = 1):
        print(continents_option)
        # if continents_index != "1":
        all_handles = browser.window_handles
        first_window_handle = all_handles[0]
        browser.switch_to.window(first_window_handle)
        region_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[2]')
        ActionChains(browser).click(region_select_form).perform()
        continents_select_form = browser.find_element(By.XPATH, '//*[@id="popupMenuPanel"]/div[2]/div[2]/div/a[{}]'.format(continents_index))
        ActionChains(browser).click(continents_select_form).perform()
        # else:
        #     pass
        # 抓取內部表單內容
        region_options = [out_region.text for out_region in browser.find_elements(By.XPATH, '//div[@class="item-head"]/a') if out_region.text]
        for  region_index, region_option in enumerate(region_options, start = 1):
            print(region_option)
            all_handles = browser.window_handles
            first_window_handle = all_handles[0]
            browser.switch_to.window(first_window_handle)
            option_element = browser.find_element(By.XPATH, f'//div[@class="item-head"]/a[text()="{region_options[region_index-1]}"]')
            actions = ActionChains(browser)
            actions.move_to_element(option_element)
            browser.execute_script('arguments[0].click()',option_element)
        #--------------------------------------------------------------------
            # 點擊出發日期表單
            click_element(browser,'//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[1]')

            #抓取可選年份
            year_options = [year.get_attribute('value').split("/")[1] for year in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/div/select[2]/option')]
            #輸入出發日期
            date_input = formatted_datetime
            #檢查日期格式
            if re.compile('\d{4}/\d{2}/\d{2}').match(date_input) != None:
                #拆分日期
                year = date_input.split("/")[0]
                month = date_input.split("/")[1].lstrip('0')
                day = date_input.split("/")[2].lstrip('0')
                # #檢查年分是否可選
                if year in year_options:
                    #取得輸入年份選項位置並點擊
                    year_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇年份"]')
                    # 使用 ActionChains 模擬點擊年份下拉選單
                    actions = ActionChains(browser)
                    actions.move_to_element(year_list_locator).click().perform()
                    # 選擇年份
                    select = Select(year_list_locator)
                    select.select_by_visible_text(year)
                    #抓取可選月份
                    month_options = [month.get_attribute('value') for month in browser.find_elements(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]/option')]
                    # 檢查月份是否可選 
                    if month in [m.split("/")[0] for m in month_options]:
                        # 取得月份表單位置並點擊
                        month_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]')
                        ActionChains(browser).click(month_list_locator).perform()
                        # 選擇月份
                        select = Select(month_list_locator)
                        option_value = month + '/' + year
                        select.select_by_value(option_value)
                        try:
                            WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table')))
                        except Exception as error:
                            print(error)
                        #取得可選日
                        week_List = []
                        day_options = []
                        week_numbers = [week_numbers.text for week_numbers in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr')]
                        # print(week_numbers)
                        for i in range(len(week_numbers)+1):
                            day_option = [day.text for day in browser.find_elements(By.XPATH, '//div[@id="searchPanel"]//div[contains(@class,"datepick-month-row")]//table//tr[{}]/td'.format(i)) if day.text.strip()]
                            day_options.extend(day_option)
                        # print(day_options)
                        for i in range(len(week_numbers)):
                            week_options = [week.text for week in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td'.format(i+1))]
                            # print(week_options)
                            week_List.append(week_options)
                            # 檢查日期是否過期
                        if eval(day) >= current_datetime.day:
                            for i in range(len(week_List)):
                                for j in range(len(week_List[i])):
                                    if week_List[i][j] == day:
                                        # print(i, j)
                                        #檢查輸入日期選項位置並點擊
                                        click_element(browser, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td[{}]'.format(i+1,j+1))
    
                        else:
                            print("請選擇" + '(' + str(day_options)[current_datetime.day].replace('[', '').replace(']', '').replace("'", '').replace(',', ' ').lstrip().rstrip().replace('  ', ',') + ')' + ": ")
                    else:
                        print("請選擇" + str(month_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
                else:
                    print("請選擇" + str(year_options).replace('[', '(').replace(']', ')').replace("'", '') + ": ")
            else:
                print("格式錯誤!")
            # --------------------------------------------------------------------
            #關閉截止日表單
            close_deadline = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[3]/a[2]')
            ActionChains(browser).click(close_deadline).perform()
            # --------------------------------------------------------------------
            #點擊搜索按鈕
            click_element(browser, '//*[@id="btn_search_pc"]')
            
            #--------------------------------------------------------------------
            #轉移到新分頁
            window_handles = browser.window_handles
            browser.switch_to.window(window_handles[-1])
            
            #等待頁面跳轉
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SearchList"]')))
            except Exception as error:
                print(error)
            
            #畫面移到最底
            # 獲取頁面高度
            last_height = browser.execute_script("return document.body.scrollHeight")
            
            while True:
                # 滾動到底部
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # 等待頁面加載新內容
                time.sleep(1)
                
                # 計算新的頁面高度並和之前的高度對比
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            #抓所有行程網址
            tour_links = [tour_link.get_attribute("href") for tour_link in browser.find_elements(By.XPATH, '//div[contains(@class, "item-list")]/div/a')]
            print(f"有 {len(tour_links)} 筆區域行程網址")
            browser.close()
            #--------------------------------------------------------------------
            #--------------------------------------------------------------------
            #開連結網址
            datesList = []
            setnumList = []
            newurls = []
            tour_links_count = 0
            for links in tour_links:
                try:
                    browser.switch_to.window(first_window_handle)
                    browser.execute_script("window.open('" + links + "', '_blank');")
                    all_handles = browser.window_handles
                    new_window_handle = all_handles[-1]
                    browser.switch_to.window(new_window_handle)
                    time.sleep(0.5)
                    #往後點擊最多5個的月份，讓行程跑完
                    previous_month = ""
                    count = 0
                    while count < 5:
                        try:
                            # 抓取按鈕月份
                            current_month = browser.find_element(By.XPATH, '//*[@id="calendar"]/div[2]/div[1]/span').text
                            if current_month == previous_month:
                                break
                            previous_month = current_month
                            # 等待 "下個月" 按钮可
                            next_month = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="calendar"]/div[2]/a[2]')))
                            # 點擊 "下個月" 按钮
                            ActionChains(browser).move_to_element(next_month).click().perform()
                            time.sleep(0.2)
                            count += 1
                        except TimeoutException:
                            print("等待超時，停止迴圈")
                            break
                    if count == 5:
                        print("已經迴圈5次，停止迴圈")

                    # 抓有成團的id
                    group_id = links.split("/")[-1].split("#")[0]
                    
                    # 解析頁面內容
                    soup = bs(browser.page_source, 'html.parser')
                    
                    # 整理每個成團的網址
                    for li in soup.find_all('li', attrs={'data-mcode': group_id}):
                        if li.get('data-more') == "true":
                            pass
                        else:
                            datesList.append(li['data-date'])
                            setnum = li['data-scode']
                            setnumList.append(setnum)
                            newurls.append(links.split("#")[0] + "#" + setnum)
                    
                    tour_links_count += 1
                    print(f"已完成第{tour_links_count}筆資料")
                
                except Exception as error:
                    print(f"處理 {links} 時發生錯誤: {error}")
                    faillinks_list.append(links)
                    continue
                browser.close() 
            print(f"有 {len(newurls)} 筆行程")
            #--------------------------------------------------------------------
            #計數器
            tour_data_count = 0
            # 讀取每個網址進去
            for url in newurls:
                data = {}
                # all_handles = browser.window_handles
                # new_window_handle = all_handles[-1]
                browser.switch_to.window(first_window_handle)
                browser.execute_script("window.open('" + url + "', '_blank');")
                all_handles = browser.window_handles
                new_window_handle = all_handles[-1]
                try:
                    browser.switch_to.window(new_window_handle)
                    time.sleep(0.4)
                    WebDriverWait(browser, 15, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="calendar"]/div[3]/ul')))
                except TimeoutException:
                    print("網頁載入超時，跳過此頁")
                    browser.close()
                    continue
                #湯
                soup = bs(browser.page_source, 'html.parser')
                #抓取的內容
                data["company"] = "五福旅遊"
                data["region"] = region_option
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
                data["type"] = "自由行"#
                data["tourist_destination"] = soup.find("div", string="旅遊地點").find_next_sibling("h2").text.strip()
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
                # for key, value in list(data.items()):
                #     print(f"{key} : {value}")
                #放進tourDatas[]
                tour_datas.append(data)
                
                #印出當前完成第幾筆資料
                tour_data_count += 1
                print(f"有 {len(newurls)} 筆行程，已完成第{tour_data_count}筆資料")
                browser.close()
    
    return pd.DataFrame(tour_datas)
    # df3 = pd.DataFrame(tour_datas)
    #存到csv
    # file_name = "lifetour_free.csv"
    # if df3.empty:
    #     print(f"{file_name}沒有資料")
    # else:
    #     df3.to_csv(file_name, index=False, encoding='utf_8')
    #     print(f'文件已保存為: {file_name}')




def all_search():
    df1 = group_travel_search_in()
    df2 = group_travel_search_out()
    df3 = group_travel_search_free()
    result = pd.concat([df1, df2, df3], ignore_index=True)
    file_name = "lifetour_search.csv"
    if result.empty:
        print(f"{file_name}沒有資料")
    else:
        result.to_csv(file_name, index=False, encoding='utf_8')
        print(f'文件已保存為: {file_name}')

all_search()