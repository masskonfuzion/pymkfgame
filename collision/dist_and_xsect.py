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
from pymkfgame.mkfmath import matrix

from pymkfgame.collision import plane   # TODO evaluate.. do we need this import?

##############################################################################
def closestPoint_Point_Plane(pt_q, pln):  # pt_q is read as "point q", a.k.a. the query point
    ''' Compute the closest point on the given plane to the given point

        Note: The plane normal (pln.n) MUST be normalized
    '''
    # closest point, R = Q - (n . (Q - P))n, where:
    # R = closest point (we're solving for R
    # Q = point somewhere in space
    # n = plane normal
    # P = plane point
    # We can say that R = Q - tn, where t = n . (Q - P), assuming that n is normalized

    #### Approach #1
    ###t = vector.vDot(pln.n, vector.vSub(pt_q, pln.p))  # t = length of vector pointing from pln.p to pt_q, along pln.n
    #### The closest point on the plane is the projection of pt_q onto pln, which is given by pt_q - t*pln.n
    ###return vector.vSub(pt_q, vector.vGetScaled(pln.n, t))

    # Approach #2
    #d = -(pln.n[0]*pln.p[0] + pln.n[1]*pln.p[1] + pln.n[2]*pln.p[2])
    d = (pln.n[0]*pln.p[0] + pln.n[1]*pln.p[1] + pln.n[2]*pln.p[2])
    t = vector.vDot(pln.n, pt_q) - d
    return vector.vSub(pt_q, vector.vGetScaled(pln.n, t))

