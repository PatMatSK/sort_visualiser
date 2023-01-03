""" Index class """
from ._setup import setup, canvas, tk, TIME_OUT_MOVE


class Index:
    """ Visual index for steppers """
    def __init__(self, idx, x, y, txt):
        self.y = int(y)
        self.i = idx
        self.index = canvas.create_text(int(x), int(y), text=txt)

    def __del__(self):
        try:
            canvas.delete(self.index)
        except tk.TclError:
            pass

    def set_to(self, idx):
        """ change place of this index to index:i """
        canvas.coords(self.index,
                      setup.FRONT_BOARDER+setup.RECT_WIDTH/2+setup.RECT_WIDTH*idx, self.y)
        self.i = idx

    def move(self, dist=1):
        """ move index to right """
        self.i += dist
        for _ in range(int(dist)*setup.RECT_WIDTH):
            canvas.move(self.index, 1, 0)
            canvas.after(TIME_OUT_MOVE)
            canvas.update()
