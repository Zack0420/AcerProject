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
        driver.set_window_size(1920, 1080)
        driver.set_window_position(0, 0)
        # 確保瀏覽器窗口大小確實設置為1920x1080
        driver.maximize_window()
        driver.set_window_size(1920, 1080)
        driver.execute_script("document.body.style.zoom='0.5'")
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
    zone_input = None
    out_region_input = None
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
    
    bound = input("國內、國外(輸入in或out): ") or "in"
    
    if bound == 'in':
        
        #點擊國內按鈕
        bound_in_button = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[3]/div[2]')
        ActionChains(browser).click(bound_in_button).perform()
        
        print("預設可報名可候補")
        # #選擇是否只顯示可報名
        # available_input = input("是否只顯示可報名選項(y/n)?") or "n"
        # if available_input == 'y':
        #     available_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[2]/div/div[1]')
        #     ActionChains(browser).click(available_locator).perform()
        # elif available_input == 'n':
        #     pass
        
        # else:
        #     print('選項不存在')
        
        # #選擇是否只顯示可候補
        # stand_input = input("是否只顯示可候補選項(y/n)?") or "n"
        # if stand_input == 'y':
        #     stand_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[2]/div/div[2]')
        #     ActionChains(browser).click(stand_locator).perform()
        # elif available_input == 'n':
        #     pass
        
        # else:
        #     print('選項不存在')
  
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
        departure_options = [city.text for city in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul')]
        
        #迴圈跑出發地
        for departure_index, departure_option in enumerate(departure_options, start=1):
            # 點擊出發地表單
            departure_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div')
            ActionChains(browser).click(departure_select_form).perform()
            # 選擇區域
            print(departure_option)
            departure_input = str(departure_index)
            departure_city_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li[{}]'.format(departure_input))
            departure_city_actions = ActionChains(browser)
            departure_city_actions.move_to_element(departure_city_locator)
            #點擊地區表單
            region_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[2]')
            ActionChains(browser).click(region_select_form).perform()
            #等待地區表單出現
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="popupMenuPanel"]/div[2]')))
            except Exception as error:
                print(error)
          
            # 抓取表單內容   //*[@id="search-tab-0"]/div[]/div[2]/a[]    ///*[@id="search-tab-0"]/div[3]/div[2]/a[2]
            region_options = [region.text for region in browser.find_elements(By.XPATH, '//*[@id="search-tab-0"]/div/div[1]')]
            # print(region_options)
            #點擊地區表單
            region_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[2]')
            ActionChains(browser).click(region_select_form).perform()
            try:
                WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="popupMenuPanel"]/div[2]')))
            except Exception as error:
                print(error)
            # region_city_locator = browser.find_element(By.XPATH, '//*[@id="search-tab-0"]/div[{}]/div[2]/a[1]'.format(departure_input))
            # region_city_actions = ActionChains(browser)
            # region_city_actions.move_to_element(region_city_locator)
            zone_options = [zone.text for zone in browser.find_elements(By.XPATH, '//*[@id="search-tab-0"]/div[{}]/div[2]/a'.format(departure_input))]

            # 依輸入點選出發地
            destination_locator = browser.find_element(By.XPATH, '//*[@id="search-tab-0"]/div[{}]/div[2]/a[1]'.format(departure_input))
            ActionChains(browser).click(destination_locator).perform()
            input()
        input()
            # # 等待出發地表單出現
            # try:
            #     WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul')))
            # except Exception as error:
            #     print(error)
            #     browser.close()
            #     browser.quit()

       
        #輸入出發地
        # print("請選擇以下出發地: ")
        # for index, options in enumerate(departure_options):
        #     print(str(index+1)+" "+options)
        # departure_city_input = input("選擇出發地代號: ") or "1"
        # if eval(departure_city_input) > len(departure_options):
        #     print("選項不存在")
        # else:
        #     #依輸入點選出發地
        #     departure_city_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li[{}]'.format(departure_city_input))
        #     ActionChains(browser).click(departure_city_locator).perform()

    #     #--------------------------------------------------------------------
          
    #     #點擊地區表單
    #     region_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[2]')
    #     ActionChains(browser).click(region_select_form).perform()
    #     #等待地區表單出現
    #     try:
    #         WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="popupMenuPanel"]/div[2]')))
    #     except Exception as error:
    #         print(error)
      
    #     # 抓取表單內容   //*[@id="search-tab-0"]/div[]/div[2]/a[]    ///*[@id="search-tab-0"]/div[3]/div[2]/a[2]
    #     region_options = [region.text for region in browser.find_elements(By.XPATH, '//*[@id="search-tab-0"]/div/div[1]')]
    #     print("請選擇以下區域: ")
    #     for index, options in enumerate(region_options):
    #         print(str(index+1)+" "+options)
    #     region_input = input("選擇區域代號: ") or "1"
        
    #     zone_options = [zone.text for zone in browser.find_elements(By.XPATH, '//*[@id="search-tab-0"]/div[{}]/div[2]/a'.format(region_input))]
    #     print("請選擇以下城市: ")
    #     for index, options in enumerate(zone_options):
    #         print(str(index+1)+" "+options)
    #     zone_input = input("選擇城市代號: ") or "1"
    #     # 依輸入點選出發地
    #     destination_locator = browser.find_element(By.XPATH, '//*[@id="search-tab-0"]/div[{}]/div[2]/a[{}]'.format(region_input,zone_input))
    #     ActionChains(browser).click(destination_locator).perform()
        
    #     #--------------------------------------------------------------------
        
    #     #點擊出發日期表單
    #     time_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[1]')
    #     ActionChains(browser).click(time_select_form).perform()
           
    #     #等待日期表單出現
    #     try:
    #         WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div')))
    #     except Exception as error:
    #         print(error)
         
    #     #抓取可選年份
    #     year_options = [year.get_attribute('value').split("/")[1] for year in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/div/select[2]/option')]
        
    #     #輸入出發日期
    #     date_input = input("輸入出發日期(yyyy/mm/dd): ") or "2024/05/16"

    #     #檢查日期格式
    #     if re.compile('\d{4}/\d{2}/\d{2}').match(date_input) != None:
        
    #         #拆分日期
    #         year = date_input.split("/")[0]
    #         month = date_input.split("/")[1].lstrip('0')
    #         day = date_input.split("/")[2].lstrip('0')
    #         # #檢查年分是否可選
    #         if year in year_options:
                
    #             #取得輸入年份選項位置並點擊
    #             year_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇年份"]')

    #             # 使用 ActionChains 模擬點擊年份下拉選單
    #             actions = ActionChains(browser)
    #             actions.move_to_element(year_list_locator).click().perform()
                
    #             # 選擇年份
    #             select = Select(year_list_locator)
    #             select.select_by_visible_text(year)
                
    #             #抓取可選月份
    #             month_options = [month.get_attribute('value') for month in browser.find_elements(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]/option')]
                
    #             # 檢查月份是否可選 
    #             if month in [m.split("/")[0] for m in month_options]:
    #                 # 取得月份表單位置並點擊
    #                 month_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]')
    #                 ActionChains(browser).click(month_list_locator).perform()
                
    #                 # 選擇月份
    #                 select = Select(month_list_locator)
    #                 option_value = month + '/' + year
    #                 select.select_by_value(option_value)
    #                 try:
    #                     WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table')))
    #                 except Exception as error:
    #                     print(error)

                    
    #                 #取得可選日
    #                 week_List = []
    #                 day_options = []

    #                 week_numbers = [week_numbers.text for week_numbers in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr')]
    #                 # print(week_numbers)
                    
    #                 for i in range(len(week_numbers)+1):
    #                     day_option = [day.text for day in browser.find_elements(By.XPATH, '//div[@id="searchPanel"]//div[contains(@class,"datepick-month-row")]//table//tr[{}]/td'.format(i)) if day.text.strip()]
    #                     day_options.extend(day_option)
    #                 # print(day_options)
                    
    #                 for i in range(len(week_numbers)):
    #                     week_options = [week.text for week in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td'.format(i+1))]
    #                     # print(week_options)
    #                     week_List.append(week_options)
                    
    #                     # 檢查日期是否過期
    #                 if eval(day) >= current_datetime.day:
                        
    #                     for i in range(len(week_List)):
    #                         for j in range(len(week_List[i])):
    #                             if week_List[i][j] == day:
    #                                 # print(i, j)
    #                                 #檢查輸入日期選項位置並點擊
    #                                 day_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td[{}]'.format(i+1,j+1))
    #                                 ActionChains(browser).click(day_locator).perform()#//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[5]/td[2]
                    
    #                 else:
                        
    #                     print("請選擇" + '(' + str(day_options)[current_datetime.day].replace('[', '').replace(']', '').replace("'", '').replace(',', ' ').lstrip().rstrip().replace('  ', ',') + ')' + ": ")
            

    #     else:
            
    #         print("格式錯誤!")
    #     '''
    #         截止日預設6個月，先不變更
    #     '''
        
    #     #--------------------------------------------------------------------

    #     #關閉截止日表單
    #     close_deadline = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[3]/a[2]')
    #     ActionChains(browser).click(close_deadline).perform()
        
    #     #點擊搜索按鈕
    #     # browser.find_element(By.XPATH, '//*[@id="btn_search_pc"]').click()
    #     search_button = browser.find_element(By.XPATH, '//*[@id="btn_search_pc"]')

    #     # 使用 execute_script 模擬點擊按鈕
    #     browser.execute_script("arguments[0].click();", search_button)
        
    #     #--------------------------------------------------------------------
        
    #     #轉移到新分頁
    #     window_handles = browser.window_handles
    #     browser.switch_to.window(window_handles[-1])
        
    #     #等待頁面跳轉
    #     try:
    #         WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SearchList"]')))
    #     except Exception as error:
    #         print(error)
        
    #     # browser.execute_script("document.body.style.zoom='0.5'")
    #     #畫面移到最底
    #     browser.find_element(By.TAG_NAME,'body').send_keys(Keys.END)

    #     #等待2秒
    #     time.sleep(5)
    #     #抓所有行程網址
    #     tour_links = [tour_link.get_attribute("href") for tour_link in browser.find_elements(By.XPATH, '//div[contains(@class, "item-list")]/div/a')]

    #     # print(tour_links[:2])
    #     print(f"有 {len(tour_links)} 筆區域行程網址")
    #     # print("所有區域行程網址獲取成功!")
    #     input("回車執行")
    #     #--------------------------------------------------------------------
    #     #開連結網址
    #     tour_datas = []
    #     datesList = []
    #     setnumList = []
    #     newurls = []
    #     tour_links_count = 0
        
    #     for links in tour_links:
    #         try:
    #             browser.get(links)
    #             browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
    #             time.sleep(0.5)
                
    #             # 切換到列表
    #             try:
    #                 day_locator = browser.find_element(By.XPATH, '//*[@id="listType"]')
    #                 ActionChains(browser).click(day_locator).perform()
    #             except Exception as error:
    #                 print(f"切換列表失敗: {error}")
    #                 continue
                
    #             try:
    #                 WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/main')))
    #             except Exception as error:
    #                 print(f"等待元素失敗: {error}")
    #                 continue
                
    #             # 抓有成團的id
    #             group_id = links.split("/")[-1].split("#")[0]
                
    #             # 解析頁面內容
    #             soup = bs(browser.page_source, 'html.parser')
                
    #             # 整理每個成團的網址
    #             for li in soup.find_all('li', attrs={'data-mcode': group_id}):
    #                 if li.get('data-more') == "true":
    #                     pass
    #                 else:
    #                     datesList.append(li['data-date'])
    #                     setnum = li['data-scode']
    #                     setnumList.append(setnum)
    #                     newurls.append(links.split("#")[0] + "#" + setnum)
                
    #             tour_links_count += 1
    #             print(f"已完成第{tour_links_count}筆資料")
            
    #         except Exception as error:
    #             print(f"處理 {links} 時發生錯誤: {error}")
    #             continue
        
    #     print(f"有 {len(newurls)} 筆行程")
    #     input("回車執行")

        
    #     #--------------------------------------------------------------------
    #     #計數器
    #     tour_data_count = 0
    #     # 讀取每個網址進去
    #     for url in newurls:
    #         data = {}
    #         browser.get(url)
            
    #         browser.find_element(By.TAG_NAME,'body').send_keys(Keys.SPACE)
    #         try:
    #             WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="calendar"]/div[3]/ul')))
    #         except Exception as error:
    #             print(error)
    #         time.sleep(0.2)
    #         #湯
    #         soup = bs(browser.page_source, 'html.parser')
            
    #         #抓取的內容
    #         data["旅遊公司名稱"] = "五福旅遊"
    #         data["標題"] = soup.select_one("div.prod-name").text.strip()
    #         data["出發日期"] = soup.find("div", text="出發日期").find_next_sibling("div").text.strip()
    #         data["旅程天數"] = soup.find("div", text="旅遊天數").find_next_sibling("div").text.strip()
    #         try:
    #             data["出發城市"] = soup.find("div", text="出發機場").find_next_sibling("div").text.strip()
    #         except:
    #             pass
    #         price = soup.select_one("div.price-bar")
    #         for div in price.find_all("div")[1:2]:
    #             data["價錢"] = div.text

    #         data["旅遊地點"] = soup.find("div", text="旅遊地點").find_next_sibling("h2").text.strip()
           
    #         statusList = soup.find("ul", class_="wrap-status")
    #         for li in statusList.find_all("li"):
    #             try:
    #                 key = li.find("span").text
    #                 value = li.find("div").text
    #                 data[key] = value
    #             except:
    #                 pass
            
    #         schedule = soup.find("section", id="schedule").text.strip()
    #         daily_schedules = schedule.split("DAY")
        
    #         for index, daily_schedule in enumerate(daily_schedules[1:]):
    #             data["每日行程DAY" + str(index + 1)] = daily_schedule.replace("每日行程","").strip()
            
    #         #顯示抓取的字典內容
    #         # for key, value in list(data.items()):
    #         #     print(f"{key} : {value}")
    #         #放進tourDatas[]
    #         tour_datas.append(data)
            
    #         #印出當前完成第幾筆資料
    #         tour_data_count += 1
    #         print(f"已完成第{tour_data_count}筆資料")
            
    #     #存到csv
    #     df = pd.DataFrame(tour_datas)
    #     # df.to_csv(f'travel_data_{out_region_options[out_region_input-1]}{zone_options[int(zone_input)-1]}.csv', index=False, encoding='utf_8_sig')
    #     departur_name = departure_options[int(departure_city_input)-1]
    #     file_name = f"travel_data_出發地{departur_name}-不限目的地.csv"
    #     df.to_csv(file_name, index=False, encoding='utf_8_sig')
    #     print(f'文件已保存為: {file_name}')

    # elif bound == 'out':
    #     #預設是國外不用點
    #     # #點擊國外按鈕
    #     # bound_in_button = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[3]/div[]')
    #     # ActionChains(browser).click(bound_in_button).perform()
        
        
    #     #選擇是否只顯示可報名
    #     available_input = input("是否只顯示可報名選項(y/n)?") or "n"
    #     if available_input == 'y':
    #         available_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[2]/div/div[1]')
    #         ActionChains(browser).click(available_locator).perform()
    #     elif available_input == 'n':
    #         pass
        
    #     else:
    #         print('選項不存在')
        
    #     #選擇是否只顯示可候補
    #     stand_input = input("是否只顯示可候補選項(y/n)?") or "n"
    #     if stand_input == 'y':
    #         stand_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[2]/div/div[2]')
    #         ActionChains(browser).click(stand_locator).perform()
    #     elif available_input == 'n':
    #         pass
        
    #     else:
    #         print('選項不存在')
  
    #     # --------------------------------------------------------------------
    #     # 點擊出發地表單
    #     departure_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div')
    #     ActionChains(browser).click(departure_select_form).perform()
       
    #     # 等待出發地表單出現
    #     try:
    #         WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul')))
    #     except Exception as error:
    #         print(error)
    #         browser.close()
    #         browser.quit()

    #     #抓取表單內容
    #     departure_options = [city.text for city in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li')]
        
    #     #輸入出發地
    #     print("請選擇以下出發地: ")
    #     for index, options in enumerate(departure_options):
    #         print(str(index+1)+" "+options)
    #     departure_city_input = input("選擇出發地代號: ") or "1"
    #     if eval(departure_city_input) > len(departure_options):
    #         print("選項不存在")
    #     else:
    #         #依輸入點選出發地
    #         departure_city_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li[{}]'.format(departure_city_input))
    #         ActionChains(browser).click(departure_city_locator).perform()

    #     #--------------------------------------------------------------------
          
    #     #點擊地區表單
    #     region_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[1]/div[2]')
    #     ActionChains(browser).click(region_select_form).perform()
    #     #等待地區表單出現
    #     try:
    #         WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="popupMenuPanel"]/div[2]')))
    #     except Exception as error:
    #         print(error)
      
    #     # 抓取表單內容   //*[@id="search-tab-0"]/div[]/div[2]/a[]    ///*[@id="search-tab-0"]/div[3]/div[2]/a[2]
    #     #點擊洲的列表選單
    #     continents_options = [continent.text for continent in browser.find_elements(By.XPATH, '//*[@id="popupMenuPanel"]/div[2]/div[2]/div/a')]
    #     print("請選擇以下區域: ")
    #     for index, options in enumerate(continents_options):
    #         print(str(index+1)+" "+options)
    #     continents_options_input = input("選擇區域代號: ") or "1"
    #     if continents_options_input != "1":
    #         continents_select_form = browser.find_element(By.XPATH, '//*[@id="popupMenuPanel"]/div[2]/div[2]/div/a[{}]'.format(continents_options_input))
    #         ActionChains(browser).click(continents_select_form).perform()
    #     else:
    #         pass
        
    #     #點擊下面的選單
    #     out_region_options = [out_region.text for out_region in browser.find_elements(By.XPATH, '//div[@class="item-head"]/a') if out_region.text]
    #     print("請選擇以下區域: ")
    #     out_region_options_list = []
    #     for index, option in enumerate(out_region_options):
    #         print(f"{index+1}. {option}")
    #         out_region_options_list.append(option)
    #     out_region_input = input("選擇區域代號: ") or "1"
    #     option_element = browser.find_element(By.XPATH, f'//div[@class="item-head"]/a[text()="{out_region_options_list[int(out_region_input)-1]}"]')
    #     actions = ActionChains(browser)
    #     actions.move_to_element(option_element)
    #     try:
    #         element_to_wait = (By.XPATH, f'//div[@class="item-head"]/a[text()="{out_region_options_list[int(out_region_input)-1]}"]')
    #         WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located(element_to_wait))
    #     except Exception as error:
    #         print(error)
    #     browser.execute_script('arguments[0].click()',option_element)

        
    #     # #--------------------------------------------------------------------
        
    #     #點擊出發日期表單
    #     out_time_select_form = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[1]')
    #     ActionChains(browser).click(out_time_select_form).perform()
        
    #     #等待日期表單出現
    #     try:
    #         WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div')))
    #     except Exception as error:
    #         print(error)
         
    #     #抓取可選年份
    #     out_year_options = [out_year.get_attribute('value').split("/")[1] for out_year in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/div/select[2]/option')]
        
    #     #輸入出發日期
    #     out_date_input = input("輸入出發日期(yyyy/mm/dd): ") or "2024/05/16"

    #     #檢查日期格式
    #     if re.compile('\d{4}/\d{2}/\d{2}').match(out_date_input) != None:
        
    #         #拆分日期
    #         out_year = out_date_input.split("/")[0]
    #         out_month = out_date_input.split("/")[1].lstrip('0')
    #         out_day = out_date_input.split("/")[2].lstrip('0')
    #         # #檢查年分是否可選
    #         if out_year in out_year_options:
                
    #             #取得輸入年份選項位置並點擊
    #             out_year_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇年份"]')

    #             # 使用 ActionChains 模擬點擊年份下拉選單
    #             actions = ActionChains(browser)
    #             actions.move_to_element(out_year_list_locator).click().perform()
                
    #             # 選擇年份
    #             out_year_select = Select(out_year_list_locator)
    #             out_year_select.select_by_visible_text(out_year)
                
    #             #抓取可選月份
    #             out_month_options = [month.get_attribute('value') for month in browser.find_elements(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]/option')]
                
    #             # 檢查月份是否可選 
    #             if out_month in [m.split("/")[0] for m in out_month_options]:
    #                 # 取得月份表單位置並點擊
    #                 out_month_list_locator = browser.find_element(By.XPATH, '//select[@class="datepick-month-year" and @title="選擇月份"]')
    #                 ActionChains(browser).click(out_month_list_locator).perform()
                
    #                 # 選擇月份
    #                 out_month_select = Select(out_month_list_locator)
    #                 out_month_option_value = out_month + '/' + out_year
    #                 out_month_select.select_by_value(out_month_option_value)
    #                 try:
    #                     WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table')))
    #                 except Exception as error:
    #                     print(error)

                    
    #                 #取得可選日
    #                 out_week_List = []
    #                 out_day_options = []

    #                 out_week_numbers = [out_week_numbers.text for out_week_numbers in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr')]
    #                 # print(out_week_numbers)
                    
    #                 for i in range(len(out_week_numbers)+1):
    #                     out_day_option = [out_day.text for out_day in browser.find_elements(By.XPATH, '//div[@id="searchPanel"]//div[contains(@class,"datepick-month-row")]//table//tr[{}]/td'.format(i)) if out_day.text.strip()]
    #                     out_day_options.extend(out_day_option)
    #                 # print(out_day_options)
                    
    #                 for i in range(len(out_week_numbers)):
    #                     out_week_options = [out_week.text for out_week in browser.find_elements(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td'.format(i+1))]
    #                     # print(out_week_options)
    #                     out_week_List.append(out_week_options)
                    
    #                     # 檢查日期是否過期
    #                 if eval(out_day) >= current_datetime.day:
                        
    #                     for i in range(len(out_week_List)):
    #                         for j in range(len(out_week_List[i])):
    #                             if out_week_List[i][j] == out_day:
    #                                 # print(i, j)
    #                                 #檢查輸入日期選項位置並點擊
    #                                 out_day_locator = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[{}]/td[{}]'.format(i+1,j+1))
    #                                 ActionChains(browser).click(out_day_locator).perform()#//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[2]/div/table/tbody/tr[5]/td[2]
                    
    #                 else:
                        
    #                     print("請選擇" + '(' + str(out_day_options)[current_datetime.day].replace('[', '').replace(']', '').replace("'", '').replace(',', ' ').lstrip().rstrip().replace('  ', ',') + ')' + ": ")
            

    #     else:
            
    #         print("格式錯誤!")
    #     '''
    #         截止日預設6個月，先不變更
    #     '''
    #     #關閉截止日表單
    #     close_deadline = browser.find_element(By.XPATH, '//*[@id="searchPanel"]/div[4]/div[1]/div[2]/div[3]/div/div/div[3]/a[2]')
    #     ActionChains(browser).click(close_deadline).perform()
        
    #     #點擊搜索按鈕
    #     search_button = browser.find_element(By.XPATH, '//*[@id="btn_search_pc"]')

    #     # 使用 execute_script 模擬點擊按鈕
    #     browser.execute_script("arguments[0].click();", search_button)

    #     #--------------------------------------------------------------------
        
    #     #轉移到新分頁
    #     window_handles = browser.window_handles
    #     browser.switch_to.window(window_handles[-1])
        
    #     #等待頁面跳轉
    #     try:
    #         WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SearchList"]')))
    #     except Exception as error:
    #         print(error)
        
    #     # browser.execute_script("document.body.style.zoom='0.5'")
    #     #畫面移到最底
    #     browser.find_element(By.TAG_NAME,'body').send_keys(Keys.END)

    #     #等待2秒
    #     time.sleep(5)
    #     #抓所有行程網址
    #     tour_links = [tour_link.get_attribute("href") for tour_link in browser.find_elements(By.XPATH, '//div[contains(@class, "item-list")]/div/a')]

    #     # print(tour_links[:2])
    #     print(f"有 {len(tour_links)} 筆區域行程網址")
    #     # print("所有區域行程網址獲取成功!")
    #     input("回車執行")
    #     #--------------------------------------------------------------------
    #     #開連結網址
    #     tour_datas = []
    #     datesList = []
    #     setnumList = []
    #     newurls = []
    #     tour_links_count = 0
        
    #     for links in tour_links[:1]:
    #         try:
    #             browser.get(links)
    #             browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
    #             time.sleep(0.5)
                
    #             # 切換到列表
    #             try:
    #                 day_locator = browser.find_element(By.XPATH, '//*[@id="listType"]')
    #                 ActionChains(browser).click(day_locator).perform()
    #             except Exception as error:
    #                 print(f"切換列表失敗: {error}")
    #                 continue
                
    #             try:
    #                 WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/main')))
    #             except Exception as error:
    #                 print(f"等待元素失敗: {error}")
    #                 continue
                
    #             # 抓有成團的id
    #             group_id = links.split("/")[-1].split("#")[0]
                
    #             # 解析頁面內容
    #             soup = bs(browser.page_source, 'html.parser')
                
    #             # 整理每個成團的網址
    #             for li in soup.find_all('li', attrs={'data-mcode': group_id}):
    #                 if li.get('data-more') == "true":
    #                     pass
    #                 else:
    #                     datesList.append(li['data-date'])
    #                     setnum = li['data-scode']
    #                     setnumList.append(setnum)
    #                     newurls.append(links.split("#")[0] + "#" + setnum)
                
    #             tour_links_count += 1
    #             print(f"已完成第{tour_links_count}筆資料")
            
    #         except Exception as error:
    #             print(f"處理 {links} 時發生錯誤: {error}")
    #             continue
        
    #     print(f"有 {len(newurls)} 筆行程")
    #     input("回車執行")

        
    #     #--------------------------------------------------------------------
    #     #計數器
    #     tour_data_count = 0
    #     # 讀取每個網址進去
    #     for url in newurls:
    #         data = {}
    #         browser.get(url)
            
    #         browser.find_element(By.TAG_NAME,'body').send_keys(Keys.SPACE)
    #         try:
    #             WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="calendar"]/div[3]/ul')))
    #         except Exception as error:
    #             print(error)
    #         time.sleep(0.2)
    #         #湯
    #         soup = bs(browser.page_source, 'html.parser')
            
    #         #抓取的內容
    #         data["旅遊公司名稱"] = "五福旅遊"
    #         data["標題"] = soup.select_one("div.prod-name").text.strip()
    #         data["出發日期"] = soup.find("div", text="出發日期").find_next_sibling("div").text.strip()
    #         data["旅程天數"] = soup.find("div", text="旅遊天數").find_next_sibling("div").text.strip()
    #         try:
    #             data["出發城市"] = soup.find("div", text="出發機場").find_next_sibling("div").text.strip()
    #         except:
    #             pass
    #         price = soup.select_one("div.price-bar")
    #         for div in price.find_all("div")[1:2]:
    #             data["價錢"] = div.text

    #         data["旅遊地點"] = soup.find("div", text="旅遊地點").find_next_sibling("h2").text.strip()
           
    #         statusList = soup.find("ul", class_="wrap-status")
    #         for li in statusList.find_all("li"):
    #             try:
    #                 key = li.find("span").text
    #                 value = li.find("div").text
    #                 data[key] = value
    #             except:
    #                 pass
            
    #         schedule = soup.find("section", id="schedule").text.strip()
    #         daily_schedules = schedule.split("DAY")
        
    #         for index, daily_schedule in enumerate(daily_schedules[1:]):
    #             data["每日行程DAY" + str(index + 1)] = daily_schedule.replace("每日行程","").strip()
            
    #         #顯示抓取的字典內容
    #         # for key, value in list(data.items()):
    #         #     print(f"{key} : {value}")
    #         #放進tourDatas[]
    #         tour_datas.append(data)
            
    #         #印出當前完成第幾筆資料
    #         tour_data_count += 1
    #         print(f"已完成第{tour_data_count}筆資料")
            
    #     #存到csv
    #     df = pd.DataFrame(tour_datas)
    #     # df.to_csv(f'travel_data_{out_region_options[out_region_input-1]}{zone_options[int(zone_input)-1]}.csv', index=False, encoding='utf_8_sig')
    #     out_region_name = out_region_options[int(out_region_input)-1]
    #     file_name = f"travel_data_{out_region_name}.csv"
    #     df.to_csv(file_name, index=False, encoding='utf_8_sig')
    #     print(f'文件已保存為: {file_name}')

links = group_travel_search()

