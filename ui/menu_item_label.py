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

# Label = form control with a text display (technically, it's not a "control" -- it's just a label :-D)

from pymkfgame.ui import menu_item_base
import pygame

# TODO: Note, now that we've added the _locked property to the base menu item (on 7/3/2016), the label is probably redundant. A locked textbox is functionally equivalent
class MenuItemLabel(menu_item_base.MenuItemBase):
    def __init__(self, posList, fontObj, text, locked=True):
        super(MenuItemLabel, self).__init__(pos=posList)
        self._font = fontObj    # This assigns a reference to an already-existing font object
        #self.setSurface( menu_item_base.MenuItemBase.createText(text , self._font, (255,255,255)) ) # TODO: Font color should be customizable
        self.setSurface( menu_item_base.MenuItemBase.createText(text , self._font, (60,190,30)) ) # TODO: Font color should be customizable
        self._locked = locked

    def render(self, renderSurface):
        renderSurface.blit(self._surface, (self._position[0], self._position[1]))

    def hasSubItems(self):
        """Return True if this item has subitems; False if not"""
        return False
