#############################################################################
# Copyright 2016 Mass KonFuzion Games
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

import sys
import pygame
from pymkfgame.gameobj.gameobj import GameObj
from pymkfgame.collision.common import CollisionGeomType
from pymkfgame.mkfmath import vector
from pymkfgame.mkfmath import matrix

class AABB(GameObj):    # TODO decide.. should collision geometry derive from GameObj?
    def __init__(self):
        super(AABB, self).__init__()

        self._minPt = (0.0, 0.0, 0.0)    # TODO should we put a Point3D class into the pymkfgame engine?
        self._maxPt = (0.0, 0.0, 0.0)
        self._type = CollisionGeomType.aabb # The idea is to give the collision geom an identifier that lets the game decide how to handle collisions involving geoms of this type

    def __str__(self):
        return "minPt:{} maxPt:{} type:{}".format(self._minPt, self._maxPt, self._type)

    def computeBounds(self, model):
        ''' Compute the AABB bounding the model object
        '''
        # TODO rename this function to update? Hmm, no probably not.. But maybe make an update() function that simply calls computeBounds? (the reason is: we want update to follow the update(self, dt_s) paradigm of the engine. Or, we could give the aabb a reference to the model it's tracking, and then this can be update(self, dt_s), without having to make any other calls.
        # TODO add the Wireframe class to the engine
        # TODO revisit this function. It's probably ripe for optimization
        obj_refs = [ model ]   # Start by adding a reference to the input model

        xmin = sys.maxint
        ymin = sys.maxint
        zmin = sys.maxint

        xmax = -sys.maxint + 1
        ymax = -sys.maxint + 1
        zmax = -sys.maxint + 1

        for obj_ref in obj_refs:    # Note, the refs list can grow while being iterated. As long as we hit the stop condition, the loop will iterate over the whole list, and properly
            if obj_ref.children:
                for child_name, child_ref in obj_ref.children.iteritems():  # NOTE: we don't NEED the child_name; it's useful for debugging
                    #print "Adding {}:{}".format(child_name, child_ref)
                    obj_refs.append(child_ref)

            for point in obj_ref._xpoints:  # _xpoints is a list of Point3D objects. TODO add Point3D class to engine
                xmin = min(xmin, point.x)
                ymin = min(ymin, point.y)
                zmin = min(zmin, point.z)

                xmax = max(xmax, point.x)
                ymax = max(ymax, point.y)
                zmax = max(zmax, point.z)

        self._minPt = (xmin, ymin, zmin)
        self._maxPt = (xmax, ymax, zmax)
        #print "Min: ({}, {}, {}), Max: ({}, {}, {})".format(self._minPt[0], self._minPt[1], self._minPt[2], self._maxPt[0], self._maxPt[1], self._maxPt[2])

    def isColliding(self, other):
        ''' Test for collision with the another AABB, aptly named, "other"
        '''
        # Note: This code is optimized for readability, not performance
        if self._maxPt[0] < other._minPt[0] or self._minPt[0] > other._maxPt[0]:
            return False

        if self._maxPt[1] < other._minPt[1] or self._minPt[1] > other._maxPt[1]:
            return False

        if self._maxPt[2] < other._minPt[2] or self._minPt[2] > other._maxPt[2]:
            return False

        return True

    # NOTE: CollisionAABB doesn't have an update() method because 'updates' will be handled by the objects that own the AABB


    def draw(self, surface, matView=matrix.Matrix.matIdent(), matViewport=matrix.Matrix.matIdent()):
        ''' Draw the AABB

            Note: Here we draw a line wireframe. We're not concerned with vertex order or hidden surface or any of that crap.
        '''
        # We need:
        # Points
        # 0 = (xmin, ymin, zmin)
        # 1 = (xmax, ymin, zmin)
        # 2 = (xmax, ymax, zmin)
        # 3 = (xmin, ymax, zmin)
        # 4 = (xmin, ymin, zmax)
        # 5 = (xmax, ymin, zmax)
        # 6 = (xmax, ymax, zmax)
        # 7 = (xmin, ymax, zmax)
        # Lines
        # 0 - 1 # front face (or back face, whatever)
        # 1 - 2
        # 2 - 3
        # 3 - 0
        # 4 - 5 # back face (or front face, whatever)
        # 5 - 6
        # 6 - 7
        # 7 - 4
        # 0 - 4 # Connect front face to back face (connect corners to each other)
        # 1 - 5
        # 2 - 6
        # 3 - 7


        pt0 = vector.Vector( self._minPt[0], self._minPt[1], self._minPt[2], 1.0 )
        pt1 = vector.Vector( self._maxPt[0], self._minPt[1], self._minPt[2], 1.0 )
        pt2 = vector.Vector( self._maxPt[0], self._maxPt[1], self._minPt[2], 1.0 )
        pt3 = vector.Vector( self._minPt[0], self._maxPt[1], self._minPt[2], 1.0 )

        pt4 = vector.Vector( self._minPt[0], self._minPt[1], self._maxPt[2], 1.0 )
        pt5 = vector.Vector( self._maxPt[0], self._minPt[1], self._maxPt[2], 1.0 )
        pt6 = vector.Vector( self._maxPt[0], self._maxPt[1], self._maxPt[2], 1.0 )
        pt7 = vector.Vector( self._minPt[0], self._maxPt[1], self._maxPt[2], 1.0 )

        tpt0 = matrix.mMultvec(matView, pt0)    # the tpt0 means "transformed pt0"
        tpt1 = matrix.mMultvec(matView, pt1)
        tpt2 = matrix.mMultvec(matView, pt2)
        tpt3 = matrix.mMultvec(matView, pt3)
        tpt4 = matrix.mMultvec(matView, pt4)
        tpt5 = matrix.mMultvec(matView, pt5)
        tpt6 = matrix.mMultvec(matView, pt6)
        tpt7 = matrix.mMultvec(matView, pt7)

        vptpt0 = matrix.mMultvec(matViewport, tpt0)    # the vptpt0 means "viewport transformed pt0" (btw, all of this rendering code is terrible and should be taken out back and shot)
        vptpt1 = matrix.mMultvec(matViewport, tpt1)
        vptpt2 = matrix.mMultvec(matViewport, tpt2)
        vptpt3 = matrix.mMultvec(matViewport, tpt3)
        vptpt4 = matrix.mMultvec(matViewport, tpt4)
        vptpt5 = matrix.mMultvec(matViewport, tpt5)
        vptpt6 = matrix.mMultvec(matViewport, tpt6)
        vptpt7 = matrix.mMultvec(matViewport, tpt7)



        color = (0, 192, 0) # TODO eventually un-hardcode the debug draw color
        pygame.draw.line( surface, color, (vptpt0[0], vptpt0[1]), (vptpt1[0], vptpt1[1]) )  # TODO - project 3D to 2D
        pygame.draw.line( surface, color, (vptpt1[0], vptpt1[1]), (vptpt2[0], vptpt2[1]) )
        pygame.draw.line( surface, color, (vptpt2[0], vptpt2[1]), (vptpt3[0], vptpt3[1]) )
        pygame.draw.line( surface, color, (vptpt3[0], vptpt3[1]), (vptpt0[0], vptpt0[1]) )

        pygame.draw.line( surface, color, (vptpt4[0], vptpt4[1]), (vptpt5[0], vptpt5[1]) )
        pygame.draw.line( surface, color, (vptpt5[0], vptpt5[1]), (vptpt6[0], vptpt6[1]) )
        pygame.draw.line( surface, color, (vptpt6[0], vptpt6[1]), (vptpt7[0], vptpt7[1]) )
        pygame.draw.line( surface, color, (vptpt7[0], vptpt7[1]), (vptpt4[0], vptpt4[1]) )

        pygame.draw.line( surface, color, (vptpt0[0], vptpt0[1]), (vptpt4[0], vptpt4[1]) )
        pygame.draw.line( surface, color, (vptpt1[0], vptpt1[1]), (vptpt5[0], vptpt5[1]) )
        pygame.draw.line( surface, color, (vptpt2[0], vptpt2[1]), (vptpt6[0], vptpt6[1]) )
        pygame.draw.line( surface, color, (vptpt3[0], vptpt3[1]), (vptpt7[0], vptpt7[1]) )

