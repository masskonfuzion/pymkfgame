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

import pygame
from pymkfgame.gameobj.gameobj import GameObj # TODO rework in 3D? Or should this only be an overlay eg on the screen (in 2D, after projection/view transformation is applied?
from pymkfgame.mkfmath import vector

# TODO make sure gameobj supports the design of this engine

class DisplayMessage(GameObj):
    """ A class for overlaying text on the screen

        NOTE: This class DOES NOT place text into the game world. Z coordinates are ignored!
    """
    def __init__(self):
        super(DisplayMessage, self).__init__()
        self._text = ""
        self._ttl = 3.0
        self._age = 0.0
        self._alive = False
        self._color = (128, 128, 0)

    def create(self, txtStr="", position=[0,0], color=(128, 128, 0), ttl=3):
        # TODO distinguish between Points and Vectors.. Perhaps make a Point class? (Note that the bike game actually has a vestigial Point3D class, from the original QBASIC version; maybe we can incorporate that)
        self._text = txtStr
        self._color = color
        self.setPosition( position[0], position[1], 0.0 )
        self._ttl = ttl
        self._age = 0.0
        self._alive = True

    def changeText(self, txtStr):
        self._text = txtStr

    def update(self, dt_s):
        if not self._alive:
            return

        self._age += dt_s
        if self._age > self._ttl:
            self._alive = False


    def getTextSurface(self, fontObj):
        ''' Return a pygame text surface object. To render on-screen, the game must blit the surface to the screen
            The font object will be supplied by the DisplayMessageManager that manages this text
        '''
        # Could use sexy Python "a if c else b" ternary here; but whatever :-)
        retObj = None
        if self._alive:
            retObj = fontObj.render(self._text, True, self._color)

        return retObj

    ##def draw(self, surface):
    ##    # TODO - write this function
    ##    surface.blit( textSurf, (self._position[0], self._position[1]) )
    ##    pass

    # NOTE! This class does not have its own draw() becasue of reasons.. Each message would require a font to be specified, in order to render. We do not want to store the font object in the message itself; therefore, something else must draw this message (either the developer, by hand, or by using a DisplayMessageManager)


