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

import pygame
from pymkfgame.display_msg.display_msg import DisplayMessage
import os
import sys

class DisplayMessageManager(object):
    def __init__(self, fontPath=None, fontSize=16):
        """ Initialize a DisplayMessageManager with an optional font spec
        """
        super(DisplayMessageManager, self).__init__()
        if fontPath:
            self.setFont(fontPath, fontSize)
        else:
            self._font = pygame.font.SysFont("pygame", fontSize, bold=False, italic=False)    # TODO replace with the pygame default system font; or define SYSTEMDEFAULT to instruct setFont to use the default system font object

        self._messages = [] # Start with an empty list
        self._maxMessages = 64  # Preallocate this many message slots; cycle through them
        self._defaultTTL = 3.0 # message time to live, in seconds
        self._nextFreeSlot = 0

        self._preAllocateMemory()

    def _preAllocateMemory(self):
        for i in xrange(0, self._maxMessages):
            self._messages.append(DisplayMessage())

    def setMessage(self, txtStr="", position=[0,0], txtColor=(128,128,0), ttl=None):
        ''' Set the next message to be displayed by this message manager
        '''
        msg = self._getNextFreeSlot()

        # Ugly workaround ot allowing class member to be default parameter of class member function
        if ttl is None:
            ttl = self._defaultTTL

        if msg:
            msg.create(txtStr, position, txtColor, ttl)
        else:
            raise Exception("Ruh roh! I was unable to find a slot to store the message:{}!".format(txtStr))

    def clear(self):
        del self._messages[:]
        self._preAllocateMemory()
        self._nextFreeSlot = 0

    def getMessage(self, k):
        return self._messages[k]

    def getMessages(self):
        ''' Return message list.
            NOTE Python returns a reference to the list. There's no const protection like in C++, so be careful!
        '''
        return self._messages

    def setFont(self, fontPath, fontSize):
        ''' Set the font (given a path to a font)
        '''
        #TODO maybe allow a dict of fonts?
        self._font = pygame.font.Font( os.path.normpath('/'.join((os.path.dirname(sys.argv[0]),fontPath))), fontSize )   # TODO make it possible to pass in a font object?

    def _getNextFreeSlot(self):
        ''' Totally naive finder -- O(n) - worst-case, iterates through whole list
        '''
        retObj = None

        for msg in self._messages:
            if not msg._alive:
                retObj = msg

        # It's possible to return None here. Make sure to test for that case
        return retObj

    def update(self, dt_s):
        for msg in self._messages:
            msg.update(dt_s)


    def draw(self, screen):
        for msg in self._messages:
            if msg._alive:
                textSurface = msg.getTextSurface(self._font)
                xPos = msg._position[0]
                if xPos + textSurface.get_size()[0] > screen.get_size()[0]:
                    xPos = screen.get_size()[1] - textSurface.get_size()[0]
                screen.blit(textSurface, (xPos, msg._position[1]))
        
