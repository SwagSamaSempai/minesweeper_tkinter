#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from Grid import *
from random import sample
import sys

DEFAULT_BOMBS = 200
BOMB_SIGN = "B"
NO_VALUE = 0
CELL_WIDTH = 20
CELL_HEIGHT = 20
CELL_SEPARATOR = 7
COLOR_CANVAS = "white"
COLOR_SEPARATOR = "black"


class Minesweeper:
    def __init__(self, master, infos=None):
        self.root = master
        self.root.title("Minesweeper")
        self.bombs_number = DEFAULT_BOMBS
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT
        if infos:
            if len(infos) > 0:
                self.bombs_number = int(infos[0])
            if len(infos) > 1:
                self.cell_width = int(infos[1])
            if len(infos) > 2:
                self.cell_height = int(infos[2])
        self.grid = Grid(self.cell_width, self.cell_height, CELL_SEPARATOR)
        self.written = [False] * len(self.grid.lines)
        self.canvas_width = self.grid.get_width() * (self.cell_width + CELL_SEPARATOR)
        self.canvas_height = self.grid.get_height() * (self.cell_height + CELL_SEPARATOR)
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg=COLOR_CANVAS)
        self.canvas.bind("<Button-1>", self.treat_click)
        self.canvas.bind("<Button-3>", self.treat_click)
        self.canvas.pack()

        self.widgets = {}
        self.create_display()
        self.place_bombs(self.bombs_number)

    def place_bombs(self, number):
        bombs = sample(self.grid.cells.keys(), number)
        for bomb in bombs:
            self.grid.cells[bomb].set_value(BOMB_SIGN)
            for cell in self.grid.cells[bomb].get_surroundings():
                if self.grid.cells[cell].get_value() != BOMB_SIGN:
                    self.grid.cells[cell].inc_value()

    def create_display(self):
        for coordinates in self.grid.get_layout():
            x = coordinates[0]
            y = coordinates[1]
            self.widgets[(x, y)] = self.canvas.create_rectangle(
                x, y, x + self.cell_width, y + self.cell_height,
                fill="grey", tag="{0}:{1}".format(x, y), activeoutline="red")
            self.canvas.update()
        self.draw_lines()

    def draw_lines(self):
        for coordinates in self.grid.get_lines():
            x = coordinates[0]
            y = coordinates[1]
            if x == 0:
                self.canvas.create_line(0, y, self.canvas_width, y, fill=COLOR_SEPARATOR)
            else:
                self.canvas.create_line(x, 0, x, self.canvas_height, fill=COLOR_SEPARATOR)
            self.canvas.update()

    def treat_click(self, event):
        button_id = event.widget.find_closest(event.widget.canvasx(event.x), event.widget.canvasy(event.y))
        button_id = self.canvas.gettags(button_id)
        if len(button_id) == 2:
            x = int(button_id[0].split(":")[0])
            y = int(button_id[0].split(":")[1])
            if event.num == 1:
                self.reveal_cells(x, y)
            elif event.num == 3:
                self.toggle_flag(x, y)
            self.check_lines()

    def reveal_cells(self, i, j):
        totreat = [(i, j)]
        while len(totreat):
            x, y = totreat.pop()
            self.canvas.delete("{0}:{1}".format(x, y))
            frame = tk.LabelFrame(self.canvas, bd=0)
            self.widgets[(x, y)] = frame
            self.grid.cells[(x, y)].reveal()
            if self.grid.cells[(x, y)].get_value() == NO_VALUE:
                tk.Label(frame, text=' ', bg="white").pack()
                for coord in self.grid.cells[(x, y)].get_surroundings():
                    cell = self.grid.cells[coord]
                    if not cell.is_revealed():
                        self.canvas.update()
                        totreat.append(coord)
            else:
                tk.Label(frame, text=self.grid.cells[(x, y)].get_value(), bg="white").pack()
                self.canvas.create_window(x + self.cell_width / 2, y + self.cell_height / 2, window=frame)
                if self.grid.cells[(x, y)].get_value() == BOMB_SIGN:
                    messagebox.showinfo(title="Pas de chance...", message="Vous avez perdu.")
                    self.root.destroy()

    def check_lines(self):
        completed = [True] * len(self.grid.lines)
        for j in range(len(completed)):
            y = self.grid.lines[j]
            for i in [key[0] for key in self.grid.cells.keys() if key[1] == y]:
                if not (self.grid.cells[(i, y)].is_revealed() or self.grid.cells[(i, y)].is_bomb()):
                    completed[j] = False
        for l in range(len(self.written)):
            if not self.written[l] \
                    and completed[max(0, l - 2)] \
                    and completed[max(0, l - 1)] \
                    and completed[l] \
                    and completed[min(len(completed) - 1, l + 1)] \
                    and completed[min(len(completed) - 1, l + 2)]:
                self.reveal_line(self.grid.lines[l])
                self.written[l] = True

    def reveal_line(self, j):
        for i in [key[0] for key in self.grid.cells.keys() if key[1] == j]:
            self.canvas.delete("{0}:{1}".format(i, j))
            frame = tk.LabelFrame(self.canvas, bd=0)
            self.widgets[(i, j)] = frame
            text = self.grid.poem[
                int((j - CELL_SEPARATOR) / (self.cell_height + CELL_SEPARATOR))][
                int((i - CELL_SEPARATOR) / (self.cell_width + CELL_SEPARATOR))]
            tk.Label(frame, text=text, bg="white", font=("TkDefaultFont",
                                                         int((self.cell_width + self.cell_height) / 3))).pack()
            self.canvas.create_window(i + self.cell_width / 2, j + self.cell_height / 2, window=frame)

    def toggle_flag(self, x, y):
        button = self.widgets[(x, y)]
        if self.canvas.itemcget(button, "fill") == "grey":
            self.canvas.itemconfig(button, fill="red", activeoutline="yellow")
            if self.grid.cells[(x, y)].get_value() == BOMB_SIGN:
                self.grid.cells[(x, y)].set_bomb(True)
        else:
            self.canvas.itemconfig(button, fill="grey", activeoutline="red")
            self.grid.cells[(x, y)].set_bomb(False)


def main():
    root = tk.Tk()
    infos = sys.argv[:]
    if "Minesweeper.py" in infos:
        index = infos.index("Minesweeper.py")
        infos = infos[index + 1:]
        Minesweeper(root, infos)
    else:
        Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()
