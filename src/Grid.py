#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Cell import *


class Grid:
    def __init__(self, cell_width, cell_height, cell_separator, filename="poem.txt"):
        self.poem, self.width, self.height = self.parse_poem(filename)
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_separator = cell_separator
        self.lines = []
        self.cells = {}
        for i, j in self.get_layout():
            if j not in self.lines:
                self.lines.append(j)
            self.cells[(i, j)] = Cell(i, j, self.width, self.height, cell_width, cell_height, cell_separator)

    @staticmethod
    def parse_poem(filename):
        matrix = []
        file = open(filename, encoding="utf-8")
        width = 0
        for line in file:
            buffer = []
            for char in line.strip():
                buffer.append(char)
            matrix.append(buffer)
            width = len(buffer) if len(buffer) > width else width
        file.close()
        for line in matrix:
            for _ in range(len(line), width):
                line.append('')
        return matrix, width, len(matrix)

    def get_lines(self):
        coordinates = []
        for i in range(self.height):
            y = (i + 1) * (self.cell_height + self.cell_separator) + self.cell_separator / 2
            x = 0
            coordinates.append((x, y))
        for j in range(self.width):
            x = (j + 1) * (self.cell_width + self.cell_separator) + self.cell_separator / 2
            y = 0
            coordinates.append((x, y))
        return coordinates

    def get_layout(self):
        coordinates = []
        for i in range(self.height):
            y = (self.cell_height + self.cell_separator) * i + self.cell_separator
            for j in range(self.width):
                x = (self.cell_width + self.cell_separator) * j + self.cell_separator
                coordinates.append((x, y))
        return coordinates

    def get_cells(self):
        return self.cells

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
