# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 18:26:12 2024

@author: USER
"""

import time
import re
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def clean_price(price_str):
    price = re.sub(r'[^\d]', '', price_str)
    return int(price) if price.isdigit() else None

def get_travel_links():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--headless=new')  
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.settour.com.tw/")
    home_url = driver.current_url

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
            WebDriverWait(driver, 30, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//h4[@class="product-name"]/a'))
            )

    def scroll_to_top():
        try:
            top_button = WebDriverWait(driver, 30, 0.1).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="top-btn animation-fadeInUp"]/a'))
            )
            top_button.click()
        except:
            pass
        
    all_links = []

    def process_region(region, xpath):
        try:
            element = WebDriverWait(driver, 30, 0.1).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView();", element)
            driver.execute_script("window.scrollBy(0, -150);")
            element.click()
        except:
            pass

        try:
            search_button = WebDriverWait(driver, 30, 0.1).until(
                EC.element_to_be_clickable((By.ID, "searchBtn_1"))
            )
            search_button.click()
        except:
            pass

        try:
            time.sleep(2)
            itinerary_button = WebDriverWait(driver, 30, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="sort pull-right hidden-sm hidden-xs"]/button[2]'))
            )
            if itinerary_button.is_displayed() and itinerary_button.is_enabled():
                driver.execute_script("arguments[0].click();", itinerary_button)
            else:
                pass
        except:
            pass

        try:
            WebDriverWait(driver, 30, 0.1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div/div[2]/div/section[2]/div/div/article'))
            )
        except:
            pass

        try:
            scroll_down_and_wait()
        except:
            pass

        try:
            scroll_to_top()
        except:
            pass

        main_window = driver.current_window_handle

        try:
            product_links = driver.find_elements(By.XPATH, '//h4[@class="product-name"]/a')
        except:
            pass

        for link in product_links:
            try:
                time.sleep(1)
                link.click()
                WebDriverWait(driver, 30, 0.1).until(EC.number_of_windows_to_be(2))
                new_window = [window for window in driver.window_handles if window != main_window][0]
                driver.switch_to.window(new_window)
                travel_page_url = driver.current_url
                if "https://tour.settour.com.tw/500" in travel_page_url:
                    driver.close()
                    driver.switch_to.window(main_window)
                    continue
                all_links.append(travel_page_url)
                driver.close()
                driver.switch_to.window(main_window)
            except:
                driver.switch_to.window(main_window)

    for region, xpath in regions.items():
        WebDriverWait(driver, 30, 0.1).until(
            EC.element_to_be_clickable((By.ID, "selCountry_1"))
        ).click()
        
        process_region(region, xpath)
        driver.get(home_url)

    driver.quit()
    return all_links

def get_travel_data(links):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    data = []

    def grab_dates():
        try:
            time.sleep(1)
            WebDriverWait(driver, 30, 0.1).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "departure-date-list-item-day")]/a'))
            )
            dates = driver.find_elements(By.XPATH, '//div[contains(@class, "departure-date-list-item-day")]/a')
            seats = driver.find_elements(By.XPATH, '//div[contains(@class, "departure-date-list-item-qty")]/strong')
            prices = driver.find_elements(By.XPATH, '//div[contains(@class, "departure-date-list-item-price")]/strong')
            if not dates or not seats or not prices:
                return {}

            result = {}
            current_year = time.strftime("%Y")
            for date, seat, price in zip(dates, seats, prices):
                date_text = date.text.strip()
                day = date_text.split('(')[0]  # 移除括號及其內的星期信息
                
                day_parts = day.split('/')
                month = day_parts[0].zfill(2)
                day = day_parts[1].zfill(2)
                
                formatted_day = f"{month}/{day}"
                
                full_date = f"{current_year}/{formatted_day}"
                seats_text = seat.text.strip()
                available_seats_match = re.search(r"餘(\d+)席", seats_text)
                if available_seats_match:
                    available_seats = available_seats_match.group(1)
                else:
                    available_seats = ""
                price_text = clean_price(price.text.strip())

                result[full_date] = {"可售": available_seats, "價格": price_text}
                
            return result
        except:
            return {}

    def click_through_calendar():
        results = {}
        while True:
            results.update(grab_dates())
            try:
                next_button = driver.find_element(By.XPATH, '//div[@class="slider-arrow"]/div[@class="slider-arrow-right"]/i[@class="fa fa-chevron-right"]')
                time.sleep(0.8)
                next_button.click()
                
                WebDriverWait(driver, 30, 0.1).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "departure-date-list-item-day")]/a'))
                )
            except:
                break
        return results

    try:
        for link in links:
            if "https://tour.settour.com.tw/500" in link:
                continue
            driver.get(link)
            
            time.sleep(2)
            
            WebDriverWait(driver, 30, 0.1).until(
                EC.visibility_of_element_located((By.XPATH, '//a[@class="navbar-brand logo"]/img'))
            )
            
            time.sleep(1)

            try:
                all_dates_button = WebDriverWait(driver, 30, 0.1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.order-btn.pull-right a'))
                )
                time.sleep(1)
                all_dates_button.click()
            except:
                continue  # 如果無法點擊按鈕，跳過當前鏈接，繼續下一個

            all_dates = click_through_calendar()
            if not all_dates:
                continue  # 如果沒有出發行程清單，跳過當前鏈接，繼續下一個

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            try:
                travelAgency = soup.select_one("a.navbar-brand.logo img")["alt"]
                travelPage = driver.current_url
                travelName = soup.select_one('h1.product-in-tit').text if soup.select_one('h1.product-in-tit') else '無行程名稱'
                departureLocation = soup.select_one('i.fa-map-marker').parent.text if soup.select_one('i.fa-map-marker') else '無出發地點'
                tripDurationElement = soup.select_one('div.tag.black.lg i.fa-calendar')
                if tripDurationElement:
                    tripDurationText = tripDurationElement.parent.text.strip()
                    tripDuration = int(re.search(r'\d+', tripDurationText).group())
                else:
                    tripDuration = 1

                itineraryContainers = soup.select('div.stroke-item')
                itineraryDetails = {}

                for day, container in enumerate(itineraryContainers, start=1):
                    dayTitle = container.select_one('div.stroke-item-tit-day').text.strip()
                    details = [detail.strip() for detail in container.select_one('div.stroke-item-tit-stroke').text.split('，')]
                
                    accommodation_info = []
                    accommodation_element = container.select_one('div.stroke-item-room div')
                    if accommodation_element:
                        accommodation_info = [info.text.strip() for info in accommodation_element.select('a')]
                        other_accommodation_info = accommodation_element.get_text(separator=" ", strip=True).split("或")[-1].strip()
                        accommodation_info.append(other_accommodation_info)
                    else:
                        accommodation_info = None
                
                    itineraryDetails[f"D{day} {dayTitle}"] = {"schedual": details, "possible_hotel": accommodation_info}

                for date, details in all_dates.items():
                    row = {
                        'travel_company': str(travelAgency),
                        'area': 'Global',
                        'title': str(travelName),
                        'date': str(date),
                        'departure_city': str(departureLocation),
                        'duration': int(tripDuration),
                        'price': details.get("價格"),
                        'remaining_quota': str(details.get("可售", "")),
                        'tour_schedule': itineraryDetails,
                        'url': str(travelPage)
                    }

                    data.append(row)
                    
            except:
                pass

    finally:
        driver.quit()
    
    return data

def main():
    # 首先獲取所有行程鏈接
    travel_links = get_travel_links()
    
    # 然後遍歷鏈接獲取行程數據
    global_data = get_travel_data(travel_links)
    
    df = pd.DataFrame(global_data)
    # df.to_csv('global_data.csv', encoding="utf-8-sig", index=False)
    
    # print("資料型態已轉換並生成CSV檔案。")
    return df