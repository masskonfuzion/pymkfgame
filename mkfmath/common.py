import math

EPSILON = 1e-5
DEGTORAD = math.pi / 180.0
RADTODEG = math.pi * 180.0

COSS = [ math.cos(th * DEGTORAD) for th in range(0, 360) ]  # Note that Python allows negative indexes, which happen to work flawlessly here. In other languages, you'll need to correct indiexes out of range of 0..360
SINN = [ math.sin(th * DEGTORAD) for th in range(0, 360) ]
TANN = [ math.tan(th * DEGTORAD) for th in range(0, 360) ]

def coss(deg):
    int_part = int(deg)
    dec_part = deg - int_part

    return COSS[int_part] + dec_part * (COSS[(int_part + 1) % 360] - COSS[int_part])

def sinn(deg):
    int_part = int(deg)
    dec_part = deg - int_part

    return SINN[int_part] + dec_part * (SINN[(int_part + 1) % 360] - SINN[int_part])


def tann(deg):
    int_part = int(deg)
    dec_part = deg - int_part

    return TANN[int_part] + dec_part * (TANN[(int_part + 1) % 360] - TANN[int_part])

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


