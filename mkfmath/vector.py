"""
3D Vector math class

For the purpose of doing matrix math, these vectors will be treated as column vectors (see matrix class)
"""

import math

from pymkfgame.mkfmath import common

class Vector(object):
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        """ Initialize a 3D vector
            
            NOTE: Vectors have a homogeneous coordinate (w) of 0.0
            But, if we want to treat an instance of this Vector class as a point (e.g., to transform via
            translation matrices), set w = 1.0

            TODO: Error checks? (prevent developer from creating invalid vector/point, e.g. w = non 0.0 or 1.0)
        """

        self.v = [float(x), float(y), float(z), float(w)]

    def __str__(self):
        #return "[ {}, {}, {} ]".format( common.floatStr(self.v[0]), common.floatStr(self.v[1]), common.floatStr(self.v[2]) )
        return "[ {}, {}, {}, {} ]".format( self.v[0], self.v[1], self.v[2], self.v[3] )

    def __getitem__(self, item):
        """ Get component indexed by item #

            NOTE: no error checking because we're lazy. We'll let the list obj do its own error checking
        """
        return self.v[item]

    def __setitem__(self, item, value):
        """ Set component indexed by item #

            NOTE: no error checking because we're lazy. We'll let the list obj do its own error checking
        """
        self.v[item] = float(value)

    def __neg__(self):
        return Vector(-self.v[0], -self.v[1], -self.v[2])

    def __eq__(self, v):
        """ Test equality

            Note that Python DOES NOT automatically imply/implement that __ne__ is the logical negation of __eq__
        """
        if not common.floatEq( self.v[0], v.v[0] ):
            return False
        if not common.floatEq( self.v[1], v.v[1] ):
            return False
        if not common.floatEq( self.v[2], v.v[2] ):
            return False
        if not common.floatEq( self.v[3], v.v[3] ):
            return False
        return True

    def __ne__(self, v):
        """ Test inequality

            Note that Python DOES NOT automatically imply/implement that __ne__ is the logical negation of __eq__
        """
        if common.floatEq( self.v[0], v.v[0] ):
            return False
        if common.floatEq( self.v[1], v.v[1] ):
            return False
        if common.floatEq( self.v[2], v.v[2] ):
            return False
        if common.floatEq( self.v[3], v.v[3] ):
            return False
        return True

    ##def normalize(self):
    ##    """ Normalize this vector in-place """
    ##    pass

    ##def getNormalized(self):
    ##    """ Return a computed normalized vector. This does not modify the vector object

    ##        To normalize the vector in-place, use normalize()
    ##    """
    ##    pass


    @property
    def x(self):
        return self.v[0]

    @x.setter
    def x(self, value):
        self.v[0] = float(value)

    @property
    def y(self):
        return self.v[1]

    @y.setter
    def y(self, value):
        self.v[1] = float(value)

    @property
    def z(self):
        return self.v[2]

    @z.setter
    def z(self, value):
        self.v[2] = float(value)

    @property
    def w(self):
        return self.v[3]

    @w.setter
    def w(self, value):
        self.v[3] = float(value)

    def makePoint(self):
        """ Make into a point (i.e., set w = 1.0) """
        self.v[3] = 1.0

    def makeVector(self):
        """ Make into a vector (i.e., set w = 0.0) """
        self.v[3] = 0.0
## ======================

def vScale(v, k):
    """ Scale Vector v, in-place """
    v[0] *= float(k)
    v[1] *= float(k)
    v[2] *= float(k)

def vGetScaled(v, k):
    """ Return a new Vector, the result of scaling v by k """
    return Vector(v[0] * float(k), v[1] * float(k), v[2] * float(k))

def vLength(v):
    """ Return Vector length """
    return (v[0]*v[0] + v[1]*v[1] + v[2]*v[2]) ** 0.5

def vLengthSquared(v):
    """ Return Vector length squared
    
        i.e., don't take the square root
    """
    return v[0]*v[0] + v[1]*v[1] + v[2]*v[2]

def vNormalize(v):
    """ Normalize Vector v in-place

        We could use vLength to calculate vector length here, but we compute it inline, because.. speed, maybe?
    
    """
    invLength = 1.0 / ((v[0]*v[0] + v[1]*v[1] + v[2]*v[2]) ** 0.5)

    v[0] *= invLength
    v[1] *= invLength
    v[2] *= invLength

def vGetNormalized(v):
    """ Return a new Vector, which is the normalized v Vector) """
    invLength = 1.0 / ((v[0]*v[0] + v[1]*v[1] + v[2]*v[2]) ** 0.5)

    return Vector(v[0] * invLength, v[1] * invLength, v[2] * invLength)

def vAdd(v, w):
    """ Return a new Vector, which is the result of v + w """
    return Vector(v[0] + w[0], v[1] + w[1], v[2] + w[2])

def vSub(v, w):
    """ Return a new Vector, which is the result of v - w """
    return Vector(v[0] - w[0], v[1] - w[1], v[2] - w[2])

def vDot(v, w):
    """ Return the dot product of v . w """
    return v[0]*w[0] + v[1]*w[1] + v[2]*w[2]

def vCross(v, w):
    """ Return a new Vector, which is the cross product, v x w """
    return Vector(v[1]*w[2] - w[1]*v[2], v[2]*w[0] - w[2]*v[0], v[0]*w[1] - w[0]*v[1])

#ret0 = v1 * w2 - v2 * w1
#ret1 = v2 * w0 - v0 * w2
#ret2 = v0 * w1 - v1 * w0



