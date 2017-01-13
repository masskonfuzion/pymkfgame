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

from pymkfgame.mkfmath import vector

class Plane(object):
    ''' A plane class in point-normal format
    '''
    def __init__(self, p=None, n=None):
        if p is None:
            self.p = vector.Vector()
        else:
            self.p = vector.Vector(p[0], p[1], p[2], p[3])  # Note that because p is a point, p[3] could be non-zero

        if n is None:
            self.n = vector.Vector()  # surface normal vector. Should always be unit length (i.e., normalized.. a normalized normal. Punny)
        else:
            self.n = vector.Vector(n[0], n[1], n[2], n[3])  # Note that for a true vector, n[3] should be 0


