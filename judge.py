def distinction(x, coordinates1, coordinates2):
    y=[]
    for i in range(len(x)):
        if coordinates1[x[i]][0] > coordinates2[x[i]][0]:
            y.append(x[i])

    return y
    