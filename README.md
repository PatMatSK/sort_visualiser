Sorting visualiser
-

(This project was done as semestrak work at CTU FIT BI-PYT)

This program displays sorting algorithms. You can run algorithm to see how it works, or go step by step. 
I have chosen 2 quadratic(Bubble sort, Select sort) and 2 logarithmic 
algorithms(Quick sort, Merge sort). Stepping quadratic algorithms shows one step of inner loop, while 
logarithmic shows one depth of recursion.  

Requirements:
- tkinter
- random
- pylint (testing)
- pytest (testing)
- math   (testing)

User can interact with program with GUI, or send commands from CLI.
To use GUI only, clone this repository, enter sorting_visualisation directory and run program with your version of python:

- python3 main.py

If you want to use CLI to control program, simply add 'cli' as argument during call:

- python3 main.py cli

Once you opened program with command above, you can use commands below to avoid interaction with buttons.

Allowed commands:
- bs - bubble sort
- ss - select sort
- ms - merge sort
- qs - quick sort
- sbs - step bubble sort
- sss - step select sort
- sms - step merge sort 
- sqs - step quick sort 
- stat - show order of rectangles 
- resize X - change count of rectangles to X (possible values of X: 5, 10, 25, 50, 100) 
- mix - shuffle rectangles 
- end - quit program

To run all tests simply run test.sh script. (You will probably need to add permission to execute first.)
- chmod +x test.sh
- ./test.sh

This will remove last line in main.py, runs test_sorting.py and after that puts last line back (so all tests can be done).
You can avoid this by manually commenting root.mainloop() in main.py and run test_sorting.py.

