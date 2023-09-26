
'''
x = [0,1,2,3,4,5,6,7,8,9]
y = [10,2,3,4,2,4,7,10,10,2]
'''

def inclination(x1, y1, x2, y2):
    a = (y1-y2)/(x1-x2)
    return a

def extremum(x, y):
    dif = 0
    maxl_x=[]
    minl_x=[]
    for i in range(len(y)):
        try:
            if(abs(y[i]-y[i+1]) > dif or abs(y[i+1]-y[i+2]) > dif):
                a1 = inclination(x[i], y[i], x[i+1], y[i+1])
                a2 = inclination(x[i+1], y[i+1], x[i+2], y[i+2])
                if a1*a2 < 0:
                    if a1>0:
                        # x[i]が極大値
                        maxl_x.append(x[i+1])
                    else:
                        # x[i]が極小値 
                        minl_x.append(x[i+1])
        except:
            continue

    return maxl_x, minl_x


