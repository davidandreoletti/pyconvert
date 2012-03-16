def enum(*sequential, **named):
    """
    Creates an "enum" type
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def escapeAllWith(aString, anEscapeString):
    """
    Escape all characters with the escape string.
    @param aString String to escape
    @param anEscapeString String to escape the first string with
    @return Escaped string
    """
    escapedString = list()
    for c in aString:
        escapedString.append(anEscapeString)
        escapedString.append(c)

    return ''.join(escapedString)

def escapePathForUnix(aString):
    """
    Escape all characters with the escape string.
    @param aString String to escape
    @param anEscapeString String to escape the first string with
    @return Escaped string
    """
    path = escapeAllWith(aString,"\\")
    return path

def escapePathForOSIndependentShell(aString):
    """
    Escape all characters with the escape string.
    @param aString String to escape
    @param anEscapeString String to escape the first string with
    @return Escaped string
    """
    return escapePathForUnix(aString)
    
    
    
    

