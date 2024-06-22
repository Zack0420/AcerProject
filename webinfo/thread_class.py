import threading
import pandas as pd
import auto_catch_travel_info, autoSearch_all0620, liontrip_def, globalcrawler, taiwancrawler

class Thread1(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)
        self.df = pd.DataFrame()

    
    def run(self):
        try:
            print("Thread 1 執行")
            self.df = auto_catch_travel_info.main()
        except Exception as e:
            print("Thread 1 失敗\n", e)
class Thread2(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)
        self.df = pd.DataFrame()

    
    def run(self):
        try:
            print("Thread 2 執行")
            self.df = autoSearch_all0620.all_search()
        except Exception as e:
            
            print("Thread 2 失敗\n", e)

class Thread3(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)
        self.df = pd.DataFrame()
    
    def run(self):
        try:
            print("Thread 3 執行")
            self.df = globalcrawler.main()
        except Exception as e:
            
            print("Thread 3 失敗\n", e)
    
class Thread4(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)
        self.df = pd.DataFrame()
    
    def run(self):
        try:
            print("Thread 4 執行")
            self.df = liontrip_def.main()
        except Exception as e:
            
            print("Thread 4 失敗\n", e)
class Thread5(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)
        self.df = pd.DataFrame()
    
    def run(self):
        try:
            print("Thread 5 執行")
            self.df = taiwancrawler.scrape_travel_data()
        except Exception as e:
            
            print("Thread 5 失敗\n", e)
    
thread1 = Thread1()
thread2 = Thread2()
thread3 = Thread3()
thread4 = Thread4()
thread5 = Thread5()
        

thread_list = [thread1, thread2, thread3, thread4, thread5]


df = pd.DataFrame()

for i in thread_list:
    i.start()
    
for i in thread_list:
    i.join()

for i in thread_list:
    
    df = pd.concat([df, i.df])
    
df.to_csv('travel_data.csv', encoding='UTF-8')
print("完成")