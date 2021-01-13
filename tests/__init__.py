from random import randint, choice

def valid_num():
    num = choice([randint(7,30), randint(-30, -7)])
    return num

def invalid_num():
    num = choice([randint(0,6), randint(31, 300),
                        randint(-6,0), randint(-300, -31)])
    return(num)
