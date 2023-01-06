""" Setup of sorting visualiser """
import tkinter as tk
from random import randint


CANVAS_WIDTH = 1100
CANVAS_HEIGHT = 500
TIME_OUT_MOVE = 1
TIME_OUT_SWAP = 20
TIME_OUT_OK = 600
OFFSET = 20

root = tk.Tk()
root.resizable(False, False)
root.title("Sort Visualiser")
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack()

# -------------------------------------------SETUP-------------------------------------------------
# -------------------------------------------SETUP-------------------------------------------------


class SetUp:
    """ Stores global data of current settings """
    def __init__(self):
        self.RECT_WIDTH = 100
        self.RECT_COUNT = 10
        self.FRONT_BOARDER = int((CANVAS_WIDTH - (self.RECT_WIDTH * self.RECT_COUNT)) / 2)
        self.BACK_BOARDER = self.FRONT_BOARDER + self.RECT_WIDTH * self.RECT_COUNT
        self.rectangles = []

    def refresh_values(self, cnt):
        """ refresh values, according to new cnt(rectangle count) if needed"""
        if cnt != self.RECT_COUNT:
            self.rectangles = []
            self.RECT_COUNT = cnt
            self.RECT_WIDTH = int(1000 / self.RECT_COUNT)
            self.FRONT_BOARDER = int((CANVAS_WIDTH - (self.RECT_WIDTH * self.RECT_COUNT)) / 2)
            self.BACK_BOARDER = self.FRONT_BOARDER + self.RECT_WIDTH * (self.RECT_COUNT - 1)
            self.initiate_rect()

    def initiate_rect(self):
        """ Build rectangles """
        offset = self.FRONT_BOARDER
        for i in range(self.RECT_COUNT):
            self.rectangles.append(Rectangle(i, offset))
            offset += self.RECT_WIDTH
        canvas.update()

    def reset_rect(self, color='blue'):
        """ repaint all rectangles """
        for i in self.rectangles:
            i.paint(color)

    def finito(self):
        """ List is sorted """
        for i in self.rectangles:
            i.paint('green')
            canvas.after(TIME_OUT_SWAP * 2)
            canvas.update()
            i.paint()


# -------------------------------------------RECTANGLE----------------------------------------------
# -------------------------------------------RECTANGLE----------------------------------------------


class Rectangle:
    """ Comparable objects for algorithms """
    def __init__(self, index, offset):
        self.length = randint(30, 450)
        self.index = index
        self.x = offset
        self.rect = canvas.create_rectangle(offset, OFFSET,
                                            offset + setup.RECT_WIDTH, self.length, fill='Blue')

    def __del__(self):
        try:
            canvas.delete(self.rect)
        except tk.TclError:
            pass

    def __lt__(self, x):
        return self.length < x.length

    def __le__(self, x):
        return self.length <= x.length

    def __gt__(self, x):
        return self.length > x.length

    def __eq__(self, x):
        return self.length == x.length

    def __repr__(self):
        return str(self.length)

    def paint(self, color='blue'):
        """ Paint rectangles with given color """
        canvas.itemconfig(self.rect, fill=color)

    def ok_with(self, x):
        """ Show this and x rectangles ar in good mutual position """
        self.paint('green')
        x.paint('green')
        canvas.update()
        canvas.after(TIME_OUT_OK)
        self.paint()
        x.paint()

    def reshape(self):
        """ Change to random size """
        self.length = randint(OFFSET, 450)
        x0, y0, x1, _ = canvas.coords(self.rect)
        canvas.coords(self.rect, x0, y0, x1, self.length)

    def set_to_index(self, position):
        """ Set this rectangle to given position(index) """
        if self.index != position:
            self.index = position
            x1 = setup.FRONT_BOARDER + position * setup.RECT_WIDTH
            x2 = setup.FRONT_BOARDER + (position + 1) * setup.RECT_WIDTH
            canvas.coords(self.rect, x1, OFFSET, x2, self.length)
            canvas.after(TIME_OUT_SWAP)
            canvas.update()

    def swap(self, second):
        """ Swap places of 2 rectangles """
        idx = self.index
        self.set_to_index(second.index)
        second.set_to_index(idx)

    def swap_slow(self, second):
        """ Swap places of 2 rectangles slowly """
        if self.index > second.index:
            second.swap_slow(self)
            return
        self.paint('red')
        second.paint('red')

        rng = (second.index - self.index) * setup.RECT_WIDTH
        for _ in range(rng):
            canvas.move(self.rect, 1, 0)
            canvas.move(second.rect, -1, 0)
            canvas.after(TIME_OUT_MOVE)
            canvas.update()
        self.paint()
        second.paint()
        second.index, self.index = self.index, second.index
        canvas.update()


setup = SetUp()
setup.initiate_rect()
