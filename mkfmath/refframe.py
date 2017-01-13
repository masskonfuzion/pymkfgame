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

    #def getLookAtMatrix(self, eyeX, eyeY, eyeZ, ctrX, ctrY, ctrZ, upX, upY, upZ):
    #    up = Vector(upX, upY, upZ)  # No real need to normalize up, because we're going to normalize all of our vectors later
    #    z = vGetNormalized( Vector(ctrX - eyeX, ctrY - eyeY, ctrZ - eyeZ) )   # z is a vector pointing 'forward' from the eye to the center point

    #    # The potentially wrong way (using a "left-hand rule for cross products, which is probably not actually a thing...."
    #    x = vGetNormalized( vCross(up, z) )
    #    y = vGetNormalized( vCross(z, x) )

    #    return Matrix(x[0], x[1], x[2], 0, y[0], y[1], y[2], 0, z[0], z[1], z[2], 0, -eyeX, -eyeY, -eyeZ, 1)

    def getLookAtMatrix(self, eyeX, eyeY, eyeZ, ctrX, ctrY, ctrZ, upX, upY, upZ):
        eye = Vector(eyeX, eyeY, eyeZ)
        up = Vector(upX, upY, upZ)  # No real need to normalize up, because we're going to normalize all of our vectors later
        z = vGetNormalized( Vector(ctrX - eyeX, ctrY - eyeY, ctrZ - eyeZ) )   # z is a vector pointing 'forward' from the eye to the center point
        x = vGetNormalized( vCross(up, z) )
        y = vGetNormalized( vCross(z, x) )

        #return Matrix(x[0], x[1], x[2], 0, y[0], y[1], y[2], 0, z[0], z[1], z[2], 0, -vDot(eye, x), -vDot(eye, y), -vDot(eye, z), 1)
        return Matrix(x[0], x[1], x[2], 0, y[0], y[1], y[2], 0, z[0], z[1], z[2], 0, -vDot(eye, x), -vDot(eye, y), vDot(eye, z), 1)    # This is what is needed for left hand coordinate system - the translation puts the model into the space in front of the camera. i.e. if the camera is mapped to 0,0,0, then a visible object is at -xpos, -ypos, zpos (because +z is in front of the camera). This is different than the right-handed coordinate frame, in which objects visible to the camera have a negative z position

    #def getPerspectiveProjectionMatrix(self, fovy, aspect, zNear, zFar):
    #    ''' fovy is the field of view in the y direction (plays a role in calculating the view frustum (in degrees)
    #        aspect is the ratio of width to height
    #        zNear is the z coordinate of the near clipping plane
    #        zFar is the z coordinate of the far clipping plane
    #    '''
    #    f = 1 / common.tann(fovy / 2.0) # Normally we'd prefer to multiply, because it's a faster CPU operation than division, but the point here is to pre-compute this value, anyway. We'll only do this once
    #    #return Matrix(f/aspect, 0.0, 0.0, 0.0, 0.0, f, 0.0, 0.0, 0.0, 0.0, (zNear + zFar) / (zNear - zFar), (2 * zNear * zFar) / (zNear - zFar), 0.0, 0.0, -1.0, 0.0)
    #    return Matrix(f/aspect, 0.0, 0.0, 0.0, 0.0, f, 0.0, 0.0, 0.0, 0.0, -(zNear + zFar) / (zNear - zFar), -(2 * zNear * zFar) / (zNear - zFar), 0.0, 0.0, 1.0, 0.0)

    def getPerspectiveProjectionMatrix(self, fovy, aspect, zNear, zFar):
        ''' Return a matrix that projects points into a normalized cube, from (-1,-1,-1) - (1,1,1)

            NOTE: This matrix transforms points into the "clip" space defined by the cube. The actual clipping algorithm must be done elsewhere.
            Also, viewport transformation must be done elsewhere

            Note, this is for a left-handed coordinate system
        '''
        top = common.tann(fovy / 2.0) * zNear
        bottom = -top
        right = top * aspect
        left = bottom * aspect

        return Matrix(2.0 * zNear / (right - left), 0.0, 0.0, 0.0, 0.0, 2.0 * zNear / (top - bottom), 0.0, 0.0, (right + left) / (right - left), (top + bottom) / (top - bottom), -(zFar + zNear) / (zFar - zNear), -1.0, 0.0, 0.0, -(2.0 * zFar * zNear) / (zFar - zNear), 0.0)   # This is for a right-handed coordinate system, I think (from scratchapixel.com)
        #return Matrix(2.0 * zNear / (right - left), 0.0, 0.0, 0.0, 0.0, 2.0 * zNear / (top - bottom), 0.0, 0.0, (right + left) / (right - left), (top + bottom) / (top - bottom), (zFar + zNear) / (zFar - zNear), 1.0, 0.0, 0.0, (2.0 * zFar * zNear) / (zFar - zNear), 0.0)
        #return Matrix(2.0 * zNear / (right - left), 0.0, 0.0, 0.0, 0.0, 2.0 * zNear / (top - bottom), 0.0, 0.0, -(right + left) / (right - left), -(top + bottom) / (top - bottom), -(zNear + zFar) / (zNear - zFar), 1.0, 0.0, 0.0, (2.0 * zNear * zFar) / (zNear - zFar), 0.0)   # Self-derived coefficients.. Are they correct? Or wrong? I think it is wrong.. I think the NDC cube mapping needs to be in the opposite handed-ness of the normal coordinate system. That's because the pinhole camera model implemented by a projection matrix uses the eye (camera position) as the point of convergence (i.e., the "vanishing" point, but on-screen, the vanishing point needs to be off in the distance. I.e., the NDC cube needs to be the z-flip of the camera system. Sooo, see below
        #return Matrix(2.0 * zNear / (right - left), 0.0, 0.0, 0.0, 
        #              0.0, 2.0 * zNear / (top - bottom), 0.0, 0.0,
        #              -(right + left) / (right - left), -(top + bottom) / (top - bottom), -(zFar + zNear) / (zFar - zNear), 1.0,
        #              0.0, 0.0, (2.0 * zFar * zNear) / (zFar - zNear), 0.0)   # Self-derived coefficients.. Did the equations by hand.. I trust this (but it doesn't give me the expected result when cam z < 0; only when cam z > 0.. But I don't understand why

