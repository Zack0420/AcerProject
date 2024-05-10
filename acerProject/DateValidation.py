import re

def date_valid(date):
    
    pattern = r'(\d{4})/(\d{2})/(\d{2})'
    match = re.findall(pattern, date)
    
    if len(match) == 0:
        print("格式不正確")
        return False
    
    else:
        
        leap = False
        month31 = ['01','03','05','07','08','10','12']
        month30 = ['04','06','09','11']
        year = eval((match[0])[0])
        month = (match[0])[1]
        day = (match[0])[2]
        
        if year%4:
            pass
        else:
            if year%100:
                leap = True
            else:
                if year%400:
                    pass
                else:
                    leap = True
                    
                    
        if day[0] == "0" and month in (month31 + month30):
            
            return True
        
        else:
            
            if month in month31:
                
                if eval(day) > 31:
                    print("日期不正確")
                    return False
                
            elif month in month30:
                
                if eval(day) > 30:
                    print("日期不正確")
                    return False
            
            elif month == "02":
                if leap:
                    
                    if eval(day) > 29:
                        print("日期不正確")
                        return False
                    
                else:
                    
                    if eval(day) > 28:
                        print("日期不正確")
                        return False
            
            else:
                print("月份不正確")
                return False
            
            return True
        
                    