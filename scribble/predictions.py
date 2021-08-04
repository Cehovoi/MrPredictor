

def predictions(size, value, m):
    if size < 6:
        comment =  'We\'ve already called the police. Sex with children is illegal.'
    elif size < 12 and value < 12:  
        comment = 'Sex of two mosquito, fast realy fast... Hey! What,s that smell? Is it burnt rubber...?'
    elif size >= 22 and value >= 22 and (max(size, value) - min(size, value))< 7:
        comment = 'The marriage game of two elephants, not fast but with a squelch and pleasure.'
    elif size//1.2 <= value and value <= size * 1.2:
        comment = 'Perfect meddle class sex, without surprize, but your bodies made for each other. Congratilation.'
    elif value * 1.5 <= size:
        if m == 'BOY':
            comment = 'His thing was too big, discomfort and pain... But there is something to tell too female friends'
        else:
            comment = 'Her vagina is too deep for you... When you take off her pants, and say "Wow!" you heard a small echo.'
    elif  size <= value and value <= size * 1.4:
        if m == 'BOY':
            comment = 'Small penis was compensated huge intelligence, boring sex but exciting conversation.'
        else:
            comment = 'Perspective to destroy pussy don`t bother your girlfrend, you remained without sex, but you get nice blowjob!'
    elif size * 1.4 <= value:
        if m == 'BOY':
            comment = 'Tickling is funny but both of you couldnt to come. Unsuitable. It happens.'
        else:
            comment = 'The girl going to become a pornstar, and your big organ didnt scare her.'
    else:
        comment = 'Something went wrong, the monthlyes came suddenly or the dick is going down... No sex, no rock`n`roll only friendly hug. Maybe next time...'
    return comment

