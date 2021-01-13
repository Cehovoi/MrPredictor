dots = '.' * 4 # dots field between organs, you can choice size from 3 to 6
var = 7 # width of organ an inverse relationship, test value from 3 to 10
length = 4 # length of | | organ an inverse relationship, test value from 2 to 16


def drawing(lovers, person, gender):
    person = ('your', person[1])
    lovers.append(person)
    lovers = sorted(lovers, key=lambda x: x[1])
    order = [0,1,2]
    organs = [lovers[i][1] for i in order]
    
    bottom = ''
    picture = []
    
    if gender == 'GIRL': arrow = '∨'; bolls = '*'; line = '*'
    else: arrow = '^'; bolls= '_'; line = '|'

    for i in organs:
        space = ''
        if i < var: space += '.'
        bottom = dots + space + ('(%s%s%s)%s' % (bolls,line * (i//var),bolls,dots[:1])
                )+ bottom
    
    picture.append(bottom)
    bottom_length = len(bottom)

    inscription = bottom_length * '.'
    order.reverse()  
    order = iter(order)
    
    for i, e in enumerate(bottom):
        if e == '(':
            inscription = inscription[:i-2] + lovers[next(order
                )][0] + gender + inscription[i+7:]
    
    inscription_length = len(inscription)
    
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
    
    while max(organs)>0:
        body = ''
        for i,e in enumerate(organs):
            space = ''
            if width[i] < var:
                    space = '.'
            if e < 0:
                body =dots + dots + (dots[:1] * (
                    (width[i]//var)-1)) +dots[:6-len(dots)] + body # this string draw end field with dots
                                                                   # there is some cooficient - 6
            elif e == 1:
                
                body = dots + dots[:1]+ space + ('(%s)' % (arrow * 
                    (width[i]//var))) + dots[:2] + body
                organs[i] = 0
            
            else:
                body= (dots + dots[:1]+ space + ('|%s|%s'% (arrow * 
                    (width[i]//var), dots[:2]))) + body
        
        picture.append(body)
        
        organs = [i-length if i > length else i -(abs(i-1)
            ) for i in organs] 
    
    if gender == 'BOY': picture.reverse()
    
    picture += [inscription]
    
    return str(picture)

