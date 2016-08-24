class Vector(object):
    def __init__(self):
        """ Initialize a 3D vector """
        self.v = [0.0, 0.0, 0.0]

    def __str__(self):
        return "< {}, {}, {} >".format(self.v[0], self.v[1], self.v[2])

    def __getitem__(self, item):
        """ Get component indexed by item #

            NOTE: no error checking because we're lazy. We'll let the list obj do its own error checking
        """
        return self.v[item]

    def __setitem__(self, item, value):
        """ Set component indexed by item #

            NOTE: no error checking because we're lazy. We'll let the list obj do its own error checking
        """
        if item in [0,1,2]:
            self.v[item] = float(value)


    @property
    def x(self):
        return self.v[0]

    @x.setter
    def x(self, value):
        self.v[0] = float(value)

    @property
    def y(self):
        return self.v[1]

    @y.setter
    def y(self, value):
        self.v[1] = float(value)

    @property
    def z(self):
        return self.v[2]

    @z.setter
    def z(self, value):
        self.v[2] = float(value)

