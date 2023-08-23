import matplotlib.pyplot as plt

def p(Xaxis, Yaxis, title=""): 
    plt.plot(Xaxis, Yaxis)
    plt.title(title)
    plt.ylabel('floor')
    plt.xlabel('time')
    plt.show()