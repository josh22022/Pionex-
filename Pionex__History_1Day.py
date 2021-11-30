"""
Case:Pionex__History_1Day
Description:
    獲取起始時間至今每日的幣價，存為CSV，可透過EXCEL可進行分析。建議直接以Python執行。
How to use:
    第15行" "內控制起始時間 ex:"2021-11-01 00:00:00"
    第20行{ }內加入所需幣種，格式為 '數字(從1開始)':'幣種代號' 以英文逗號分隔。
    第34行( )內設定檔案名稱 ex:'history.csv'
Author: Josh Chiao
"""
import pandas as pd
import requests , datetime , time

#Time setting	
start_time = "2021-11-01 00:00:00"
ts_start= int(time.mktime(datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timetuple()))
ts_end = int(time.time())

#Currency
currency_dict = {'1':'MANA','2':'FLOW','3':'ENJ','4':'SAND','5':'ALICE','6':'AXS'}
data = []

#Main program
for i in range(1,len(currency_dict)+1):
    data.append([currency_dict[str(i)]])
    df = pd.DataFrame(requests.get('https://www.pionex.com/kline/query_unite_candle_data?base='+currency_dict[str(i)]+'&quote=USDT&market=pionex.v2&start='+str(ts_start)+'&end='+str(ts_end)+'&interval=1d&from=web').json())  
    j = (ts_end - ts_start)/(60*60*24)
    for k in range(0,int(j)+2):
        history_price = df.iloc[k,3]
        data[i-1].append(history_price['close'])
        
#Data Sorting
data = pd.DataFrame(data)
data.to_csv('history.csv')

print('The history data has been download.')
input('Press any key to finish.')
