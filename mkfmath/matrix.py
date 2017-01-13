#############################################################################
# Copyright 2016 Mass KonFuzion
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#############################################################################

"""
3D Matrix math class

Matrices will be stored as 3x3 matrices (a 9-item array).  The vector will be stored in column-major order, e.g. the 9-element array indexes are arranged like the following:

| 0 3 6 |
| 1 4 7 |
| 2 5 8 |

We're using column-major because, apparently, DirectX and OpenGL internally store matrices in column-major order. If we want to be interoperable with those, we'll need to comply. (NOTE: I haven't looked into Vulkan..)

We'll be post-multiplying vectors (i.e. T = Mv, where M is a 3x3 matrix, and v is a 3x1 vector. T, the transformed vector, is a 3x1 vector)

For point transformations, where some APIs use 4x1 vectors and 4x4 matrices (e.g., scale, rotate, translate), we'll handle the homogeneous coords internally within the functions, and return a Vector object (which is 3x1 by definition in this API

Also note: We're going to design our world with a left-handed coordinate system. +x points right, +y points up, and +z points INTO the screen. LHCS has the following rotation characteristisc:
* rotating about z turns the xy plane so that [1,0,0] rotates to [0,1,0] (i.e., how + rot about z looks in math books). 
* rotating about y turns the xz plane so that [0,0,1] rotates to [1,0,0]
* rotating about x turns the yz plane so that [0,1,0] rotates to [0,0,1]

# TODO: Maybe change to 4-element vectors and such.. If we ever want. Say we want to get a translation matrix from the engine, and hold onto it, to transform a bunch of points.. It's quickest to return that matrix as a 4x4

To compose transformations, we want, e.g. v' = vRT (where v' is transformed vec; R = rot mat; T = trans mat)
"""


import math

from pymkfgame.mkfmath import common
from pymkfgame.mkfmath.vector import Vector

class Matrix(object):
    # TODO maybe make a function that returns a composed XYZ rotation matrix (faster than composing the matrices by calling multiple individual rotation matrix multiplications
    @staticmethod
    def matRotX(th=0.0):
        """ Return a column-major matrix for rotation about the x axis, by th RADIANS
        
            th is short for theta.
        """
        v0  = 1.0
        v1  = 0.0
        v2  = 0.0
        v3  = 0.0

        v4  = 0.0
        v5  = math.cos(th)   # TODO possibly use a cos/sin lookup table for speed?
        v6  = math.sin(th)
        v7  = 0.0

        v8  = 0.0
        v9  = -math.sin(th)
        v10 = math.cos(th)
        v11 = 0.0

        v12 = 0.0
        v13 = 0.0
        v14 = 0.0
        v15 = 1.0

        return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)

    @staticmethod
    def matRotY(th=0.0):
        """ Return a column-major matrix for rotation about the x axis, by th RADIANS
        
            th is short for theta.
        """

        v0  = math.cos(th)
        v1  = 0.0
        v2  = -math.sin(th)
        v3  = 0.0

        v4  = 0.0
        v5  = 1.0
        v6  = 0.0
        v7  = 0.0

        v8  = math.sin(th)
        v9  = 0.0
        v10 = math.cos(th)
        v11 = 0.0

        v12 = 0.0
        v13 = 0.0
        v14 = 0.0
        v15 = 1.0
        
        return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)

    @staticmethod
    def matRotZ(th=0.0):
        """ Return a column-major matrix for rotation about the z axis, by th RADIANS
        
            th is short for theta.
        """
        v0  = math.cos(th)
        v1  = math.sin(th)
        v2  = 0.0
        v3  = 0.0

        v4  = -math.sin(th)
        v5  =  math.cos(th)
        v6  = 0.0
        v7  = 0.0

        v8  = 0.0
        v9  = 0.0
        v10 = 1.0
        v11 = 0.0

        v12 = 0.0
        v13 = 0.0
        v14 = 0.0
        v15 = 1.0

        return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)

    @staticmethod
    def matRotArb(th, px, py, pz, dx, dy, dz):
        """ Return a matrix for rotation about an arbitrary axis
            p (x,y,z) defines a point that the axis goes through
            d (x,y,z) defines the direction. d MUST BE NORMALIZED!
        """
        v0  = dx*dx + (dy*dy + dz*dz) * math.cos(th)
        v1  = dx * dy * (1.0 - math.cos(th)) + dz * math.sin(th)
        v2  = dx * dz * (1.0 - math.cos(th)) - dy * math.sin(th)
        v3  = 0.0

        v4  = dx * dy * (1.0 - math.cos(th)) - dz * math.sin(th)
        v5  = dy*dy + (dx*dx + dz*dz) * math.cos(th)
        v6  = dy * dz * (1.0 - math.cos(th)) + dx * math.sin(th)
        v7  = 0.0

        v8  = dx * dz * (1.0 - math.cos(th)) + dy * math.sin(th)
        v9  = dy * dz * (1.0 - math.cos(th)) - dx * math.sin(th)
        v10 = dz*dz * (dx*dx + dy*dy) * math.cos(th)
        v11 = 0.0

        v12 = (px * (dy*dy + dz*dz) - dx * (py*dy + pz*dz)) * (1 - math.cos(th)) + (py*dz - pz*dy) * math.sin(th)
        v13 = (py * (dx*dx + dz*dz) - dy * (px*dx + pz*dz)) * (1 - math.cos(th)) + (pz*dx - px*dz) * math.sin(th)
        v14 = (pz * (dx*dx + dy*dy) - dz * (px*dx + py*dy)) * (1 - math.cos(th)) + (px*dy - py*dx) * math.sin(th)
        v15 = 1.0

        return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)

    @staticmethod
    def matRotFromAxisAngle(th, ax, ay, az):
        """ Compute a rotation matrix from an axis and angle

            NOTE: The axis must be normalized, and th given in RADIANS
        """
        c = math.cos(th)
        s = math.sin(th)
        t = 1 - c

        v0  = t*ax*ax + c
        v1  = t*ax*ay - az*s
        v2  = t*ax*az + ay*s
        v3  = 0.0

        v4  = t*ax*ay + az*s
        v5  = t*ay*ay + c
        v6  = t*ay*az - ax*s
        v7  = 0.0

        v8  = t*ax*az - ay*s
        v9  = t*ay*az + ax*s
        v10 = t*az*az + c
        v11 = 0.0

        v12 = 0.0
        v13 = 0.0
        v14 = 0.0
        v15 = 1.0

        return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)

    @staticmethod
    def matScale(sx=1.0, sy=1.0, sz=1.0):
        v0  = sx
        v1  = 0.0
        v2  = 0.0
        v3  = 0.0

        v4  = 0.0
        v5  = sy
        v6  = 0.0
        v7  = 0.0

        v8  = 0.0
        v9  = 0.0
        v10 = sz
        v11 = 0.0

        v12 = 0.0
        v13 = 0.0
        v14 = 0.0
        v15 = 1.0

        return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)

    @staticmethod
    def matTrans(tx=0.0, ty=0.0, tz=0.0):
        v0  = 1.0
        v1  = 0.0
        v2  = 0.0
        v3  = 0.0

        v4  = 0.0
        v5  = 1.0
        v6  = 0.0
        v7  = 0.0

        v8  = 0.0
        v9  = 0.0
        v10 = 1.0 
        v11 = 0.0

        v12 = tx
        v13 = ty
        v14 = tz
        v15 = 1.0

        return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)

    @staticmethod
    def matIdent():
        ## TODO maybe make the ident matrix a member function? e.g., in-place set matrix to identity?
        v0  = 1.0
        v1  = 0.0
        v2  = 0.0
        v3  = 0.0

        v4  = 0.0
        v5  = 1.0
        v6  = 0.0
        v7  = 0.0

        v8  = 0.0
        v9  = 0.0
        v10 = 1.0
        v11 = 0.0

        v12 = 0.0
        v13 = 0.0
        v14 = 0.0
        v15 = 1.0

        return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)

    @staticmethod
    def matZero():
        ## TODO maybe make the zero matrix a member function? e.g., in-place set matrix to zero?
        v0  = 0.0
        v2  = 0.0
        v3  = 0.0
        v4  = 0.0

        v4  = 0.0
        v5  = 0.0
        v6  = 0.0
        v7  = 0.0

        v8  = 0.0
        v9  = 0.0
        v10 = 0.0
        v11 = 0.0

        v12 = 0.0
        v13 = 0.0
        v14 = 0.0
        v15 = 0.0

        return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)
    # TODO also compute matrix for rotation about an arbitrary axis?

    def __init__(self, v00=0.0, v01=0.0, v02=0.0, v03=0.0, v04=0.0, v05=0.0, v06=0.0, v07=0.0, v08=0.0, v09=0.0, v10=0.0, v11=0.0, v12=0.0, v13=0.0, v14=0.0, v15=0.0):
        """ Initialize matrix as a zero matrix

            REMEMBER!! Column-major. What looks like rows in this definition are actually columns, based on
            the math we've programmed
        """
        self.v = [ float(v00), float(v01), float(v02), float(v03), 
                   float(v04), float(v05), float(v06), float(v07), 
                   float(v08), float(v09), float(v10), float(v11), 
                   float(v12), float(v13), float(v14), float(v15) ]

    def __str__(self):
        s = """| {:06f}  {:06f}  {:06f}  {:06f} |
| {:06f}  {:06f}  {:06f}  {:06f} |
| {:06f}  {:06f}  {:06f}  {:06f} |
| {:06f}  {:06f}  {:06f}  {:06f} |"""

        return s.format(self.v[0], self.v[4], self.v[8], self.v[12], self.v[1], self.v[5], self.v[9], self.v[13], self.v[2], self.v[6], self.v[10], self.v[14], self.v[3], self.v[7], self.v[11], self.v[15])

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
        return Matrix(-self.v[0], -self.v[1], -self.v[2], -self.v[3], -self.v[4], -self.v[5], -self.v[6], -self.v[7], -self.v[8] )

    def __eq__(self, m):
        """ Test equality

            Note that Python DOES NOT automatically imply/implement that __ne__ is the logical negation of __eq__
        """
        for i in range(0, len(self.v)):
            if not common.floatEq( self.v[i], m.v[i] ):
                return False
        return True

    def __ne__(self, m):
        """ Test equality

            Note that Python DOES NOT automatically imply/implement that __ne__ is the logical negation of __eq__
        """
        for i in range(0, len(self.v)):
            if common.floatEq( self.v[i], m.v[i] ):
                return False
        return True


def mMultvec(m, v):
    """ Multiply Vector v with Matrix m

        Post-multiply m by v.
        Note: m is 4x4. v is 4x1. The resulting vector is 4x1

        This function handles points with a homogeneous coordinate (i.e. 4D, w == 1), and true "vectors", 3D
    """
    x = m[0]*v[0] + m[4]*v[1] + m[8] *v[2] + m[12]*v[3]    # m[12] is, e.g. the position in matrix for tx (translate)
    y = m[1]*v[0] + m[5]*v[1] + m[9] *v[2] + m[13]*v[3]
    z = m[2]*v[0] + m[6]*v[1] + m[10]*v[2] + m[14]*v[3]
    w = m[3]*v[0] + m[7]*v[1] + m[11]*v[2] + m[15]*v[3]

    # Handle homogeneous case
    if v[3] == 1.0 and w != 1.0:
        x /= w
        y /= w
        z /= w
        w = 1.0

    return Vector(x, y, z, w)


def mMultmat(ma, mb):
    """ Multiply matrix ma and mb

        Postmultiply mb
    """
    ## TODO test this matrix multiplication
    v0  = ma[0]*mb[0] + ma[4]*mb[1] + ma[8] *mb[2] + ma[12]*mb[3]
    v1  = ma[1]*mb[0] + ma[5]*mb[1] + ma[9] *mb[2] + ma[13]*mb[3]
    v2  = ma[2]*mb[0] + ma[6]*mb[1] + ma[10]*mb[2] + ma[14]*mb[3]
    v3  = ma[3]*mb[0] + ma[7]*mb[1] + ma[11]*mb[2] + ma[15]*mb[3]

    v4  = ma[0]*mb[4] + ma[4]*mb[5] + ma[8] *mb[6] + ma[12]*mb[7]
    v5  = ma[1]*mb[4] + ma[5]*mb[5] + ma[9] *mb[6] + ma[13]*mb[7]
    v6  = ma[2]*mb[4] + ma[6]*mb[5] + ma[10]*mb[6] + ma[14]*mb[7]
    v7  = ma[3]*mb[4] + ma[7]*mb[5] + ma[11]*mb[6] + ma[15]*mb[7]

    v8  = ma[0]*mb[8] + ma[4]*mb[9] + ma[8] *mb[10] + ma[12]*mb[11]
    v9  = ma[1]*mb[8] + ma[5]*mb[9] + ma[9] *mb[10] + ma[13]*mb[11]
    v10 = ma[2]*mb[8] + ma[6]*mb[9] + ma[10]*mb[10] + ma[14]*mb[11]
    v11 = ma[3]*mb[8] + ma[7]*mb[9] + ma[11]*mb[10] + ma[15]*mb[11]

    v12 = ma[0]*mb[12] + ma[4]*mb[13] + ma[8] *mb[14] + ma[12]*mb[15]
    v13 = ma[1]*mb[12] + ma[5]*mb[13] + ma[9] *mb[14] + ma[13]*mb[15]
    v14 = ma[2]*mb[12] + ma[6]*mb[13] + ma[10]*mb[14] + ma[14]*mb[15]
    v15 = ma[3]*mb[12] + ma[7]*mb[13] + ma[11]*mb[14] + ma[15]*mb[15]

    return Matrix(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15)


## TODO 
# matrix inverse
# matrix transpose (for a matrix composed of orthonormal vectors, the transpose is the inverse)
# determinant
# perhaps some static functions for the class:
# zero out matrix (in-place)
# make matrix identity matrix (in-place)
# - getRotMat
# - getTransMat
# - getScaleMat
# - getZeroMat
# - getIdMat
