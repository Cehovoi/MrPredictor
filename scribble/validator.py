def validator(name, size, comment=None):
    try:
        size = int(size)
    except ValueError:
        comment ='%s that\'s probably not what you meant. Only numbers. Positive if you have a dick, negative if you have vagina!' % size
    
    else:
        if (len(name)>30 or len(name)<2 or 
                not( all(i.isalpha() or i.isspace() for i in name))):
            comment = 'No digits, no long story. The name field must be at least 2 letters long and no more than 20 letters'

        if abs(size) > 30:
            comment = ('Don\'t flatter yourself %s. You not a horse, horse can`t input the data!'% name)
        
        if abs(size) < 7:
            comment = ('Well %s, this test is for adults only. Don\'t pretend to be a child.' % name)

    return(size, comment)
