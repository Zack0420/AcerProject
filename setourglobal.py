# -*- coding: utf-8 -*-
"""
Created on Mon May 27 01:17:54 2024

@author: USER
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

# 設置 Chrome 瀏覽器選項
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

# 初始化 Chrome 瀏覽器
driver = webdriver.Chrome(options=options)
driver.get("https://www.settour.com.tw/")

regions = {
    "東北亞": '//*[@href="#1A_ALL"]',
    "東南亞": '//*[@href="#1C_ALL"]',
    "港澳大陸": '//*[@href="#1B_ALL"]',
    "美洲": '//*[@href="#1D_ALL"]',
    "歐洲": '//*[@href="#1E_ALL"]',
    "紐澳關帛": '//*[@href="#1F_ALL"]',
    "南亞北亞中亞非": '//*[@href="#1G_ALL"]',
    "郵輪": '//*[@href="#1I_ALL"]'
}

def scroll_down_and_wait():
    previous_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)  # 添加一些延遲以確保頁面加載
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height
        WebDriverWait(driver, 20, 0.1).until(
            EC.presence_of_element_located((By.XPATH, '//h4[@class="product-name"]/a/div')))

# 等待頁面加載
time.sleep(5)  # 加長等待時間，確保所有內容加載完成

data = []

def grab_dates():
    try:
        # 等待日期元素出現
        WebDriverWait(driver, 20, 0.1).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "date") and contains(@class, "has-remark")]'))
        )
        dates = driver.find_elements(By.XPATH, '//div[contains(@class, "date") and contains(@class, "has-remark")]')
        if not dates:
            return {"行程日期和價格": "此行程暫時告一段落，敬請期待下一季行程"}
        
        result = {}
        for date in dates:
            day = date.find_element(By.XPATH, './/div[@class="date-list-day"]/div').text.strip()
            
            # 等待月份元素出現
            WebDriverWait(driver, 20, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//li[@class="active"]/a/div[@class="month"]'))
            )
            month = driver.find_element(By.XPATH, '//li[@class="active"]/a/div[@class="month"]').text.strip()
            
            remarks_elements = date.find_elements(By.XPATH, './/div[@class="date-list-remark"]/div')
            if len(remarks_elements) >= 2:
                remark_0 = remarks_elements[0].text.strip().replace('\n', ' ')
                remark_1 = remarks_elements[1].text.strip().replace('\n', ' ')
                result[f"{month}/{day}"] = {"價格": remark_1, "備註": remark_0}
            else:
                result[f"{month}/{day}"] = {"價格": "無價格資訊", "備註": "無備註"}
        return result
    except Exception as e:
        print(f"抓取日期和價格時發生錯誤: {e}")
        return {"行程日期和價格": "此行程暫時告一段落，敬請期待下一季行程"}

def click_through_calendar():
    results = {}
    while True:
        results.update(grab_dates())
        try:
            next_button = driver.find_element(By.XPATH, '//div[@class="slider-arrow"]/div[@class="slider-arrow-right"]/i[@class="fa fa-chevron-right"]')
            next_button.click()
            time.sleep(3)  # 等待新頁面內容加載
            WebDriverWait(driver, 20, 0.1).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "date") and contains(@class, "has-remark")]'))
            )
        except:
            break
    return results

def grab_flight_info():
    flight_info_list = []
    flight_info_items = driver.find_elements(By.XPATH, '//div[@class="slider-flight-info-item"]')
    
    for item in flight_info_items:
        flight_lists = item.find_elements(By.XPATH, './/div[@class="slider-flight-info-list"]')
        
        for flight in flight_lists:
            flight_info = {}
            
            try:
                tag = flight.find_element(By.XPATH, './/div[contains(@class, "tag") and contains(@class, "lg") and (contains(@class, "solid blue") or contains(@class, "gray-darker"))]').text
                flight_info['去回程'] = tag
            except:
                flight_info['去回程'] = ''
            
            try:
                airports = flight.find_element(By.XPATH, './/div[@class="a-to-b-tit"]').text
                flight_info['班機'] = airports
            except:
                flight_info['班機'] = ''
            
            try:
                airline_info = flight.find_element(By.XPATH, './/div[@class="col-sm-2 col-xs-10"]').text
                flight_info['航班資訊'] = airline_info
            except:
                flight_info['航班資訊'] = ''
            
            try:
                date_time_info = flight.find_elements(By.XPATH, './/div[@class="station-info"]')
                dates_times = [dt.text for dt in date_time_info]
                flight_info['班機時間'] = dates_times
            except:
                flight_info['班機時間'] = []
            
            try:
                duration = flight.find_element(By.XPATH, './/div[@class="flight-duration-time"]').text
                flight_info['飛行時間'] = duration
            except:
                flight_info['飛行時間'] = ''
            
            flight_info_list.append(flight_info)
    if not flight_info_list:
        flight_info_list.append({"訊息": "未提供航班資訊，請聯絡旅行社"})
        
    return flight_info_list

def process_region(region, xpath):
    try:
        print(f"嘗試點擊 {region}")
        element = WebDriverWait(driver, 20, 0.1).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("window.scrollBy(0, -150);")  # 向上滾動以便看到元素
        element.click()
        print(f"點擊 {region} 成功")
    except Exception as e:
        print(f"點擊 {region} 時出錯: {e}")

    try:
        #print("等待搜尋按鈕可點擊")
        search_button = WebDriverWait(driver, 20, 0.1).until(
            EC.element_to_be_clickable((By.ID, "searchBtn_1"))
        )
        search_button.click()
        #print("點擊搜尋按鈕")
    except Exception as e:
        print(f"點擊搜尋按鈕時出錯: {e}")

    try:
        time.sleep(2)
        
        print("等待行程按鈕出現")
        itinerary_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="sort pull-right hidden-sm hidden-xs"]/button[2]'))
        )
        if itinerary_button.is_displayed() and itinerary_button.is_enabled():
            driver.execute_script("arguments[0].click();", itinerary_button)
            print("使用JavaScript點擊行程按鈕")
        else:
            print("行程按鈕不可見或不可點擊")
    except Exception as e:
        print(f"等待行程按鈕出現時出錯: {e}")

    try:
        #print("等待搜尋結果")
        WebDriverWait(driver, 20, 0.1).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div/div[2]/div/section[2]/div/div/article'))
        )
        #print("搜尋結果出現")
    except Exception as e:
        print(f"等待搜尋結果時出錯: {e}")

    main_window = driver.current_window_handle

    try:
        scroll_down_and_wait()
        #print("滾動頁面到最底")
    except Exception as e:
        print(f"滾動頁面時出錯: {e}")

    try:
        product_links = driver.find_elements(By.XPATH, '//h4[@class="product-name"]/a')
        print(f"找到 {len(product_links)} 行程結果")
    except Exception as e:
        print(f"找尋行程結果時出錯: {e}")

    for link in product_links:
        try:

            time.sleep(5)

            WebDriverWait(driver, 20, 0.1).until(
                EC.element_to_be_clickable(link)
            )
            ActionChains(driver).move_to_element(link).click(link).perform()
            #print("點擊連結")

            time.sleep(5)

            WebDriverWait(driver, 20, 0.1).until(EC.number_of_windows_to_be(2))
            new_window = [window for window in driver.window_handles if window != main_window][0]
            driver.switch_to.window(new_window)
            #print("切換新分頁")

            time.sleep(5)

            WebDriverWait(driver, 20, 0.1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "a.navbar-brand.logo img"))
            )
            #print("新分頁載入完畢")

            time.sleep(3)
            all_dates = click_through_calendar()

            try:
                travelAgency = WebDriverWait(driver, 20, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@class="navbar-brand logo"]/img'))
                ).get_attribute('alt')

                travelPage = driver.current_url

                travelName = WebDriverWait(driver, 20, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, '//h1[@class="product-in-tit"]'))
                ).text if driver.find_elements(By.XPATH, '//h1[@class="product-in-tit"]') else '無行程名稱'
                
                departureLocation = WebDriverWait(driver, 20, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, '//i[@class="fa fa-map-marker"]/parent::div'))
                ).text if driver.find_elements(By.XPATH, '//i[@class="fa fa-map-marker"]/parent::div') else '無出發地點'
                
                tourType = WebDriverWait(driver, 20, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="tag black lg"]//i[@class="fa fa-calendar fa-fw"]/parent::div'))
                ).text if driver.find_elements(By.XPATH, '//div[@class="tag black lg"]//i[@class="fa fa-calendar fa-fw"]/parent::div') else "無總天數資訊"
                #print(tourType)
                groupSize = WebDriverWait(driver, 20, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="tag black lg"]//i[@class="fa fa-user fa-fw"]/parent::div'))
                ).text if driver.find_elements(By.XPATH, '//div[@class="tag black lg"]//i[@class="fa fa-user fa-fw"]/parent::div') else "無成團人數資訊"
                #print(groupSize)
                
                flightinfo = grab_flight_info()

                itineraryContainers = WebDriverWait(driver, 20, 0.1).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="stroke-item"]'))
                )

                itineraryDetails = []

                for container in itineraryContainers:
                    try:
                        day = WebDriverWait(container, 20, 0.1).until(
                            EC.presence_of_element_located((By.XPATH, './/div[@class="stroke-item-tit-day"]'))
                        ).text.strip()
                    except:
                        day = '無天數資訊'
                    try:
                        details = WebDriverWait(container, 20, 0.1).until(
                            EC.presence_of_element_located((By.XPATH, './/div[@class="stroke-item-tit-stroke"]'))
                        ).text.strip()
                    except:
                        details = '無行程資訊'
                    try:
                        meals_elements = WebDriverWait(container, 20, 0.1).until(
                            EC.presence_of_all_elements_located((By.XPATH, './/div[@class="stroke-item-eat"]/ul/li'))
                        )
                        meals = ' | '.join([meal.text for meal in meals_elements])
                    except:
                        meals = '無餐點資訊'
                    try:
                        accommodation_elements = WebDriverWait(container, 20, 0.1).until(
                            EC.presence_of_all_elements_located((By.XPATH, './/div[@class="stroke-item-room"]/div'))
                        )
                        accommodation = ' | '.join([a.text for a in accommodation_elements])
                    except:
                        accommodation = '無住宿資訊'

                    itineraryDetails.append(f"{day}: {details} | 餐點: {meals} | 住宿: {accommodation}")

                combined_itinerary = " | ".join(itineraryDetails)

                for date, details in all_dates.items():
                    row = {
                        '區域': region,
                        '旅行社': travelAgency,
                        '行程網頁': travelPage,
                        '行程名稱': travelName,
                        '哪裡出發': departureLocation,
                        '行程總天數': tourType,
                        '成團人數': groupSize,
                        '預計航班': flightinfo,
                        '行程日期': date,
                        '價格': details["價格"],
                        '備註': details["備註"],
                        '行程資訊': combined_itinerary
                    }
                    data.append(row)

            except Exception as e:
                print(f"抓取行程資訊時發生錯誤: {e}")
                driver.save_screenshot(f'screenshot_{time.time()}.png')

            driver.close()
            #print("關閉分頁")

            driver.switch_to.window(main_window)
            #print("切換回搜尋結果頁面")
        except Exception as e:
            print(f"處理行程連結時出錯: {e}")

try:
    for region, xpath in regions.items():
        # 首先點擊目的地輸入框，展開下拉菜單
        #print("嘗試點擊目的地輸入框")
        WebDriverWait(driver, 20, 0.1).until(
            EC.element_to_be_clickable((By.ID, "selCountry_1"))
        ).click()
        #print("已點擊目的地輸入框")
        
        process_region(region, xpath)
        
        # 返回首頁
        driver.get("https://www.settour.com.tw/")
        print(f"已返回首頁，準備抓取下一個區域：{region}")


    df = pd.DataFrame(data)
    df.to_csv('travel_data.csv', index=False, encoding='utf-8-sig')
    print("Data has been saved to travel_data.csv.")

finally:
    driver.quit()
    print("Browser has been closed.")
