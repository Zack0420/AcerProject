# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 22:35:47 2024

@author: USER
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


def scrape_travel_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--headless=new') 
    
    
    def clean_price(price_str):
        price = re.sub(r'[^\d]', '', price_str)
        return int(price) if price.isdigit() else 0

    def get_travel_links(driver):
        driver.get("https://www.settour.com.tw/")

        def scroll_down_and_wait():
            previous_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(4)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == previous_height:
                    break
                previous_height = new_height
                WebDriverWait(driver, 30, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/section[2]/div[1]/article'))
                )
            

        try:
            WebDriverWait(driver, 30, 0.1).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="searchBar_tour"]/ul/li[2]/a'))
            ).click()
            

            search_button = WebDriverWait(driver, 30, 0.1).until(
                EC.element_to_be_clickable((By.ID, "dtSearchBtn"))
            )
            ActionChains(driver).click(search_button).perform()
            

            WebDriverWait(driver, 30, 0.1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/section[2]/div[1]/article'))
            )
            

            scroll_down_and_wait()

            product_links = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/section[2]/div[1]/article/div/div/div[2]/h4/a')
            

            links = []
            main_window = driver.current_window_handle

            for link in product_links:
                try:
                    time.sleep(1)
                    WebDriverWait(driver, 30, 0.1).until(
                        EC.element_to_be_clickable(link)
                    )
                    ActionChains(driver).move_to_element(link).click(link).perform()
                    

                    WebDriverWait(driver, 30, 0.1).until(EC.number_of_windows_to_be(2))
                    new_window = [window for window in driver.window_handles if window != main_window][0]
                    driver.switch_to.window(new_window)
                    

                    WebDriverWait(driver, 30, 0.1).until(
                        EC.visibility_of_element_located((By.XPATH, '//a[@class="navbar-brand logo"]/img'))
                    )

                    travel_page_url = driver.current_url
                    if "https://tour.settour.com.tw/500" in travel_page_url:
                        driver.close()
                        driver.switch_to.window(main_window)
                        continue

                    links.append(travel_page_url)
                    

                    driver.close()
                    driver.switch_to.window(main_window)
                    
                except:
                    
                    driver.switch_to.window(main_window)
        finally:
            driver.quit()
            
        
        return links

    def get_travel_data(links):
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
                    day = date_text.split('(')[0]

                    day_parts = day.split('/')
                    month = day_parts[0].zfill(2)
                    day = day_parts[1].zfill(2)

                    formatted_day = f"{month}/{day}"
                    
                    full_date = f"{current_year}/{formatted_day}"
                    seats_text = seat.text.strip()
                    available_seats_match = re.search(r"可售\s*(\d+)", seats_text)
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
                    time.sleep(1)
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
                    continue

                all_dates = click_through_calendar()
                if not all_dates:
                    continue

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
                        accommodation_element = container.select_one('div.stroke-item-room')
                        if accommodation_element:
                            accommodation_info = [info.text.strip() for info in accommodation_element.select('span a')]
                            other_accommodation_info = accommodation_element.select_one('span').contents[-1].strip().split('或')
                            accommodation_info.extend(other_accommodation_info)
                        else:
                            accommodation_info = None
                    
                        itineraryDetails[f"D{day} {dayTitle}"] = {"schedual": details, "possible_hotel": accommodation_info}

                    for date, details in all_dates.items():
                        row = {
                            'travel_company': str(travelAgency),
                            'area': 'Taiwan',
                            'title': str(travelName),
                            'date': str(date),
                            'departure_city': str(departureLocation),
                            'duration': int(tripDuration),
                            'price': int(details.get("價格", 0)),
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

    # 獲取行程鏈接
    driver = webdriver.Chrome(options=options)
    travel_links = get_travel_links(driver)

    # 獲取行程數據
    travel_data = get_travel_data(travel_links)

    # 儲存數據到CSV文件
    df = pd.DataFrame(travel_data)
    # df.to_csv('travel_data.csv', index=False, encoding='utf-8-sig')
    # print("資料抓取完畢，並已儲存至 travel_data.csv 檔案")
    return df


