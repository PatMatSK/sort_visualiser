""" Logic of whole sorting """
from ._setup import canvas, setup, TIME_OUT_OK, CANVAS_WIDTH
from ._help_functions import separate, swap_conditional, flatten, merge
from ._index import Index


class SortSystem:
    """ Sorting system """
    def __init__(self):
        self.i = 0
        self.j = 0
        self.min_index = 0
        self.index1 = None
        self.index2 = None
        self.lists = []
        self.stepper = ""

    def reset(self):
        """ reset edited values """
        for i in range(setup.RECT_COUNT):
            setup.rectangles[i].index = i
        self.i = 0
        self.j = 0
        self.min_index = 0
        self.index1 = None
        self.index2 = None
        self.lists = []
        self.stepper = ""

    def bubblesort(self):
        """ Bubble sort """
        for i in range(setup.RECT_COUNT):
            for j in range(setup.RECT_COUNT-i-1):
                if setup.rectangles[j] > setup.rectangles[j + 1]:
                    setup.rectangles[j], setup.rectangles[j + 1] = \
                        setup.rectangles[j + 1], setup.rectangles[j]
                    setup.rectangles[j].swap(setup.rectangles[j + 1])

    def selectsort(self):
        """ Select sort """
        for i in range(setup.RECT_COUNT):
            min_index = i
            for j in range(i + 1, setup.RECT_COUNT):
                if setup.rectangles[j] < setup.rectangles[min_index]:
                    min_index = j

            setup.rectangles[i], setup.rectangles[min_index] = \
                setup.rectangles[min_index], setup.rectangles[i]
            setup.rectangles[i].swap(setup.rectangles[min_index])

    def mergesort(self, lst, idx):
        """ Merge sort, idx represents index of first element in lst in global scope rectangles """
        length = len(lst)
        if length == 1:
            return lst
        if length == 2:
            res = lst.copy()
            if lst[1] < lst[0]:
                res[0], res[1] = res[1], res[0]
                res[0].set_to_index(idx)
                res[1].set_to_index(idx + 1)
            return res
        l1 = self.mergesort(lst[0:length//2], idx)
        l2 = self.mergesort(lst[length//2: length], idx+length//2)
        return merge(l1, l2, idx, False)

    def quicksort(self, lst, idx):
        """ Quick sort, idx represents index of first element in lst in global scope rectangles  """
        length = len(lst)
        if length <= 1:
            return lst

        lower, pivot, greater = separate(lst, idx)
        return self.quicksort(lower, idx) + [pivot] + self.quicksort(greater, idx+len(lower)+1)

# ---------------------------------------STEPPERS--------------------------------------
# ---------------------------------------STEPPERS--------------------------------------

    def sel_sort_init(self):
        """ set initial data for select sort """
        self.index1 = Index(1, setup.FRONT_BOARDER + setup.RECT_WIDTH / 2, 10, 'min')
        self.index2 = Index(0, setup.FRONT_BOARDER + setup.RECT_WIDTH * 3 / 2, 10, 'i')
        self.j = 1
        self.stepper = "selectsort"

    def bub_sort_init(self):
        """ set initial data for bubble sort """
        self.index1 = Index(0, setup.FRONT_BOARDER + setup.RECT_WIDTH / 2, 10, 'i')
        self.index2 = Index(1, setup.FRONT_BOARDER + setup.RECT_WIDTH * 3 / 2, 10, 'i+1')
        self.stepper = "bubblesort"

    def merge_sort_init(self):
        """ set initial data for merge sort """
        self.j = []
        self.lists = self.merge_prep(setup.rectangles, 0)
        setup.rectangles = flatten(self.lists)
        self.stepper = "mergesort"

    def inner_select_loop(self):
        """ shift indexes for select sort step and switch rectangles,
            this is called at the end of inner loop """
        setup.rectangles[self.min_index].swap_slow(setup.rectangles[self.i])
        setup.rectangles[self.min_index], setup.rectangles[self.i] = \
            setup.rectangles[self.i], setup.rectangles[self.min_index]
        self.i += 1
        self.j = self.i + 1
        self.min_index = self.i
        self.index1.set_to(self.i)
        self.index2.set_to(self.j)

    def inner_bubble_loop(self):
        """ shift indexes for bubbles sort step """
        self.j = 0
        self.i += 1
        self.index1.set_to(0)
        self.index2.set_to(1)

    def quick_list_prep(self):
        """ find nearest sublist to be sorted,
            and also retunrs index of it's first element in global scope """
        idx = 0
        length = len(self.lists)
        for i in range(length):
            if len(self.lists[i]) != 1:
                self.i = i
                return self.lists.pop(i), idx
            idx += 1
        return False, False             # only lists of length 1, so sorting is done

    def bubblesort_step(self):
        """ make one step of inner loop of quadratic bubblesort """
        if self.i == 0 and not self.index1:
            self.bub_sort_init()
            return

        if self.i >= setup.RECT_COUNT:
            self.index1 = None
            self.index2 = None
            setup.finito()
            return

        if self.j >= setup.RECT_COUNT-self.i-1:
            self.inner_bubble_loop()
            return

        if setup.rectangles[self.j] > setup.rectangles[self.j + 1]:
            setup.rectangles[self.j], setup.rectangles[self.j + 1] = \
                setup.rectangles[self.j + 1], setup.rectangles[self.j]
            setup.rectangles[self.j].swap_slow(setup.rectangles[self.j + 1])  # visual
        else:
            setup.rectangles[self.j].ok_with(setup.rectangles[self.j + 1])

        self.index1.move()
        self.index2.move()
        self.j += 1

    def selectsort_step(self):
        """ make one step of inner loop of quadratic selectsort """
        if self.i == self.j == 0:
            self.sel_sort_init()
            return

        if self.i >= setup.RECT_COUNT:
            self.index1 = None
            self.index2 = None
            setup.finito()
            return

        if self.j >= setup.RECT_COUNT:
            self.inner_select_loop()
            return

        if setup.rectangles[self.j] < setup.rectangles[self.min_index]:
            self.index1.move(self.j-self.min_index)
            self.min_index = self.j
        else:
            self.index2.move()
            self.j += 1

    def merge_prep(self, lst, idx):
        """ cut rectangles into the smallest lists, if its length is 2 -> swap if needed
            stores starting indexes to be moved after merge in global scale.
            final list looks this way -> [[[0, 1], [[2], [3, 4]]], [[5, 6], [[7], [8, 9]]]]"""
        length = len(lst)
        if length <= 2:
            return lst

        prev = self.merge_prep(lst[:length//2], idx)
        pos = self.merge_prep(lst[length//2:], idx + len(flatten(prev)))
        self.j.append(idx)      # starting index to be moved after merge
        return [prev, pos]

    def find_to_merge(self):
        """ returns lists that should be merged as first and stores path to self.i """
        lst1 = self.lists[0]
        lst2 = self.lists[1]
        self.i = []             # here is stored path made from indexes to list
        while isinstance(lst1[0], list) or isinstance(lst2[0], list):
            if isinstance(lst1[0], list):
                lst2 = lst1[1]
                lst1 = lst1[0]
                self.i.append(0)
            else:
                lst1 = lst2[0]
                lst2 = lst2[1]
                self.i.append(1)

        if not self.i:
            self.i = [0]

        return lst1, lst2

    def mergesort_step(self):
        """ make one recursion dive, first is to split list, others to merge splitted ones """
        if not self.lists:          # first step
            self.merge_sort_init()

        if not self.j:              # already sorted
            setup.finito()
            return

        lst1, lst2 = self.find_to_merge()
        lst1 = swap_conditional(lst1)
        lst2 = swap_conditional(lst2)

        m = self.lists
        for i in self.i[:-1]:  # get to the list to be merged
            m = m[i]

        if self.i == [0] and len(lst1) + len(lst2) == len(setup.rectangles):
            self.lists = merge(lst1, lst2, self.j.pop(0), True)
        else:
            m[self.i[-1]] = merge(lst1, lst2, self.j.pop(0), True)

        setup.reset_rect()
        setup.rectangles = flatten(self.lists)

    def connect_subresults(self, lower, greater, pivot):
        """ reconnect all separated elements back to setup.rectangles """
        if lower:
            self.lists.insert(self.i, lower)
            self.i += 1
        self.lists.insert(self.i, [pivot])
        if greater:
            self.lists.insert(self.i+1, greater)

        for i in lower:
            i.paint('green')
        for i in greater:
            i.paint('red')
        canvas.update()
        canvas.after(TIME_OUT_OK)
        canvas.update()

        setup.rectangles = [item for sublist in self.lists for item in sublist]

    def quicksort_step(self):
        """ inside one recursion
            find the nearest list bigger than 1 element and separate him
            into pivot, lower and greater  """
        if not self.lists:
            self.stepper = "quicksort"
            self.lists = [setup.rectangles]

        lst, idx = self.quick_list_prep()
        if lst == idx:                  # both is FALSE
            setup.finito()
            return

        pivot = lst[-1]
        pivot.paint('orange')
        l1 = canvas.create_line(setup.FRONT_BOARDER+setup.RECT_WIDTH*idx, 0,
                                setup.FRONT_BOARDER+setup.RECT_WIDTH*idx, 500)
        l2 = canvas.create_line(setup.FRONT_BOARDER+setup.RECT_WIDTH*(idx+len(lst)), 0,
                                setup.FRONT_BOARDER+setup.RECT_WIDTH*(idx+len(lst)), 500)
        l3 = canvas.create_line(0, pivot.length, CANVAS_WIDTH, pivot.length)
        canvas.after(TIME_OUT_OK)
        canvas.update()
        lower, pivot, greater = separate(lst, idx)
        self.connect_subresults(lower, greater, pivot)
        canvas.after(TIME_OUT_OK)
        canvas.update()
        setup.reset_rect()
        canvas.delete(l1, l2, l3)


sort_sys = SortSystem()
