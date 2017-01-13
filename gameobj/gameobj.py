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

## TODO.. MAKE 3D! Use pymkfmath vector and matrix and all that

import pygame
import sys
from pymkfgame.mkfmath import vector

class GameObj(object):
    ''' Game Object Class purpose-built for Low Rez Jam 2016. The game must take place in a 64x64 grid
    '''
    def __init__(self):
        # TODO make the GameObj a container of things, e.g. physics component (which does velocity/accel/etc), render component, etc. For now, we're going to cheat and assume that every object has all of these properties
        self._position = vector.Vector()
        #self._size = [2, 2]     # default size is 2 "pixels" by 2 pixels (1 "pixel" is a square on the 64x64 grid # TODO let's see if we can get rid of this for the 3D engine
        self._velocity = vector.Vector()
        self._acceleration = vector.Vector()
        self._image = None
        self._rect = None

        self.update_delay_dict = {} # key/value pairs, e.g.: { 'on_row': 0.25, 'falling': 0.1 }
        self._objState = 0 # object's state.
        self._accumulator_s = [0.0, 0.0]

    ##def setSize(self, sx, sy):
    ##    ''' Set the size of the object, in terms of grid squares
    ##    '''
    ##    # TODO let's see if we can get rid of this for the 3D engine. This is an artifact of game design for the low rez jam
    ##    self._size[0] = sx
    ##    self._size[1] = sy

    def setPosition(self, gx, gy, qz):
        ''' Set the object's position on the grid (gx, gy)
        '''
        self._position[0] = gx
        self._position[1] = gy
        self._position[2] = gy

    def setSpeed(self, sx, sy, sz):
        ''' Set "speed" of object
            NOTE: Speed is defined as the # of "pixels" the object will move per update cycle. An update cycle is an interval of time the object must wait before making one move
        '''
        self._speed[0] = sx
        self._speed[1] = sy
        self._speed[2] = sz

    def update(self, dt_s, game_stats_obj):
        ''' Update (which really involves simply counting dt and figuring out whether or not we should be moving or sitting still)
        '''
        # NOTE: game_stats_obj is an object that has vital game info, e.g. score, level, etc. For this base class, we should consider using **args or some other construct that allows flexibility for many different inputs to the Update() function
        # dt_s is delta-time, in seconds
        raise NotImplementedError

    def draw(self, screen):
        # Might not need draw() if we're blitting images to the screen surface
        raise NotImplementedError
        pass

    def loadImage(self, filename):
        self._image = pygame.image.load(filename)
        self._rect = self._image.get_rect()



