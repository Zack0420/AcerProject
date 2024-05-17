# -*- coding: utf-8 -*-
"""
Created on Fri May 17 02:35:29 2024

@author: USER
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=options)
driver.get("https://www.settour.com.tw/")

def scroll_down_and_wait():
    previous_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(7)  # 添加一些延遲以確保頁面加載
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height
        # 使用 WebDriverWait 等待加載新內容
        WebDriverWait(driver, 10, 0.1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/section[2]/div[1]/article'))
        )

try:
    close_button = WebDriverWait(driver, 10, 0.1).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="belt-close-box"]'))
    )
    close_button.click()
    print("關閉廣告")

    WebDriverWait(driver, 10, 0.1).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="searchBar_tour"]/ul/li[2]/a'))
    ).click()
    print("點擊台灣")

    search_button = WebDriverWait(driver, 10, 0.1).until(
        EC.element_to_be_clickable((By.ID, "dtSearchBtn"))
    )
    ActionChains(driver).click(search_button).perform()
    print("點擊搜尋")

    WebDriverWait(driver, 10, 0.1).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/section[2]/div[1]/article'))
    )
    print("等待搜尋結果")

    main_window = driver.current_window_handle

    scroll_down_and_wait()
    print("滾動頁面到最底")

    product_links = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/section[2]/div[1]/article/div/div/div[2]/h4/a')
    print(f"找到 {len(product_links)} 行程結果")

    data = []

    def grab_dates():
        try:
            WebDriverWait(driver, 10, 0.1).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "date") and contains(@class, "has-remark")]'))
            )
            dates = driver.find_elements(By.XPATH, '//div[contains(@class, "date") and contains(@class, "has-remark")]')
            if not dates:
                return {"行程日期和價格": "此行程暫時告一段落，敬請期待下一季行程"}
            
            result = {}
            for date in dates:
                day = date.find_element(By.CLASS_NAME, 'date-list-day').text.strip()
                month = driver.find_element(By.XPATH, '//li[@class="active"]/a/div[@class="month"]').text.strip()
                remarks = [remark.text.strip().replace('\n', ' ') for remark in date.find_elements(By.CLASS_NAME, 'date-list-remark') if remark.text.strip()]
                price = next((remark for remark in remarks if '$' in remark), None)
                if price:
                    if len(remarks) > 1:
                        result[f"{month}/{day}"] = f"{price} ({', '.join(remarks[:-1])})"
                    else:
                        result[f"{month}/{day}"] = price
            return result
        except:
            return {"行程日期和價格": "此行程暫時告一段落，敬請期待下一季行程"}

    def click_through_calendar():
        results = {}
        while True:
            results.update(grab_dates())
            try:
                next_button = driver.find_element(By.XPATH, '//div[@class="slider-arrow"]/div[@class="slider-arrow-right"]/i[@class="fa fa-chevron-right"]')
                next_button.click()
                WebDriverWait(driver, 10, 0.1).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "date") and contains(@class, "has-remark")]'))
                )
            except:
                break
        return results

    for link in product_links:
        WebDriverWait(driver, 10, 0.1).until(
            EC.element_to_be_clickable(link)
        )
        ActionChains(driver).move_to_element(link).click(link).perform()
        print("點擊連結")

        WebDriverWait(driver, 10, 0.1).until(EC.number_of_windows_to_be(2))
        new_window = [window for window in driver.window_handles if window != main_window][0]
        driver.switch_to.window(new_window)
        print("切換新分頁")

        WebDriverWait(driver, 10, 0.1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.navbar-brand.logo img"))
        )
        print("新分頁載入完畢")

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        time.sleep(2)
        all_dates = click_through_calendar()

        try:
            travelAgency = soup.select_one("a.navbar-brand.logo img")["alt"]
            travelPage = driver.current_url

            travelName = soup.select_one('h1.product-in-tit').text if soup.select_one('h1.product-in-tit') else '無行程名稱'
            print(travelName)
            departureLocation = soup.select_one('i.fa-map-marker').parent.text if soup.select_one('i.fa-map-marker') else '無出發地點'
            tourType = soup.select_one('div.tag.black.lg i.fa-flag').parent.text if soup.select_one('div.tag.black.lg i.fa-flag') else "無跟團/自由行資訊"
            groupSize = soup.select_one('div.tag.black.lg i.fa-user').parent.text if soup.select_one('div.tag.black.lg i.fa-user') else "無成團人數資訊"
            tripDuration = soup.select_one('div.tag.black.lg i.fa-calendar').parent.text if soup.select_one('div.tag.black.lg i.fa-calendar') else "未提供旅遊天數或者一日遊"
            groupedNumber = soup.select_one('div.calendar-annotation-icon span.already').text if soup.select_one('div.calendar-annotation-icon span.already') else "未找到已成團/保證出團資訊"
            comingSoongroupe = soup.select_one('div.calendar-annotation-icon span.soon').text if soup.select_one('div.calendar-annotation-icon span.soon') else "未找到將成團資訊"
            transportMode = soup.select_one('div.tag.lg.gray-darker.display-block').text if soup.select_one('div.tag.lg.gray-darker.display-block') else "未提供交通方式"
            trainProject = soup.select_one('div.station-info').text if soup.select_one('div.station-info') else ""
            seatsInfo = soup.select_one('div.departure-date-list-item-remark').text if soup.select_one('div.departure-date-list-item-remark') else ""
            transport = f"{transportMode} {trainProject} {seatsInfo}".strip()

            itineraryContainers = soup.select('div.stroke-item-tit')
            itineraryDetails = []

            for day, container in enumerate(itineraryContainers, start=1):
                dayTitle = container.select_one('div.stroke-item-tit-day').text
                details = container.select_one('div.stroke-item-tit-stroke').text
                accommodation_info = container.select_one('div.stroke-item-room').text if container.select_one('div.stroke-item-room') else "未提供住宿"
                itineraryDetails.append(f"第{day}天: {dayTitle} - {details} - 住宿地點: {accommodation_info}")

            row = {
                '旅行社': travelAgency,
                '行程網頁': travelPage,
                '行程名稱': travelName,
                '哪裡出發': departureLocation,
                '跟團/自由行': tourType,
                '成團人數': groupSize,
                '旅程天數': tripDuration,
                '已成團/保證出團': groupedNumber,
                '將成團': comingSoongroupe,
                '交通方式': transport,
                '行程資訊': " | ".join(itineraryDetails),
                '行程日期和價格': all_dates
            }

            data.append(row)

        except Exception as e:
            print(f"抓取行程資訊時發生錯誤: {e}")
            driver.save_screenshot(f'screenshot_{time.time()}.png')  # 如果出錯才截圖

        driver.close()
        print("關閉分頁")

        driver.switch_to.window(main_window)
        print("切換回搜尋結果頁面")

    df = pd.DataFrame(data)
    df.to_csv('travel_data.csv', index=False, encoding='utf-8-sig')
    print("Data has been saved to travel_data.csv.")
        
finally:
    driver.quit()
    print("Browser has been closed.")
