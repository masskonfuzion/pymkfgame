from pymkfgame.mkfmath import matrix

class MatrixStack(object):
    ''' A matrix stack that will mimic OpenGL's matrix stack.
    
        Stack will grow toward increasing list indices

        (I've always wanted to write one of these.. Why not just use OpenGL? Because I want to learn)
    '''
    def __init__(self):
        self._m = []        # We're going to implement a stack using a list
        self._sp = 0        # Stack pointer

    def pushMatrix(self, m):
        ''' Push a matrix onto the stack

            NOTE; Because a stack is LIFO, you have to push the matrices on in the opposite order you
            want them to be multiplied. e.g., if you want to rotate, then translate, you would push
            translate first. That way, rotate is _accessed_ and multiplied first, during matrix
            composition
        '''

        # Make a deep copy of the incoming matrix
        matrix_copy = matrix.Matrix(
            m.v[0], m.v[1], m.v[2], m.v[3]
        ,   m.v[4], m.v[5], m.v[6], m.v[7]
        ,   m.v[8], m.v[9], m.v[10], m.v[11]
        ,   m.v[12], m.v[13], m.v[14], m.v[15]
        )

        self._m.append(matrix_copy)

    def popMatrix(self, m):
        ''' Pop head of the stack and discard it '''
        self._m.pop()

    def getMatrix(self):
        ''' Return the composed matrix resulting from multiplying all of the matrices in the stack
        '''
        composed_matrix = matrix.Matrix.matIdent()

        for mat in reversed(self._m):
            composed_matrix = matrix.mMultmat(mat, composed_matrix)

        return composed_matrix
