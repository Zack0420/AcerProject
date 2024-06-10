# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 16:02:22 2024

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
import re

def clean_price(price_str):
    price = re.sub(r'[^\d]', '', price_str)
    return int(price) if price.isdigit() else 0

def taiwan_travel_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.settour.com.tw/")

    def scroll_down_and_wait():
        previous_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == previous_height:
                break
            previous_height = new_height
            WebDriverWait(driver, 10, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/section[2]/div[1]/article'))
            )

    try:
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
        time.sleep(2)
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
                    return {"date": ""}
                
                result = {}
                for date in dates:
                    day = date.find_element(By.CLASS_NAME, 'date-list-day').text.strip()
                    month = driver.find_element(By.XPATH, '//li[@class="active"]/a/div[@class="month"]').text.strip()
                    remarks = [remark.text.strip().replace('\n', ' ') for remark in date.find_elements(By.CLASS_NAME, 'date-list-remark') if remark.text.strip()]
                    price = next((remark for remark in remarks if '$' in remark), None)
                    if price:
                        price = clean_price(price)
                        if len(remarks) > 1:
                            result[f"{month}/{day}"] = {"價格": price, "備註": ', '.join(remarks[:-1])}
                        else:
                            result[f"{month}/{day}"] = {"價格": price}
                    else:
                        result[f"{month}/{day}"] = {"價格": 0}

                    ActionChains(driver).move_to_element(date).click(date).perform()
                    time.sleep(1)
                    
                    try:
                        WebDriverWait(driver, 10, 0.1).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@class="info-list-tag-type-item-text"]'))
                        )
                        info_element = driver.find_element(By.XPATH, '//div[@class="info-list-tag-type-item-text"]')
                        info_text = info_element.text
                        if "可售" in info_text:
                            available_seats = info_text.split("可售")[1].split()[0].strip()
                        else:
                            available_seats = ""
                    except:
                        available_seats = ""

                    result[f"{month}/{day}"]["可售"] = available_seats
                    
                return result
            except Exception as e:
                print(f"Error grabbing dates: {e}")
                return {"tour_schedual": ""}

        def click_through_calendar():
            results = {}
            while True:
                results.update(grab_dates())
                try:
                    next_button = driver.find_element(By.XPATH, '//div[@class="slider-arrow"]/div[@class="slider-arrow-right"]/i[@class="fa fa-chevron-right"]')
                    next_button.click()
                    time.sleep(1)
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
                tripDuration = soup.select_one('div.tag.black.lg i.fa-calendar').parent.text if soup.select_one('div.tag.black.lg i.fa-calendar') else "未提供旅遊天數或者一日遊"
                try:
                    tripDuration = int(tripDuration)
                except:
                    tripDuration = 1
                
                itineraryContainers = soup.select('div.stroke-item')
                itineraryDetails = {}

                for day, container in enumerate(itineraryContainers, start=1):
                    dayTitle = container.select_one('div.stroke-item-tit-day').text.strip()
                    details = [detail.strip() for detail in container.select_one('div.stroke-item-tit-stroke').text.split('，')]
                    
                    accommodation_info = []
                    accommodation_element = container.select_one('div.stroke-item-room')
                    if accommodation_element:
                        accommodation_info = [info.text.strip() for info in accommodation_element.select('span a')]
                        other_accommodation_info = accommodation_element.select_one('span').contents[-1].strip().split('或')
                        accommodation_info.extend(other_accommodation_info)
                    else:
                        accommodation_info = None

                    itineraryDetails[f"D{day} {dayTitle}"] = {"schedual": details, "posible_hotel": accommodation_info}

                for date, details in all_dates.items():
                    row = {
                        'travel_company': travelAgency,
                        'area': '台灣',
                        'title': travelName,
                        'date': date,
                        'departure_city': departureLocation,
                        'duration': tripDuration,
                        'price': details.get("價格", 0),
                        'remaining_quota': details.get("可售", ""),
                        'tour_schedual': itineraryDetails,
                        'url': travelPage
                    }

                    data.append(row)
                    
            except:
                print("error1")

            driver.close()
            print("關閉分頁")

            driver.switch_to.window(main_window)
            print("切換回搜尋結果頁面")
            
    finally:
        driver.quit()
        return data
        print("瀏覽器已關閉")

def global_travel_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.settour.com.tw/")

    regions = {
        "東北亞": '//*[@href="#1A_ALL"]',
        "東南亞": '//*[@href="#1C_ALL"]',
        "大陸港澳": '//*[@href="#1B_ALL"]',
        "美洲": '//*[@href="#1D_ALL"]',
        "歐洲": '//*[@href="#1E_ALL"]',
        "大洋洲": '//*[@href="#1F_ALL"]',
        "其他": '//*[@href="#1G_ALL"]',
    }

    def scroll_down_and_wait():
        previous_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == previous_height:
                break
            previous_height = new_height
            WebDriverWait(driver, 20, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//h4[@class="product-name"]/a/div')))

    time.sleep(5)
    data = []

    def grab_dates():
        try:
            WebDriverWait(driver, 20, 0.1).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "date") and contains(@class, "has-remark")]'))
            )
            dates = driver.find_elements(By.XPATH, '//div[contains(@class, "date") and contains(@class, "has-remark")]')
            if not dates:
                return {"行程日期和價格": "此行程暫時告一段落，敬請期待下一季行程"}
            
            result = {}
            for date in dates:
                day = date.find_element(By.XPATH, './/div[@class="date-list-day"]/div').text.strip()
                WebDriverWait(driver, 20, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, '//li[@class="active"]/a/div[@class="month"]'))
                )
                month = driver.find_element(By.XPATH, '//li[@class="active"]/a/div[@class="month"]').text.strip()
                
                remarks_elements = date.find_elements(By.XPATH, './/div[@class="date-list-remark"]/div')
                if len(remarks_elements) >= 2:
                    remark_1 = remarks_elements[1].text.strip().replace('\n', ' ').replace('$', '').replace(',', '')
                    result[f"{month}/{day}"] = {"價格": remark_1}
                else:
                    result[f"{month}/{day}"] = {"價格": ""}

                ActionChains(driver).move_to_element(date).click(date).perform()
                
                time.sleep(1)

                try:
                    WebDriverWait(driver, 10, 0.1).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="info-list-tag-type-item-text"]'))
                    )
                    info_element = driver.find_element(By.XPATH, '//div[@class="info-list-tag-type-item-text"]')
                    info_text = info_element.text
                    if "餘" in info_text and "席" in info_text:
                        remaining_quota = info_text.split("餘")[1].split("席")[0].strip()
                    else:
                        remaining_quota = ""
                except:
                    remaining_quota = ""

                result[f"{month}/{day}"]["餘額"] = remaining_quota

            return result
        except:
            print("error2")
            return {"tour_schedual": ""}

    def click_through_calendar():
        results = {}
        while True:
            results.update(grab_dates())
            try:
                next_button = driver.find_element(By.XPATH, '//div[@class="slider-arrow"]/div[@class="slider-arrow-right"]/i[@class="fa fa-chevron-right"]')
                next_button.click()
                time.sleep(3)
                WebDriverWait(driver, 20, 0.1).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "date") and contains(@class, "has-remark")]'))
                )
            except:
                break
        return results

    def process_region(region, xpath):
        try:
            print(f"嘗試點擊 {region}")
            element = WebDriverWait(driver, 20, 0.1).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView();", element)
            driver.execute_script("window.scrollBy(0, -150);")
            element.click()
            print(f"點擊 {region} 成功")
        except:
            print(f"點擊 {region} 時出錯: error3")

        try:
            search_button = WebDriverWait(driver, 20, 0.1).until(
                EC.element_to_be_clickable((By.ID, "searchBtn_1"))
            )
            search_button.click()
            print("點擊搜尋按鈕")
        except:
            print("error4")

        try:
            time.sleep(2)
            
            itinerary_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="sort pull-right hidden-sm hidden-xs"]/button[2]'))
            )
            if itinerary_button.is_displayed() and itinerary_button.is_enabled():
                driver.execute_script("arguments[0].click();", itinerary_button)
                print("使用JavaScript點擊行程按鈕")
            else:
                print("行程按鈕不可見或不可點擊")
        except:
            print("等待行程按鈕出現時出錯: error5")

        try:
            WebDriverWait(driver, 20, 0.1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div/div[2]/div/section[2]/div/div/article'))
            )
            print("搜尋結果出現")
        except:
            print("等待搜尋結果時出錯: error6")

        main_window = driver.current_window_handle

        try:
            scroll_down_and_wait()
            print("滾動頁面到最底")
        except:
            print("滾動頁面時出錯: error7")

        try:
            product_links = driver.find_elements(By.XPATH, '//h4[@class="product-name"]/a')
            print(f"找到 {len(product_links)} 行程結果")
        except:
            print("找尋行程結果時出錯: error8")

        for link in product_links:

            try:
                time.sleep(5)

                WebDriverWait(driver, 20, 0.1).until(
                    EC.element_to_be_clickable(link)
                )
                ActionChains(driver).move_to_element(link).click(link).perform()
                print("點擊連結")

                time.sleep(5)

                WebDriverWait(driver, 20, 0.1).until(EC.number_of_windows_to_be(2))
                new_window = [window for window in driver.window_handles if window != main_window][0]
                driver.switch_to.window(new_window)
                print("切換新分頁")

                time.sleep(5)

                WebDriverWait(driver, 20, 0.1).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "a.navbar-brand.logo img"))
                )
                print("新分頁載入完畢")

                time.sleep(3)
                all_dates = click_through_calendar()

                try:
                    travelAgency = WebDriverWait(driver, 20, 0.1).until(
                        EC.presence_of_element_located((By.XPATH, '//a[@class="navbar-brand logo"]/img'))
                    ).get_attribute('alt') if driver.find_elements(By.XPATH, '//a[@class="navbar-brand logo"]/img') else ""
                    
                    travelPage = driver.current_url

                    travelName = WebDriverWait(driver, 20, 0.1).until(
                        EC.presence_of_element_located((By.XPATH, '//h1[@class="product-in-tit"]'))
                    ).text if driver.find_elements(By.XPATH, '//h1[@class="product-in-tit"]') else ''
                    
                    departureLocation = WebDriverWait(driver, 20, 0.1).until(
                        EC.presence_of_element_located((By.XPATH, '//i[@class="fa fa-map-marker"]/parent::div'))
                    ).text if driver.find_elements(By.XPATH, '//i[@class="fa fa-map-marker"]/parent::div') else ''
                    
                    tourType = WebDriverWait(driver, 20, 0.1).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="tag black lg"]//i[@class="fa fa-calendar fa-fw"]/parent::div'))
                    ).text if driver.find_elements(By.XPATH, '//div[@class="tag black lg"]//i[@class="fa fa-calendar fa-fw"]/parent::div') else ""
                    duration_days = int(tourType.split('天')[0]) if '天' in tourType else 0
                    
                    itineraryContainers = WebDriverWait(driver, 20, 0.1).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="stroke-item"]'))
                    )

                    itineraryDetails = {}

                    day_counter = 1
                    for container in itineraryContainers:
                        try:
                            day = f"D{day_counter}"
                            day_counter += 1
                            schedual_elements = container.find_elements(By.XPATH, './/div[@class="stroke-item-tit-stroke"]')
                            schedual = [s.text for s in schedual_elements] if schedual_elements else []
                        except:
                            schedual = []
                        try:
                            accommodation_elements = container.find_elements(By.XPATH, './/div[@class="stroke-item-room"]/div')
                            possible_hotel = [a.text for a in accommodation_elements] if accommodation_elements else []
                        except:
                            possible_hotel = []

                        itineraryDetails[f"{day}"] = {'schedual': schedual, 'possible_hotel': possible_hotel}

                    for date, details in all_dates.items():
                        row = {
                            'travel_company': travelAgency,
                            'area': region,
                            'title': travelName,
                            'date': date,
                            'departure_city': departureLocation,
                            'duration': duration_days,
                            'price': int(details.get("價格", "")) if details.get("價格", "").isdigit() else "",
                            'remaining_quota': details.get("餘額", ""),
                            'tour_schedual': itineraryDetails,
                            'url': travelPage
                        }
                        data.append(row)
                        
                except:
                    print("抓取行程資訊時發生錯誤: error9")

                driver.close()
                print("關閉分頁")

                driver.switch_to.window(main_window)
                print("切換回搜尋結果頁面")
            except:
                print("處理行程連結時出錯: error10")

    for region, xpath in regions.items():
        WebDriverWait(driver, 20, 0.1).until(
            EC.element_to_be_clickable((By.ID, "selCountry_1"))
        ).click()
        
        process_region(region, xpath)

    driver.quit()

    for item in data:
        item['duration'] = int(item['duration'])

    return data

def main():
    taiwan_data = taiwan_travel_data()
    global_data = global_travel_data()

    all_data = taiwan_data + global_data

    df = pd.DataFrame(all_data)
    df.to_csv('travel_data.csv', index=False)

if __name__ == "__main__":
    main()
