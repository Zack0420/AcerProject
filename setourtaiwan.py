# -*- coding: utf-8 -*-
"""
Created on Wed May 15 19:20:11 2024

@author: USER
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=options)
driver.get("https://www.settour.com.tw/")

# 等待網頁加載完畢
driver.implicitly_wait(10)  # 等待 10 秒

def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)  # 等待頁面加載

try:
    # 使用 XPath 找到廣告的關閉按鈕並點擊
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="belt-close-box"]'))
    )
    close_button.click()
    print("Closed the advertisement.")

    # 等待台灣標籤的元素被定位後點擊
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="searchBar_tour"]/ul/li[2]/a'))
    ).click()
    print("Clicked the Taiwan tab.")

    # 找到搜尋按鈕並用ActionChains點擊
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "dtSearchBtn"))
    )
    ActionChains(driver).click(search_button).perform()
    print("Clicked the search button.")

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/section[2]/div[1]/article'))
    )
    print("Search results are visible.")

    # 保存當前的瀏覽器窗口
    main_window = driver.current_window_handle

    # 滾動頁面直到所有結果都加載完成
    previous_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        scroll_down()
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height
    print("Scrolled through the search results.")

    # 獲取所有搜索結果的元素
    product_links = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/section[2]/div[1]/article/div/div/div[2]/h4/a')
    print(f"Found {len(product_links)} product links.")

    # 準備存儲資料的列表
    data = []

    for link in product_links:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(link)
        )
        # 使用 ActionChains 點擊連結
        ActionChains(driver).move_to_element(link).click(link).perform()
        print("Clicked a product link.")

        # 等待新窗口打開
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        new_window = [window for window in driver.window_handles if window != main_window][0]
        driver.switch_to.window(new_window)
        print("Switched to the new window.")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.navbar-brand.logo img"))
        )
        print("The new page has loaded.")

        try:
            travelAgency = driver.find_element(By.CSS_SELECTOR, "a.navbar-brand.logo img").get_attribute("alt")
            travelPage = driver.current_url

            # 抓取網頁行程名稱
            travelNames = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//h1[@class="product-in-tit"]'))
            )
            travelName = travelNames[0].text if travelNames else '無行程名稱'

            # 抓取出發地點
            departureLocations = driver.find_elements(By.XPATH, '//div[@class="tag black lg" and .//i[@class="fa fa-map-marker" and @aria-hidden="true"]]')
            departureLocation = departureLocations[0].text if departureLocations else '無出發地點'

            # 抓取旅程天數
            try:
                tripDuration = driver.find_element(By.XPATH, '//div[@class="tag black lg" and .//i[@class="fa fa-calendar fa-fw" and @aria-hidden="true"]]').text
            except:
                tripDuration = "未提供旅遊天數或者一日遊"

            # 抓取已成團的數目
            try:
                groupedNumber = driver.find_element(By.XPATH, '//div[@class="calendar-annotation-icon"]/span[@class="already"]').text
            except:
                groupedNumber = "未找到已成團/保證出團資訊"

            # 抓取將成團資訊
            try:
                comingSoongroupe = driver.find_element(By.XPATH, '//div[@class="calendar-annotation-icon"]/span[@class="soon"]').text
            except:
                comingSoongroupe = "未找到將成團資訊"

            # 抓取交通方式
            try:
                transportMode = driver.find_element(By.XPATH, '//div[@class="tag lg gray-darker display-block"]').text
                trainProject = driver.find_element(By.XPATH, '//div[@class="station-info"]').text
                seatsInfo = driver.find_element(By.XPATH, '//div[@class="departure-date-list-item-remark"]').text
                transport = f"{transportMode} {trainProject} {seatsInfo}"
            except:
                transport = "未提供交通方式"

            # 抓取行程資訊
            itineraryContainers = driver.find_elements(By.XPATH, '//div[@class="stroke-item-tit"]')
            itineraryDetails = []

            for day, container in enumerate(itineraryContainers, start=1):
                # 使用相對XPath找到每個容器內的元素
                dayTitle = container.find_element(By.XPATH, './/div[@class="stroke-item-tit-day"]').text
                details = container.find_element(By.XPATH, './/div[@class="stroke-item-tit-stroke"]').text

                try:
                    accommodation_info = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, './/div[@class="stroke-item-room"]'))
                    ).text
                except:
                    accommodation_info = "未提供住宿"

                itineraryDetails.append(f"第{day}天: {dayTitle} - {details} - 住宿地點: {accommodation_info}")

            # 將行程資訊存入字典
            row = {
                '旅行社': travelAgency,
                '行程網頁': travelPage,
                '行程名稱': travelName,
                '哪裡出發': departureLocation,
                '旅程天數': tripDuration,
                '已成團/保證出團': groupedNumber,
                '將成團': comingSoongroupe,
                '交通方式': transport,
                '行程資訊': " | ".join(itineraryDetails)
            }

            # 添加到資料列表
            data.append(row)

        except Exception as e:
            print(f"抓取行程資訊時發生錯誤: {e}")

        # 關閉新窗口
        driver.close()
        print("Closed the new window.")

        # 切換回原始的搜尋結果頁面
        driver.switch_to.window(main_window)
        print("Switched back to the main window.")

    # 使用 pandas 將資料儲存為 CSV 檔案
    df = pd.DataFrame(data)
    df.to_csv('travel_data.csv', index=False, encoding='utf-8-sig')
    print("Data has been saved to travel_data.csv.")
        
finally:
    # 確保在任何情況下都能關閉瀏覽器
    driver.quit()
    print("Browser has been closed.")
