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
import sys
import os
from pymkfgame.audio import audio

class GameApplication(object):
    ''' Application class that stores all the data and stuff
    '''
    def __init__( self, window_size=None, bg_col=(0,0,0) ):
        ''' Application class
        '''
        # TODO make screen size customizable. Use the dot-access config dict structure
        # TODO should the assertions enforce input of type, int?
        # TODO make it possible to specify other window modes (e.g., double-buffer) in the ctor?

        # dirt-nasty initialization: window_size is a list [width, height], default = 800x600, and is resizable (well.. as long as pygame window is initialized as resizable)
        assert( (isinstance(window_size, list) and len(window_size) == 2) or (window_size is None) )
        if window_size: # window_size defaults to None, just to be extra safe avoiding weird behavior exhibited default function params are lists
            self.window_size = [window_size[0], window_size[1]] # janky way of deep-copying the supplied window size
        else:
            self.window_size = [800, 600]
        self.surface_bg = pygame.display.set_mode(self.window_size, pygame.DOUBLEBUF, 32)   # Feel free to add surfaces, for making viewports, etc.
        self.mixer = audio.AudioMixer()
        self.exepath = os.path.dirname(sys.argv[0])     # Get the path where the script is. This allows us to properly compute relative paths to assets, e.g. images, sounds, etc.

        assert( len(bg_col) == 3 )
        self.bg_col = (bg_col[0], bg_col[1], bg_col[2]) # No default param weirdness to worry about with a tuple, because it's immutable
        self.isRunning = True
        self._states = []   # States are managed via stack, which we will implement using a Python list

    def cleanup(self):
        pass

    def setRunningFlagToFalse(self, argsDict = None):
        """Set the application's isRunning flag to alse

           Note: argsDict is in the function header to accommodate EventQueue/Messaging system design. Those systems procedurally generate a function call that expects an arguments dict.
        """
        print "Thank you for playing :-)"
        self.isRunning = False

    def changeState(self, toState, takeWith=None):
        """Change State to toState

           takeWith is an object (likely a list or dict) of objects to transfer into to the toState
        """
        fromState = self.popState() # Get the current state and then pop it off the stack
        if fromState:
            fromState.Cleanup()

        self.pushState(toState, takeWith)

    def getState(self):
        """Return a reference to the state at the top of the stack"""
        if self._states:
            return self._states[ len(self._states) - 1 ]
        else:
            return None

    def pushState(self, toState, takeWith=None):
        """Push toState onto the stack"""
        self._states.append(toState)
        self.getState().Init(self, takeWith)

    def popState(self):
        """Remove state from the stack, and return it"""
        fromState = None
        if self._states:
            fromState = self._states.pop()
        return fromState

    def update(self, dt_s):
        """Call Update() on state at top of stack
           
           Call State's Update(), passing in a reference to the engine. The state may need a reference to the engine, especially when the engine has valuable data, e.g. time keeping or other objects the state needs access to
        """
        self.getState().Update(dt_s)

    def processEvents(self):
        """Call ProcessEvents on state at top of stack"""
        self.getState().ProcessEvents()

    def processCommands(self):
        """Call ProcessEvents on state at top of stack"""
        self.getState().ProcessCommands()

    def preRenderScene(self):
        """Call PreRender on state at top of stack"""
        self.getState().PreRenderScene()

    def renderScene(self):
        ''' Render scene
            NOTE render() does not 'write' to the screen.
        '''
        """Call PreRender on state at top of stack"""
        # Draw all states on the stack (this allows for one state to overlay on another, e.g. a pause menu overlaid on the game playing screen))
        for state in self._states:
            state.RenderScene()

    def postRenderScene(self):
        """Call PreRender on state at top of stack"""
        self.getState().PostRenderScene()
