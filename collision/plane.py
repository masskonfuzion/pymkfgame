from pymkfgame.mkfmath import vector

class Plane(object):
    ''' A plane class in point-normal format
    '''
    def __init__(self, p=None, n=None):
        if p is None:
            self.p = vector.Vector()
        else:
            self.p = vector.Vector(p[0], p[1], p[2], p[3])  # Note that because p is a point, p[3] could be non-zero

        if n is None:
            self.n = vector.Vector()  # surface normal vector. Should always be unit length (i.e., normalized.. a normalized normal. Punny)
        else:
            self.n = vector.Vector(n[0], n[1], n[2], n[3])  # Note that for a true vector, n[3] should be 0


