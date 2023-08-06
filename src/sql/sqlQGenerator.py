from functools import reduce


rst = lambda a,b: a+str(b) +',' if type(b) == int else a + "'" + b + "'" + ','


def insert(table, *args):
    return f"insert into {table} values ({reduce(rst, args, '')[:-1]})"

