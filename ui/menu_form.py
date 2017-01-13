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

# Form is simply a list (or perhaps a dict)
# Each item in the list (or dict) is a Menu Item
## Also with a location on the screen (eventually should be specifiable by percentages or something, to accommodate many screen resolutions)
# Form has a bound config file (or just a bound data object)

# NOTE: A "better" import structure would be to have menu_form import its menu item classes, so that any UIForm object could immediately have access to them,
# and modules that import menu_form would not need to import the menu item classes

import json
import pygame
from pymkfgame.core import dot_access_dict
from pymkfgame.ui import menu_item_base


class UIForm(object):
    @staticmethod
    def createFontObject(fontPath, fontSize):
        return pygame.font.Font(fontPath, fontSize)

    def __init__(self, boundFile=None, menuDefFile=None, engineRef=None):
        """Create a form object that is bound to the given config file
            
           boundFile contains the file with the objet to be loaded/modified/written back (can be configs, high scores, etc.)
           menuDefFile contains layout/definition of the UI form
        """
        self._uiItems = []

        self._boundObj = None         # The dict that holds the configuration that this menu is controlling
        self._activeMenuItem = None # The active menu item (e.g. a spinner, label, button, etc.)
        self._activeSubItem = None  # The active menu item's active sub-item (e.g. a spinner's left arrow)
        self._font = None           # Font object for the form TODO - use a list? Possibly move into a FormManager class? (e.g. a FontManager could contain many forms, for multi-screen menus; and also, could manage all the font objects and what not)
        self._fontColor = None
        self._engineRef = engineRef 
        self._kbSelection = None    # The index # of the item selected by keyboard input
        self._maxKbSelection = None
        # NOTE: this._engineRef is currently not used and is a candidate for deprecation. 
        # - Instead of using engineRef to call functions belonging to the engine, pass-through actions (pass the action instruction back to the calling scope instead of executing it here in this scope)
        # allow calls to propagate through this class (e.g., mouse-click handler) to trigger an action on the form (e.g. flash a light when a button is clicked), but then also allow the caller to take its own action,
        # (e.g., change gamestate when the button is clicked). Admittedly, this design is probably over-engineered.. But eh, it's what I thought of..

        if boundFile:
            self._boundFile = boundFile     # The file name -- use this when reading and writing the file
            self.loadObjectFromFile()
        else:
            self._boundFile = None

        if menuDefFile:
            # TODO implement this -- load menu definition from json (or otherwise, delete this whole block)
            # Maybe call a function to load from json?
            pass
        else:
            # TODO don't hardcode menu definition? Right now, menu is hardcoded and passed into this constructor
            # NOTE: Right now, the menuDefFile is entirely unsed. And the menu items are defined outside the scope of this class
            pass

    def loadObjectFromFile(self):
        """Load config from the file specified in the constructor of this object"""
        with open(self._boundFile, 'r+') as fd:
            # TODO add error checking (e.g. IOError)?
            tmpDict = json.load(fd)
            self._boundObj = dot_access_dict.DotAccessDict(tmpDict)

    def saveConfigToFile(self):
        """Save config back to file specified in the constructor of this object"""
        with open(self._boundFile, 'w') as fd:
            json.dump(self._boundObj, fd)

    def processMouseEvent(self, event, engineRef):
        """Process mouse event

           Events are Pygame events
           engineRef is provided in case it is needed
        """
        # TODO Make it possible for the UI to know where the cursor is, and to be able to move the cursor with the mouse, joystick, whatever. Also, the UI should respond to button presses on the keyboard, mouse, joystick, whatever
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            pressedButtons = pygame.mouse.get_pressed() # [0] = left; [1] = middle; [2] = right
            timeStamp = pygame.time.get_ticks() / 1000.0 # get timestamp; convert to seconds
            #print "menu_form: captured mouse click: {}, coord:{}, time:{}".format(pressedButtons, mousePos, timeStamp)

            for uiItem in self._uiItems:
                # TODO test which mouse button is pressed before taking action
                if uiItem['uiItem'].isMouseWithinBounds(mousePos): 
                    #print "menu_form: Mouse click button {} in bounds of object id:{}".format(event.button, id(uiItem))
                    # TODO perhaps separate the setting of the active item (during collection phase) from the handling (e.g. setting initial timer)/update

                    # Before setting the active item, ensure that the currently active item (if there is one) is deactivated and taken out of editMode (if applicable, e.g. textboxes)
                    if self._activeMenuItem and id(self._activeMenuItem) != id(uiItem):
                        try:
                            self._activeMenuItem._editMode = 0
                        except AttributeError as e:
                            # If we're here, that means the object doesn't have an editMode attribute. No issue; just keep trucking along
                            # TODO: Perhaps replace try/except paradigm here with a method (e.g., disableEditMode()) in the base/subclass model? I suspect that may be faster (but I admit I haven't researched it)
                            pass
                    self._activeMenuItem = uiItem['uiItem']   # activeMenuItem is a variable that maybe can belong to a top-level UI manager object thingamajig
                    
                    self._activeMenuItem.setMouseButtonState(event.button - 1, menu_item_base.UIItemState.mouseButtonDown, pygame.time.get_ticks() / 1000.0)
                    self._activeMenuItem.setMousePosition(mousePos)

                    # NOTE: onClickFunc is meant to be an internal action; e.g., for spinner UI items, onClickFunc should increment/decrement the bound value
                    if self._activeMenuItem._onClickFunc:
                        # TODO perhaps the clickFuncs should take in the mouse position and button states? Or otherwise, the onClickFuncs should NOT take those, but should USE them, after they've been set elsewhere (e.g. in setMouseButtonState, setMousePosition, etc)?
                        self._activeMenuItem._onClickFunc() 

                    # NOTE: action is a pass-through action. It is not acted upon by the menu item itself, but rather it is passed back to the scope the owns thie UI item. That way, the scope can take the action (e.g. change game state or something like that)
                    # TODO maybe rename this to "passThruAction" or something. We're going to simply pass the input value through as a return value, to allow the calling scope to execute an action
                    if uiItem['action']:
                        return uiItem['action']

            # TODO Detect that the user clicked e.g. in menu whitespace, and set self._activeMenuItem to None

        elif event.type == pygame.MOUSEBUTTONUP:
            if self._activeMenuItem:
                # Unset whatever button was pressed (i.e. unset mouse tracking var of active menu item
                self._activeMenuItem.setMouseButtonState(event.button - 1, menu_item_base.UIItemState.mouseButtonUp, pygame.time.get_ticks() / 1000.0)

        return None

    def processKeyboardEvent(self, event, engineRef):
        """Process keyboard event

           Events are Pygame events
           engineRef is provided in case it is needed
        """
        if event.type == pygame.KEYDOWN:
            # TODO make the keys that confirm/cancel customizable. Also, distinguish between e.g. space bar pressed while editing textbox, vs space bar used to confirm entry (or maybe just remove the space bar from this list)
            #if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):  # Confirm selections with SPACE or ENTER
            if event.key == pygame.K_RETURN:                                    # Confirm selections with ENTER only
                # Confirm selection -- take action
                # TODO make action trigger keys/buttons configurable
                uiItem = self.getKBActiveItem()
                if uiItem:
                    # TODO maybe rename this to "passThruAction" or something. We're going to simply pass the input value through as a return value, to allow the calling scope to execute an action
                    if uiItem['action']:
                        #print "menu_form: Processing user keypress of RETURN key. action = {}".format(uiItem['action'])
                        return uiItem['action']

            elif event.key == pygame.K_DOWN:
                self._kbSelection += 1
                if self._kbSelection > self._maxKbSelection:
                    self._kbSelection = 0

            elif event.key == pygame.K_UP:
                self._kbSelection -= 1
                if self._kbSelection < 0:
                    self._kbSelection = self._maxKbSelection

            else:
                # TODO insert some logic here to determine whether or not to process keypresses that aren't the "confirm/cancel" keys
                if self._activeMenuItem and self._activeMenuItem._onKeyFunc:
                    self._activeMenuItem._onKeyFunc(event)

        return None

    def getKBActiveItem(self):
        for uiItem in self._uiItems:
            if uiItem['kbSelectIdx'] == self._kbSelection:
                return uiItem
        return None

    def addMenuItem(self, uiItem, kbSelectIdx=None, action=None):
        """Add a UI menu item to this form's list of UI items
        """
        self._uiItems.append( {'uiItem': uiItem, 'kbSelectIdx': kbSelectIdx, 'action': action} )
        # kbSelectIdx tells the item how to interact with the keyboard. The index # is the number in the list of keyboard-interactive items
        # Action is an instruction that ends up being passed back to the calling scope. That allows the UI to determine how the user interacted with it, but allow the calling scope to execute the necessary action.

    def update(self, dt_s):
        """Update
        """
        for uiItem in self._uiItems:
            uiItem['uiItem'].update(dt_s)

    def render(self, renderSurface):
        for uiItem in self._uiItems:
            uiItem['uiItem'].render(renderSurface)

            if uiItem['kbSelectIdx'] == self._kbSelection:
                # TODO add customizable "padding" value to enable space between the menu item and its surrounding outline/highlight
                surfSize = uiItem['uiItem']._surface.get_size()
                pygame.draw.rect(renderSurface, (192,128,0), (10, uiItem['uiItem']._position[1], surfSize[0], surfSize[1]), 2)

    def synchronize(self, initialKbSelection, maxKbSelection):
        """Set the index of the object selected by default (the keyboard highlight cursor), and the max kb selection index.
        
           Also synchronize any objects with internal data selection ranges (e.g. spinners) to match the object's internal 'pointer' with the location of the data range
           e.g., if a spinner can select an int between 1 and 5 (inclusive, i.e. range(1, 6)), and the config file is loaded with a value of 3, synchronize the spinner so its "selected" value points at the location of 3 in the list
        """
        self._kbSelection = initialKbSelection # It is necessary to set the selected item (the keyboard selection) manually. Otherwise, the UI has no way of knowing which item to interact with
        self._maxKbSelection = maxKbSelection # Janky hack to know how many kb-interactive items are on the form # TODO is there a better way to specify maximum? Or maybe write an algo that figures this out?

        for uiItem in self._uiItems:
            try:
                if hasattr(uiItem['uiItem'], '_dataIndex'):    # TODO perhaps put a type identifier in each class, to use that as a lookup, instead of hasattr foolishness
                    uiItem['uiItem']._dataIndex = uiItem['uiItem']._data.index(uiItem['uiItem']._boundObj[uiItem['uiItem']._boundItemKey])  # Set _dataIndex to the index in the _data list where the bound item is found

            except AttributeError as ae:
                # uiItem does not have a member called 'dataIndex'. Probably no no biggie
                #print ae
                continue
            except ValueError as ve:
                # uiItem's _data list does not contain the sought-after value (e.g., the config we're loading somehow has a value that is not in the range of possible selectable values)
                # TODO do something useful if we reach this condition (but we really shouldn't reach this condition)
                #print ve
                continue
                


