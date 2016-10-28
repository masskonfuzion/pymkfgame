import math

EPSILON = 1e-5
DEGTORAD = math.pi / 180.0
RADTODEG = math.pi * 180.0

COSS = [ math.cos(th * DEGTORAD) for th in range(0, 360) ]
SINN = [ math.sin(th * DEGTORAD) for th in range(0, 360) ]

def coss(deg):
    int_part = int(deg)
    dec_part = deg - int_part

    return COSS[int_part] + dec_part * (COSS[(int_part + 1) % 360] - COSS[int_part])

def sinn(deg):
    int_part = int(deg)
    dec_part = deg - int_part

    return SINN[int_part] + dec_part * (SINN[(int_part + 1) % 360] - SINN[int_part])

def isZero(num, threshold=EPSILON):
    """ Return true if a number is near 0

        NOTE: no error testing here.. Don't be an idiot
    """
    return float(num) < threshold

def floatEq(a, b, threshold=EPSILON):
    return abs(a - b) < threshold

def floatStr(n):
    if n < EPSILON:
        return str(0.0)
    else:
        return str(float(n))


