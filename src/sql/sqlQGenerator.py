"""Takes arguments and generates sql queries."""

from functools import reduce


rst = lambda a,b: a+str(b) +',' if (type(b) == int or type(b) == float) else a + "'" + b + "'" + ','

tupleToString = lambda prev, tuple: prev + tuple[0] + "=" + str(tuple[1]) + ',' if (type(tuple[1]) == int or type(tuple[1]) == float) else prev + tuple[0] + "=" + "'" + tuple[1] + "'" + ','

"""Insert query"""
def insertG(table, args):
    return f"insert into {table} values ({reduce(rst, args, '')[:-1]})"

"""
Update query

Args must be tuples (a,b)
"""
def updateG(table,condition, args):
    return f"update {table} set {reduce(tupleToString, args, '')[:-1]} where {tupleToString('', condition)[:-1]}"



