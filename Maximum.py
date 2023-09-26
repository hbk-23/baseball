def Max(y):
    max = 0
    for i in range(len(y)):
        if max < y[i]:
            max = i
    
    return max