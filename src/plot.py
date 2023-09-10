import matplotlib.pyplot as plt
from postgresconnection import PostgresConnection
from intervals import MONTH
import sys

def p(Xaxis, Yaxis, title="", ylabel='', xlabel=''): 
    plt.plot(Xaxis, Yaxis)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()

# Reads from postgresql
def getData(address: str, column: str, end: int, start=-1):
    if start == -1:
        start = end - MONTH
    response = PostgresConnection().readonly(f"select {column}, last_updated from analytics where address='{address}' and last_updated>={end-start} and last_updated<={end}")
    y = list(map(lambda x: x[0], response))
    x = list(map(lambda x: x[1], response)) 
    return (x,y)

if __name__ == "__main__":
    address = sys.argv[1]
    column = sys.argv[2]
    end = int(sys.argv[3])
    # start = sys.argv[4]

    response = getData(address, column, end)

    p(response[0], response[1])
    