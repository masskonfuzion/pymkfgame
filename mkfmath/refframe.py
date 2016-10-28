import math

from pymkfgame.mkfmath import common
from pymkfgame.mkfmath.vector import *
from pymkfgame.mkfmath.matrix import * # We don't import specific classes from the matrix and vector modules because the module also has functions outside of any class

class ReferenceFrame(object):
    ''' A reference frame class

        This class is based on a left-handed system. The up vector corresponds to +Y axis; the look vector
        corresponds to the +Z axis (going into the screen)
    '''
    def __init__(self):
        self.up = Vector(0, 1, 0)
        self.look = Vector(0, 0, 1)     # Left-handed coordinate system means +z looks into the screen
        self.position = Vector(0, 0, 0)

    def setUpVector(self, x, y, z):
        self.up[0] = float(x)
        self.up[1] = float(y)
        self.up[2] = float(z)
        self.up[3] = 0.0

    def setLookVector(self, x, y, z):
        self.look[0] = float(x)
        self.look[1] = float(y)
        self.look[2] = float(z)
        self.look[3] = 0.0

    def setPosition(self, x, y, z):
        self.position[0] = float(x)
        self.position[1] = float(y)
        self.position[2] = float(z)
        self.position[3] = 0.0


    def getMatrix(self):
        ''' Compute the view matrix determined by self.up and self.look

            NOTE: self.up and self.look must be set. This library does not do any runtime checking to make sure

            Also, remember that matrices are column-major, so what look likes like a row in this return value
            is actually a column. The columns are | x axis | up vec | look vec | translate/position vec |
        '''
        # cross(yAxis, zAxis) gives you xAxis
        xAxis = vCross(self.up, self.look)

        return Matrix(
        xAxis[0], xAxis[1], xAxis[2], 0,
        self.up[0], self.up[1], self.up[2], 0,  # self.up[3] should be 0, but just in case, force the issue
        self.look[0], self.look[1], self.look[2], 0,
        self.position[0], self.position[1], self.position[2], 1
        )

