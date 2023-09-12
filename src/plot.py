import matplotlib.pyplot as plt
from Postgresql import PostgresConnection
from Intervals import MONTH
from time import time
import sys

def p(Xaxis, Yaxis, title="", ylabel='', xlabel=''): 
    plt.plot(Xaxis, Yaxis)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()

# Reads from postgresql
def getData(address: str, column: str, end, start):
    slug = PostgresConnection().readonly(f"select slug from collections where address='{address}'")[0][0]
    

    response = PostgresConnection().readonly(f"select {column}, last_updated from analytics where address='{address}' and last_updated>={end-start} and last_updated<={end}")
    y = list(map(lambda x: x[0], response))
    x = list(map(lambda x: x[1], response)) 
    return (x,y, slug,column)

if __name__ == "__main__":
    address = sys.argv[1]
    column = sys.argv[2]

    end = int(sys.argv[3]) if len(sys.argv) > 3 else time()
    start = int(sys.argv[4]) if len(sys.argv) > 4 else time() - MONTH

    r = getData(address, column, end, start)

    p(r[0], r[1], title=r[2],ylabel=r[3], xlabel='time')
    