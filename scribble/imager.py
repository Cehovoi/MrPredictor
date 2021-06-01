dots = '.' * 4 # dots field between organs, you can choice size from 3 to 6
var = 7 # width of organ an inverse relationship, test value from 3 to 10
length = 4 # length of | | organ an inverse relationship, test value from 2 to 16

def prepare_lovers(lovers, person, gender, organ):
    person = ('your', person[1])
    lovers.append(person)
    lovers = [(item[0] + gender, item[1]) for item in lovers]
    lovers = sorted(lovers, key=lambda x: x[1])
    lovers = lovers + [('YourStaff', organ)]
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
    staff = len(organs) -1

    bottom = ''
    picture = []
    fillers = prepare_fillers(gender, order, staff) # list with dict - difference between user and prediction(gender)

    for i, e in enumerate(organs):
        space = ''
        if e < var:
            space += '.'
        bottom_staff = dots + space + ('(%s%s%s)%s' % (fillers[i]['bolls'],
                                                     fillers[i]['line'] * (e // var),
                                                     fillers[i]['bolls'], dots[:1]))
        bottom = bottom_staff + bottom # bootom_staff still need

    bottom_length = len(bottom)
    inscription = bottom_length * '.'
    inscription_length = len(inscription)
    order.reverse()  
    order = iter(order)
    
    for i, e in enumerate(bottom):
        if e == '(':
            inscription = inscription[:i-2] + lovers[next(order
                )][0] + inscription[i+7:]
        if i == staff:
            bottom = bottom[len(bottom_staff):]
            bottom = '.' * len(bottom_staff) + bottom

    picture.append(bottom)

    if bottom_length < inscription_length:
        difference  = inscription_length - bottom_length
        if difference <= 2:
            inscription = inscription[difference:]
        else: 
            iscription = inscription[2:]
            inscription.replace('.', '', difference-2)  
    
    if bottom_length > inscription_length:
        inscription += dots[:(bottom_length - inscription_length)]

    width = organs
    step = max(organs)//length - organs[staff]//length
    while max(organs)>0:
        body = ''
        for i, e in enumerate(organs):
            space = ''
            if width[i] < var:
                    space = '.'
            if i == staff:
                if max(organs) == 0:
                    body = bottom_staff + body
                    continue
                else:
                    e = - step
            if e <= 0:
                body =dots + dots + (dots[:1] * (
                    (width[i]//var)-1)) +dots[:6-len(dots)] + body # this string draw end field with dots
                                                                   # there is some cooficient - 6
            elif e == 1:
                
                body = dots + dots[:1]+ space + ('(%s)' % (fillers[i]['arrow'] *
                    (width[i]//var))) + dots[:2] + body
                organs[i] = 0
            
            else:
                body= (dots + dots[:1]+ space + ('|%s|%s'% (fillers[i]['arrow'] *
                    (width[i]//var), dots[:2]))) + body
        
        picture.append(body)

        organs = [i-length if i > length else i -(abs(i-1)
            ) for i in organs]
        step -= 1
    if gender == 'BOY': picture.reverse()

    picture += [inscription]

    return str(picture)

