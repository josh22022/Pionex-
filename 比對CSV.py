import pandas as pd
df1 = pd.read_csv('aaa.csv')  #左邊
df2 = pd.read_csv('bbb.csv')  #右邊
result = df1.merge(df2, how='outer', indicator=True)  #outer找相異 inner找相同
result = result.loc[lambda x : x['_merge'] == 'right_only']  #右邊才有
result=pd.DataFrame(result)
#print(result)

for row in range(0,result.shape[0]):
    print(result.iat[row,0],result.iat[row,1])
#result.to_csv('right.csv')
