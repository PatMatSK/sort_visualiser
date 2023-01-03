""" helpfull functions """
from ._setup import canvas, setup, TIME_OUT_OK


def light_up(lst1, lst2, idx):
    """ light up 2 lists different color to see their origin after merge """
    for i in lst1:
        i.paint('green')
    for i in lst2:
        i.paint('red')
    dist = setup.FRONT_BOARDER + (idx + len(lst1 + lst2)) * setup.RECT_WIDTH
    lines = [canvas.create_line(setup.FRONT_BOARDER + idx * setup.RECT_WIDTH, 0,
                                setup.FRONT_BOARDER + idx * setup.RECT_WIDTH, 500),
             canvas.create_line(dist, 0, dist, 500)]
    canvas.after(TIME_OUT_OK * 2)
    canvas.update()
    return lines


def turn_off(lines):
    """ delete cutting merge lines """
    canvas.after(2*TIME_OUT_OK)
    canvas.update()
    for i in lines:
        canvas.delete(i)


def merge(lst1, lst2, idx, slow):
    """ merge 2 lists into result starting at given position(idx) """
    if slow:
        lines = light_up(lst1, lst2, idx)
    res = []
    while lst1 and lst2:
        if lst1[0] < lst2[0]:
            res.append(lst1.pop(0))
        else:
            res.append(lst2.pop(0))
        res[-1].set_to_index(idx)
        idx += 1
    lst3 = lst1 + lst2  # one of them is empty
    while lst3:
        res.append(lst3.pop(0))
        res[-1].set_to_index(idx)
        idx += 1
    if slow:
        turn_off(lines)
    return res


def swap_conditional(lst):
    """ swap 2 items if in wrong order """
    if len(lst) == 2:
        if lst[1] < lst[0]:
            lst[0].swap_slow(lst[1])
            lst[0], lst[1] = lst[1], lst[0]
    return lst


def separate(lst, idx):
    """ return lists of lower and greater than last element of lst (also visually) """
    length = len(lst)
    lower, greater = [], []
    lt, gt = idx, idx + length - 1
    pivot = lst[-1]
    for x in lst[0:length - 1]:
        if x <= pivot:
            x.set_to_index(lt)
            lower.append(x)
            lt += 1
        elif x > pivot:
            x.set_to_index(gt)
            greater.append(x)
            gt -= 1
    pivot.set_to_index(lt)

    return lower, pivot, greater


def flatten(lst):
    """ return flatted list of nested lists """
    res = []
    for i in lst:
        if isinstance(i, list):
            res += (flatten(i))
        else:
            res.append(i)
    return res


def change_status(*args):
    """ repolarize buttons (lock before procedure and unlock after) """
    for one in args:
        if one['state'] == 'normal':
            one['state'] = 'disabled'
        else:
            one['state'] = 'normal'


def wrong_input(cmd):
    """ gives helpfull user info """
    print("Unknown command:", cmd)
    print("Allowed commands:\n\
- bs - bubble sort \n\
- ss - select sort \n\
- ms - merge sort \n\
- qs - quick sort \n\
- sbs - step bubble sort \n\
- sss - step select sort \n\
- sms - step merge sort \n\
- sqs - step quick sort \n\
- stat - show order of rectangles \n\
- resize X - change count of rectangles to X (possible values of X: 5, 10, 25, 50, 100) \n\
- mix - change order of rectangles \n\
- end - quit program\n")
