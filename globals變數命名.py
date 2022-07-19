ls = [ 'Apple','Banana','Cherry']
ls2 = [100,200,300]
for i in range(len(ls)):
    globals()[ls[i]+'_price'] =  ls2[i]
print(Apple_price,Banana_price,Cherry_price)
