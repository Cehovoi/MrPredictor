dots = '.' * 4 # dots field between organs, you can choice size from 3 to 6
var = 7 # width of organ an inverse relationship, test value from 3 to 10
length = 4 # length of | | organ an inverse relationship, test value from 2 to 16

def prepare_lovers(lovers, person, gender, organ):
    person = ('your', person[1])
    lovers += [person]
    lovers = [(item[0] + gender, item[1]) for item in lovers]
    lovers += [('YourStaff', organ)]
    return lovers

def prepare_fillers(gender, order, staff):
    fillers = []
    for item in order:
        sex = ['GIRL', 'BOY']
        if item == staff:
            sex = ['BOY', 'GIRL']
        if gender == sex[0]:
            value = {'arrow': '∨', 'bolls': '*', 'line': '*'}
        if gender == sex[1]:
            value = {'arrow': '^', 'bolls': '_', 'line': '|'}
        fillers.append(value)
    return fillers

def drawing(lovers, person, gender, organ):
    lovers = prepare_lovers(lovers, person, gender, organ)
    order = list(range(len(lovers)))
    organs = [lovers[i][1] for i in order]
    width = [i // var for i in organs]
    organs = [i // length + 1 for i in organs]
    staff = len(organs) -1
    organs[-1] = (max(organs) // length - organs[staff] // length) - 1 # inverse your stuff
    bottom = ''
    picture = []
    fillers = prepare_fillers(gender, order, staff) # list with dict - difference between user and prediction(gender)

    for i, e in enumerate(width):
        space = ''
        if e < 1:
            space += '.'
        bottom_staff = dots + space + ('(%s%s%s)%s' % (fillers[i]['bolls'],
                                                     fillers[i]['line'] * e,
                                                     fillers[i]['bolls'], dots[:1]))
        bottom = bottom_staff + bottom # bootom_staff still need

    inscription = len(bottom) * '.'
    order.reverse()  
    order = iter(order)
    
    for i, e in enumerate(bottom):
        if e == '(':
            inscription = inscription[:i-2] + lovers[next(order)][0] + inscription[i+7:]

    if len(inscription) < len(bottom):
        inscription = inscription + '.' * (len(bottom)-len(inscription))
    else:
        inscription = inscription[len(inscription) - len(bottom):]

    bottom = bottom[len(bottom_staff):]
    bottom = '.' * len(bottom_staff) + bottom
    picture.append(bottom)

    while max(organs)>0:
        body = ''
        for i, e in enumerate(organs):
            space = ''
            if width[i] < 1:
                    space = '.'
            if i == staff:
                if max(organs) == 1:
                    body = bottom_staff + body
                    continue
                else:
                    e = - e
            if e <= 0:
                body = dots + dots + (dots[:1] * (
                        width[i] - 1)) + dots[:6 - len(dots)] + body  # this string draw end field with dots
                                                                    # there is some cooficient - 6
            elif e == 1:
                body = dots + dots[:1] + space + (
                        '(%s)' % (fillers[i]['arrow'] * width[i])) + dots[:2] + body
            else:
                body = dots + dots[:1] + space + (
                        '|%s|%s' % (fillers[i]['arrow'] * width[i], dots[:2])) + body
        picture.append(body)

        organs = [i - 1 for i in organs]

    if gender == 'BOY': picture.reverse()

    picture += [inscription]

    return str(picture)

