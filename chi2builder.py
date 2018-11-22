
class Vector:
    def __init__(self, *vec):
        if 1 < len(vec):
            self._arr = list((x for x in vec))
        elif 1 == len(vec):
            if (type(vec[0]) == list or type(vec[0]) == tuple or
                    type(vec[0]).__name__ == "generator"):
                self._arr = list((x for x in vec[0]))
            elif (type(vec[0]).__name__ == "instance" and
                    vec[0].__class__ == Vector):
                self._arr = list((x for x in vec[0]._arr))
            elif type(vec[0]) == int or type(vec[0]) == float:
                self._arr = list(vec[0])
            else:
                raise "type error"
        else:
            raise "wrong number of arguments"

    def __str__(self):
        return str(self._arr)

    def __repr__(self):
        return "Vector(" + str(self._arr) + ")"

    def __len__(self):
        return len(self._arr)

    def __iter__(self):
        return self._arr.__iter__()

    def __getitem__(self, idx):
        if type(idx) != int:
            raise TypeError
        if idx < 0 or idx >= len(self):
            raise IndexError
        return self._arr[idx]

    def __setitem__(self, idx, val):
        if type(idx) != int:
            raise TypeError
        if idx < 0 or idx >= len(self):
            raise IndexError
        self._arr[idx] = val

    def __neg__(self):
        return Vector((-x for x in self))

    def __iadd__(self, other):
        if type(other).__name__ == "instance" and other.__class__ == Vector:
            if len(self) != len(other):
                return NotImplemented
            for i in xrange(0, len(self)):
                self._arr[i] += other._arr[i]
            return self
        elif type(other) == int or type(other) == float:
            for i in xrange(0, len(self)):
                self._arr[i] += other
            return self
        else:
            return NotImplemented

    def __add__(self, other):
        retVal = Vector(self)
        retVal += other
        return retVal

    def __radd__(self, other):
        retVal = Vector(self)
        retVal += other
        return retVal

    def __isub__(self, other):
        if type(other).__name__ == "instance" and other.__class__ == Vector:
            if len(self) != len(other):
                return NotImplemented
            for i in xrange(0, len(self)):
                self._arr[i] -= other._arr[i]
            return self
        elif type(other) == int or type(other) == float:
            for i in xrange(0, len(self)):
                self._arr[i] -= other
            return self
        else:
            return NotImplemented

    def __sub__(self, other):
        retVal = Vector(self)
        retVal -= other
        return retVal

    def __rsub__(self, other):
        if type(other) != int and type(other) != float:
            retVal = Vector(self)
            for i in xrange(0, len(self)):
                retVal._arr[i] = other - retVal._arr[i]
            return retVal
        else:
            return NotImplemented

    def __imul__(self, other):
        if type(other) == int or type(other) == float:
            for i in xrange(0, len(self)):
                self._arr[i] *= other
            return self
        else:
            return NotImplemented

    def __mul__(self, other):
        if type(other).__name__ == "instance" and other.__class__ == Vector:
            # dot product
            if len(self) != len(other):
                return NotImplemented
            tmp = 0
            for i in xrange(0, len(self)):
                tmp += self._arr[i] * other._arr[i]
            return tmp
        elif (type(other).__name__ == "instance" and other.__class__ == Matrix
                and 1 == other.rows() and other.columns() == len(self)):
            retVal = Matrix(len(self), len(self), *tuple((self[i] * other[0][j]
                for j in xrange(0, len(self)) for i in xrange(0, len(self)))))
            return retVal
        else:
            retVal = Vector(self)
            retVal *= other
            return retVal

    def __rmul__(self, other):
        if type(other) == int or type(other) == float:
            retVal = Vector(self)
            retVal *= other
            return retVal
        else:
            return NotImplemented

    def __idiv__(self, other):
        if type(other) == int or type(other) == float:
            for i in xrange(0, len(self)):
                self._arr[i] /= other
            return self
        else:
            return NotImplemented

    def __div__(self, other):
        retVal = Vector(self)
        retVal /= other
        return retVal


class Matrix:
    def __init__(self, *vec):
        if 1 == len(vec):
            # one parameter:
            # Matrix(otherMatrix) or Matrix([[...], ...]) or
            # Matrix(((...), ...))
            if (type(vec[0]).__name__ == "instance" and
                    vec[0].__class__ == Matrix):
                self._rows = vec[0]._rows
                self._cols = vec[0]._cols
                self._arr = list((list((vec[0]._arr[i][j] for j in xrange(0,
                    self._cols))) for i in xrange(0, self._rows)))
            elif type(vec[0]) == list or type(vec[0]) == tuple:
                if type(vec[0][0]) == list or type(vec[0][0]) == tuple:
                    # okay, we're being passed a list of lists or a tuple of
                    # tuples
                    for i in xrange(0, len(vec[0])):
                        if len(vec[0][0]) != len(vec[0][i]):
                            raise "shape error"
                    self._rows = len(vec[0])
                    self._cols = len(vec[0][0])
                    self._arr = list((list((vec[0][i][j] for j in xrange(0,
                        self._cols))) for i in xrange(0, self._rows)))
                else:
                    raise "type error"
            else:
                raise "type error"
        elif 1 < len(vec):
            # more than one parameter:
            # rows, columns (for zero matrix), or
            # rows, columns, list, or
            # rows, columns, tuple, or
            # rows, columns, elements...
            if 2 == len(vec):
                self._rows = vec[0]
                self._cols = vec[1]
                self._arr = list((list((0 for j in xrange(0, self._cols))) for i in xrange(0, self._rows)))
            elif 3 <= len(vec):
                if 1 <= vec[0] * vec[1] and (type(vec[2]) == int or type(vec[2]) == float):
                    if len(vec) != (vec[0] * vec[1] + 2):
                        raise "wrong number of elements"
                    self._rows = vec[0]
                    self._cols = vec[1]
                    self._arr = list((list((vec[2 + i * self._cols + j] for j
                        in xrange(0, self._cols))) for i in xrange(0,
                            self._rows)))
                elif 3 == len(vec) and (type(vec[2]) == list or type(vec[2]) == tuple):
                    if len(vec[2]) != vec[0] * vec[1]:
                        raise "wrong number of elements"
                    self._rows = vec[0]
                    self._cols = vec[1]
                    self._arr = list((list((vec[2][i * self._cols + j] for j
                        in xrange(0, self._cols))) for i in xrange(0,
                            self._rows)))
                elif 3 == len(vec) and type(vec[2]).__name__ == "generator":
                    self._rows = vec[0]
                    self._cols = vec[1]
                    data = list((vec[2] for i in xrange(0, self._rows * self._cols)))
                    self._arr = list((list((data[i * self._cols + j] for j
                        in xrange(0, self._cols))) for i in xrange(0,
                            self._rows)))
                else:
                    raise "type error"
            else:
                raise "type error"
        else:
            raise "wrong number of arguments"

    def __str__(self):
        return str(self._arr)

    def __repr__(self):
        return "Matrix(" + str(self._arr) + ")"

    def __len__(self):
        return len(self._arr)

    def rows(self):
        return self._rows

    def columns(self):
        return self._cols

    def __iter__(self):
        return self._arr.__iter__()

    def __getitem__(self, idx):
        if type(idx) != int:
            raise TypeError
        if idx < 0 or idx >= len(self):
            raise IndexError
        return self._arr[idx]

    def __setitem__(self, idx, val):
        if type(idx) != int:
            raise TypeError
        if idx < 0 or idx >= len(self):
            raise IndexError
        self._arr[idx] = val

    def __neg__(self):
        return Matrix(list((list((-el for el in row)) for row in self)))

    def __add__(self, other):
        retVal = Matrix(self)
        retVal += other
        return retVal

    def __iadd__(self, other):
        if type(other).__name__ == "instance" and other.__class__ == Matrix:
            if self.rows() != other.rows() or self.columns() != other.columns():
                return NotImplemented
            for i in xrange(0, self._rows):
                for j in xrange(0, self._cols):
                    self._arr[i][j] += other._arr[i][j]
            return self
        elif type(self) == int or type(other) == float:
            for i in xrange(0, self._rows):
                for j in xrange(0, self._cols):
                    self._arr[i][j] += other
            return self
        else:
            return NotImplemented

    def __sub__(self, other):
        retVal = Matrix(self)
        retVal -= other
        return retVal

    def __isub__(self, other):
        if type(other).__name__ == "instance" and other.__class__ == Matrix:
            if self.rows() != other.rows() or self.columns() != other.columns():
                return NotImplemented
            for i in xrange(0, self._rows):
                for j in xrange(0, self._cols):
                    self._arr[i][j] -= other._arr[i][j]
            return self
        elif type(self) == int or type(other) == float:
            for i in xrange(0, self._rows):
                for j in xrange(0, self._cols):
                    self._arr[i][j] -= other
            return self
        else:
            return NotImplemented

    def __imul__(self, other):
        if type(self) == int or type(other) == float:
            for i in xrange(0, self._rows):
                for j in xrange(0, self._cols):
                    self._arr[i][j] *= other
            return self
        else:
            return NotImplemented

    def __mul__(self, other):
        if type(other).__name__ == "instance" and other.__class__ == Matrix:
            if self.columns() != other.rows():
                return NotImplemented
            retVal = Matrix(self.rows(), other.columns())
            for i in xrange(0, self.rows()):
                for j in xrange(0, other.columns()):
                    t = 0
                    for k in xrange(0, other.rows()):
                        t += self[i][k] * other[k][j]
                    retVal[i][j] = t
            if 1 == retVal.rows() * retVal.columns():
                return retVal[0][0]
            return retVal
        elif type(other).__name__ == "instance" and other.__class__ == Vector:
            if self.columns() != len(other):
                return NotImplemented
            retVal = Vector(((sum((self._arr[i][j] * other[j] for j in xrange(0,
                len(other)))) for i in xrange(0, self.rows()))))
            if 1 == len(retVal):
                return retVal[0]
            return retVal
        elif type(other) == int or type(other) == float:
            retVal = Matrix(self)
            retVal *= other
            return retVal
        else:
            return NotImplemented

    def __rmul__(self, other):
        if type(other) == int or type(other) == float:
            retVal = Matrix(self)
            retVal *= other
            return retVal
        else:
            return NotImplemented

    def __idiv__(self, other):
        if type(self) == int or type(other) == float:
            for i in xrange(0, self._rows):
                for j in xrange(0, self._cols):
                    self._arr[i][j] /= other
            return self
        else:
            return NotImplemented

    def __div__(self, other):
        if type(other) == int or type(other) == float:
            retVal = Matrix(self)
            retVal /= other
            return retVal
        else:
            return NotImplemented


def transpose(other):
    if type(other).__name__ == "instance" and other.__class__ == Matrix:
        return Matrix(other.columns(), other.rows(), *tuple(other[j][i] for j
            in xrange(0, other.rows()) for i in xrange(0, other.columns())))
    elif type(other).__name__ == "instance" and other.__class__ == Vector:
        return Matrix(1, len(other), *tuple(other[i] for i in xrange(0,
            len(other))))
    else:
        return NotImplemented

