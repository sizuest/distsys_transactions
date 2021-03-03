from random import random

ERROR_PROBABILITY = 0.1


class Warehouse:
    def __init__(self, name):
        self.name = name
        self.places = []

    def add_stock_position(self, position: 'Stock'):
        self.places.append(position)

    def get_positions(self):
        return self.places

    def get_stock_position(self, pos_name):
        for p in self.places:
            if p.get_name() == pos_name:
                return p

        raise Exception(self.name + ': ' + 'Position "' + pos_name + '" not found')


class Stock:

    def __init__(self, pos_name, dm, max_content, init_content=0):
        self.pos_name = pos_name
        self.dm = dm
        self.dm[self.pos_name] = init_content
        self.max_content = max_content

    def get_count(self):
        return self.dm[self.pos_name]

    def put(self, c):
        if ERROR_PROBABILITY > random():
            raise GeneralError(self.pos_name + ': ' + 'Unknown error!')

        # Check, if space is available
        if self.dm[self.pos_name] + c > self.max_content:
            raise SpaceNotAvailableError(self.pos_name + ': ' + 'Space not available, available ' +
                                         str(self.max_content - self.dm[self.pos_name]) +
                                         ', required ' + str(c) + '!')

        self.dm[self.pos_name] = self.dm[self.pos_name] + c

    def pick(self, c):
        if ERROR_PROBABILITY > random():
            raise GeneralError(self.pos_name + ': ' + 'Unknown error!')

        # Check, if material is available
        if self.dm[self.pos_name] < c:
            raise MaterialNotAvailableError(
                self.pos_name + ': ' + 'Material not available, available ' + str(self.dm[self.pos_name]) +
                ', required ' + str(c) + '!')

        self.dm[self.pos_name] = self.dm[self.pos_name] - c

    def get_name(self):
        return self.pos_name


class Error(Exception):
    pass


class MaterialNotAvailableError(Error):
    pass


class SpaceNotAvailableError(Error):
    pass


class GeneralError(Error):
    pass
