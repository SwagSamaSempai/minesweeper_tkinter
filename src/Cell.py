#!/usr/bin/python3
# -*- coding: utf-8 -*-
NO_VALUE = 0


class Cell:
    def __init__(self, x, y, width, height, cell_width, cell_height, cell_separator):
        self.x = x
        self.y = y
        self.value = NO_VALUE
        self.revealed = False
        self.isbomb = False
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_separator = cell_separator
        self.max_x = (self.cell_width + self.cell_separator) * (width - 1) + self.cell_separator
        self.max_y = (self.cell_height + self.cell_separator) * (height - 1) + self.cell_separator

    def get_surroundings(self):
        for i in [-(self.cell_width + self.cell_separator), 0, self.cell_width + self.cell_separator]:
            for j in [-(self.cell_height + self.cell_separator), 0, self.cell_height + self.cell_separator]:
                if not (i == 0 and j == 0) and 0 <= self.x + i <= self.max_x and 0 <= self.y + j <= self.max_y:
                    yield (self.x + i, self.y + j)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def inc_value(self):
        self.value += 1

    def is_revealed(self):
        return self.revealed

    def reveal(self):
        self.revealed = True

    def set_bomb(self, boolean):
        self.isbomb = boolean

    def is_bomb(self):
        return self.isbomb
