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

