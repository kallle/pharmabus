class Dimensions:
    def __init__(self, width, height, depth):
        self._width = width
        self._height = height
        self._depth = depth

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def depth(self):
        return self._depth

    def __repr__(self):
        return ('Dimensions(width={self._width!r}, '
                'height={self._height!r}, '
                'depth={self._depth!r})'
                ).format(self=self)


def get_default_dimensions():
    return Dimensions(0, 0, 0)