"""Takes arguments and generates sql queries."""

from functools import reduce
from typing import NewType

SqlArg = NewType('SqlArg', (str or int or str or float))
ListSqlArg = NewType('ListSqlArg', list[SqlArg])

rst = lambda a,b: a+str(b) +',' if (type(b) == int or type(b) == float) else a + "'" + b + "'" + ','

tupleToString = lambda prev, tuple: prev + tuple[0] + "=" + str(tuple[1]) + ',' if (type(tuple[1]) == int or type(tuple[1]) == float) else prev + tuple[0] + "=" + "'" + tuple[1] + "'" + ','

"""Insert query

insert into _ values (...)
"""
def insertG(table: str, args: list[SqlArg]):
    # print(args)
    return f"insert into {table} values ({reduce(rst, args, '')[:-1]})"

"""
Update query
update _ set _=_, _=_, ... where _ = _
"""
def updateG(table: str, condition: SqlArg, args: ListSqlArg):
    return f"update {table} set {reduce(tupleToString, args, '')[:-1]} where {tupleToString('', condition)[:-1]}"

def select(table: str, columns: list[str], where: ListSqlArg):
    pass
