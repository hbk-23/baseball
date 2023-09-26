
def mark(x, y, plt, col, text):
    plt.scatter(x, y[x], color=col, marker='o')
    if text == 1:
        plt.text(x, y[x], 'frame' + str(x))

def markAR(x, y, plt, col, text):
    for i in range(len(x)):
        plt.scatter(x[i], y[x[i]], color=col, marker='o')
        if text == 1:
            plt.text(x[i], y[x], 'frame' + str(x[i]))

def line(x, plt, col, style, text):
    plt.axvline(x, color=col, linestyle=style)
    if text == 1:
        plt.text(x, 0, 'frame' + str(x))