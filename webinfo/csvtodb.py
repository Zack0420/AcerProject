import mariadb 
import numpy as np
import pandas as pd

conn = mariadb.connect(
    user="x2lyeo1kke5qulwf",
    password="oh7g4vofe610rn8a",
    host="dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    database="f992vvvy5adtt70y")
cur = conn.cursor() 

# user="root",
# password="root",
# host="localhost",
# database="mysite")

filename = 'settour.csv'

data = pd.read_csv(filename)
data['price'] = data['price'].copy().replace(np.nan, None)
data['duration'] = data['duration'].copy().replace(np.nan, None)

# for index, r in data.iterrows():
#     if index > 12000:
#         break
    
#     cur.execute("INSERT INTO Trip (travel_company, area, title, price, date, departure_city, duration, remaining_quota, tour_schedule, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (r["travel_company"],r["area"],r["title"],r["price"],r["date"],r["departure_city"],r["duration"],r["remaining_quota"], r['tour_schedule'], r['url'])) 
    
# conn.commit() 
# conn.close()


