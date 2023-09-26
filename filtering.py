# データフィルタリング
def fitering(x, y):
    filtered_x = []
    filtered_y = []
    for i in range(len(x)):
        if y[i] != 0:
            filtered_x.append(x[i])
            filtered_y.append(y[i])

    return filtered_x, filtered_y
