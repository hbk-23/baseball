import Maximum

def PtoN(x, y):
    max = Maximum.Max(y)

    val = 0
    for i in range(max, len(x)):
        if y[i] > val and y[i+1] < val:
            return x[i+1]


