from django.core.management.base import BaseCommand
from ...models import Trip
import pandas as pd
import time
import os
import glob
import numpy as np
from pathlib import Path

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parent.parent
        path = os.path.join(BASE_DIR,'commands/csv/*.csv')
        csv_files = [file for file in glob.glob(path)]
        combined = pd.DataFrame()
        values = {"price":"無資料","date":"無資料","duration":"無資料","remaining_quota":"無資料","departure_city":"無資料"}

        for f in csv_files:
            
            data =  pd.read_csv(f)
            data['price'] = data['price'].copy().replace(np.nan, None)
            data['duration'] = data['duration'].copy().replace(np.nan, None)
            combined = pd.concat([combined,data])
            combined.dropna(subset = ['title'], inplace=True)
            combined.fillna(value =values)
            

            for index, row in data.iterrows():

                if index % 10000 == 0:
                    print("休息中")
                    time.sleep(3610)

                if "更新時間" in str(row['departure_city']):
                    row['departure_city'] = "無資料"

        
                
                trip_instance = Trip(
                    travel_company=row['travel_company'],
                    area=row['area'],
                    title=row['title'],
                    price=row['price'],
                    date=row['date'],
                    departure_city=row["departure_city"],
                    duration=row['duration'],
                    remaining_quota=row['remaining_quota'],
                    tour_schedule=row['tour_schedule'],
                    url=row['url']
                )
                trip_instance.save()
            
            print("完成!")

