from random import choice, randint

from scribble.predictions import predictions
from scribble.imager import drawing


def predictor(organ):
    if organ < 0:
        gender = 'BOY'
        pronoun = 'he'
        measure = 'LONG'
    else:
        gender = 'GIRL'
        pronoun = 'she'
        measure = 'DEEP'

    value = abs(organ)

    lovers = [('ASIAN', (randint(value // 3.2, value))),
              ('WHITE', (randint(value // 1.2, value // 0.8))),
              ('NIGER', (randint(value // 1.1, value // 0.7)))]

    person = choice(lovers)

    race, size = person[0], person[1]

    del (lovers[lovers.index(person)])

    if size < value // 1.3:
        dimension = 'SMALL'
    elif size > value // 0.7:
        dimension = 'BIG'
    else:
        dimension = 'MEDDLE'

    return (printer(lovers[0], lovers[1], gender, measure, race, dimension,
        organ, pronoun, size, value), drawing(lovers, person, gender, value))


def printer(lover1, lover2, gender, measure, race, dimension, organ, pronoun, size, value):
    return 'Tomorrow you HAVEN\'T a date with {0} {4} {1} {5} and {2} {4} {3} {5}.\nBut you meet {6} {4} with {7} genital.\nYour size is {8} {9} is {10}.\n{11}'.format(lover1[0], 
        lover1[1],lover2[0], lover2[1], gender, measure, race, 
        dimension, organ, pronoun, size, predictions(size, value, 
            gender))

