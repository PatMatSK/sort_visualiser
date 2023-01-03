""" Sorting visualiser """
import sys
from tkinter import ttk
from components._setup import setup, tk, root
from components._sort_system import sort_sys
from components._help_functions import change_status, wrong_input


BUTTON_WIDTH = 22


def button_prep(is_sorting):
    """ lock buttons and reset values if needed """
    change_status(step_button, sort_button, random_button)
    setup.refresh_values(int(count_combobox.get()))
    sort_type = sort_combobox.get()
    if is_sorting or sort_sys.stepper != sort_type:
        sort_sys.reset()

    return sort_type


def sort():
    """ Call selected sorted function """
    sort_type = button_prep(True)

    if sort_type == 'bubblesort':
        sort_sys.bubblesort()
    elif sort_type == 'selectsort':
        sort_sys.selectsort()
    elif sort_type == 'mergesort':
        setup.rectangles = sort_sys.mergesort(setup.rectangles, 0)
    else:
        setup.rectangles = (sort_sys.quicksort(setup.rectangles, 0))

    setup.finito()
    change_status(step_button, sort_button, random_button)


def randomize():
    """ Reset calculated sub-results and randomize rectangles """
    sort_sys.reset()
    setup.refresh_values(int(count_combobox.get()))
    for i in range(setup.RECT_COUNT):
        setup.rectangles[i].reshape()


def step():
    """ Execute one step of chosen sort """
    sort_type = button_prep(False)

    if sort_type == 'bubblesort':
        sort_sys.bubblesort_step()
    elif sort_type == 'selectsort':
        sort_sys.selectsort_step()
    elif sort_type == 'mergesort':
        sort_sys.mergesort_step()
    else:
        sort_sys.quicksort_step()

    change_status(step_button, sort_button, random_button)


def work_from_cmd():
    """ user input handler """
    sorts = {'bs': 0, 'ss': 1, 'ms': 2, 'qs': 3}
    steps = {'sbs': 0, 'sss': 1, 'sms': 2, 'sqs': 3}
    counts = {'5': 0, '10': 1, '25': 2, '50': 3, '100': 4}

    while True:
        cmd = input("~> ")
        if len(cmd.split(' ')) == 2:
            arg = cmd.split(' ')[1]
            cmd = cmd.split(' ')[0]
            if cmd == 'resize' and arg in counts:
                count_combobox.current(counts[arg])
                sort_sys.reset()
                setup.refresh_values(int(arg))
            else:
                wrong_input(cmd+' '+arg)
        elif cmd in sorts:
            sort_combobox.current(sorts[cmd])
            sort_button.invoke()
        elif cmd in steps:
            sort_combobox.current(steps[cmd])
            step_button.invoke()
        elif cmd == 'mix':
            random_button.invoke()
        elif cmd == 'stat':
            print(setup.rectangles)
        elif cmd == 'end':
            root.destroy()
            break
        else:
            wrong_input(cmd)


# ------------------------------------------WIDGETS------------------------------------------------
# ------------------------------------------WIDGETS------------------------------------------------

sort_button = tk.Button(root, text='SORT', command=sort, width=BUTTON_WIDTH)
random_button = tk.Button(root, text='RANDOMIZE', command=randomize, width=BUTTON_WIDTH)
step_button = tk.Button(root, text='STEP', command=step, width=BUTTON_WIDTH)
sort_combobox = ttk.Combobox(root,
                             values=['bubblesort', 'selectsort', 'mergesort', 'quicksort'],
                             state='readonly')
count_combobox = ttk.Combobox(root,
                              values=["5", "10", "25", "50", "100"],
                              state='readonly')
count_combobox.current(1)
sort_combobox.current(0)

sort_button.pack()
random_button.pack()
step_button.pack()
sort_combobox.pack()
count_combobox.pack()


def main():
    """ user preference """
    args = sys.argv
    if len(args) == 2:
        if args[1] == 'cli':
            work_from_cmd()


if __name__ == '__main__':
    main()

root.mainloop()
