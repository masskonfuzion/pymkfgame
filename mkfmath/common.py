EPSILON = 1e-9

def isZero(num, threshold=EPSILON):
    """ Return true if a number is near 0

        NOTE: no error testing here.. Don't be an idiot
    """
    return float(num) < threshold

def floatEq(a, b, threshold=EPSILON):
    return abs(a - b) < threshold
