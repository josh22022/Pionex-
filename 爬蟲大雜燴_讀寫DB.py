#引入套件
import pandas as pd
import requests , datetime , time
import pyodbc 
import talib
import matplotlib.pyplot as plt 

#Time setting	
start_time = "2017-10-01 00:00:00"  #設定時間
ts_start= int(time.mktime(datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timetuple()))  #將起始時間轉為timestamp
ts_end = int(time.time())  #將結束時間轉為timestamp

#Spider
dict = ['BTC','SOL','ETH','AXS','FLOW','MANA','ALICE','ENJ','SAND','APE','LPT','AR','HNT','GRT','ENS']

data = []  
df = pd.DataFrame(requests.get('https://www.pionex.com/kline/query_unite_candle_data?base=ENS&quote=USDT&market=pionex.v2&start='+str(ts_start)+'&end='+str(ts_end)+'&interval=1d&from=web').json())  
for k in range(len(df)):
    history_price = df.iloc[k,3]
    data.append([history_price['date'],
                history_price['high'],
                history_price['low'],
                history_price['open'],
                history_price['close'],
                history_price['volume']
                ])
data = pd.DataFrame(data)   #將DataFrame整理一下方便匯入SQL
data.columns=['date','high','low','open','close','volume']
data = data.round(2)

#The history data has been download.

#Connect to DB
server = 'LAPTOP-5QLDG1OL' #主機位址
database = 'Pionex'   #資料庫名稱
username = 'sa'    #使用者名稱
password = 'Josh1107.' #密碼
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


#Create Table
cursor.execute("CREATE TABLE [dbo].[BTC_1D](\
    [DATE] [varchar](50) NOT NULL,\
    [HIGH] [varchar](50) NOT NULL,\
    [LOW] [varchar](50) NOT NULL,\
    [OPEN] [varchar](50) NOT NULL,\
    [CLOSE] [varchar](50) NOT NULL,\
    [VOLUME] [varchar](50) NOT NULL,\
PRIMARY KEY CLUSTERED\
(\
    [DATE] ASC\
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]\
) ON [PRIMARY]")
csr = cnxn.cursor()  
csr.close()
del csr


#Insert Data
for i in range(len(data)):  #迴圈將所有資料轉成SQL語法
    try:
        cursor.execute("INSERT INTO ENS_1D VALUES ('"+str(data.loc[i][0])+"','"+str(data.loc[i][1])+"','"+str(data.loc[i][2])+"','"+str(data.loc[i][3])+"','"+str(data.loc[i][4])+"','"+str(data.loc[i][5])+"');")
    except:
        print(i)
        continue
print('Total :'+str(len(data)))
cnxn.commit()    #Commit
csr = cnxn.cursor()  
csr.close()
del csr


#Select Data
query ="SELECT * FROM BTC_1D"  #資料庫語法
df2 = pd.read_sql(query, cnxn) #將取出的資料轉為DataFrame

#Analysis
ADX = talib.ADX(df2.HIGH, df2.LOW, df2.CLOSE, timeperiod = 14)  #Average Directional Movement Index
RSI = talib.RSI(df2.CLOSE)  #Relative Strength Index

#Plot
fig = plt.figure()
plt.style.use("ggplot") 
plt.plot(ADX,c = "r")   #繪製ADX圖
plt.legend(labels=["ADX"], loc = 'best')  #下標籤
plt.xlabel("Day", fontweight = "bold")  #X軸名稱
fig.savefig('ADX.png')  #將圖檔存下

fig = plt.figure()  
plt.plot(RSI,c = "b")  #繪製RSI圖
plt.legend(labels=["RSI"], loc = 'best')  #下標籤
plt.xlabel("Day", fontweight = "bold")  #X軸名稱
fig.savefig('RSI.png')  #將圖檔存下
'''
