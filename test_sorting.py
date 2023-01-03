""" test module """
# codestyle tests taken from homeworks
import pytest
import inspect
from pylint.lint import Run
from pylint.reporters import CollectingReporter
from math import log2
import main
from components import _help_functions, _index, _sort_system, _setup
from components._setup import setup
from components._sort_system import sort_sys

RANDOM_TEST = 1000
# this is testing so we can speed it up
_setup.TIME_OUT_OK = 1
_setup.TIME_OUT_SWAP = 1
_setup.TIME_OUT_MOVE = 1


@pytest.fixture
def linter():
    """ Test codestyle for src file. From BI-PYT homeworks """
    src_file0 = inspect.getfile(main)
    src_file1 = inspect.getfile(_setup)
    src_file2 = inspect.getfile(_index)
    src_file3 = inspect.getfile(_sort_system)
    src_file4 = inspect.getfile(_help_functions)

    rep = CollectingReporter()
    r = Run(
        # 0103 variables name (does not like shorter than 2 chars) (__lt__, ...)
        ["--disable=C0103", "-sn", src_file0, src_file1, src_file2, src_file3, src_file4],
        reporter=rep,
        exit=False,
    )
    return r.linter


@pytest.mark.parametrize("limit", range(0, 11))
def test_codestyle_score(linter, limit, runs=[]):
    """Evaluate codestyle for different thresholds.  From BI-PYT homeworks ."""
    if len(runs) == 0:
        print("\nLinter output:")
        for m in linter.reporter.messages:
            print(f"{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}")
    runs.append(limit)
    score = linter.stats.global_note

    print(f"pylint score = {score} limit = {limit}")
    assert score >= limit


def is_end(sort):
    if sort == 'sbs' or sort == 'sss':
        if sort_sys.i >= setup.RECT_COUNT:
            sort_sys.index1 = None
            sort_sys.index2 = None
            return True
        return False
    elif sort == 'sqs':
        tmp = [len(x) for x in sort_sys.lists]
        return 1 == max(tmp)
    else:
        return not sort_sys.j


@pytest.mark.parametrize("sort", ['ms', 'bs', 'ss', 'qs'])
@pytest.mark.parametrize("count", [5, 10, 25, 50, 100])
def test_sort(sort, count):
    """ testing each sort """
    counts = {5: 0, 10: 1, 25: 2, 50: 3, 100: 4}
    sorts = {'bs': 0, 'ss': 1, 'ms': 2, 'qs': 3}
    main.count_combobox.current(counts[count])
    main.sort_combobox.current(sorts[sort])
    main.randomize()
    ref = str(sorted(setup.rectangles))
    main.sort_button.invoke()

    assert ref == str(setup.rectangles)


def test_random():
    """ check that data are really random """
    data = {str(setup.rectangles)}
    for i in range(RANDOM_TEST):       # chance of match is very low but not zero
        main.randomize()
        assert str(setup.rectangles) not in data
        data.add(str(setup.rectangles))


@pytest.mark.parametrize("sort", ['sqs', 'sbs', 'sss', 'sms'])
@pytest.mark.parametrize("count", [5, 10, 25, 50, 100])
def test_steps(sort, count):
    """ count of steps in files, depends on time requirements quadratic/logarithmic """
    counts = {5: 0, 10: 1, 25: 2, 50: 3, 100: 4}
    steps = {'sbs': 0, 'sss': 1, 'sms': 2, 'sqs': 3}
    main.count_combobox.current(counts[count])
    main.sort_combobox.current(steps[sort])
    main.randomize()

    if sort in ['sms', 'sqs']:                  # n*log n
        maximum = int(count * log2(count))      # but steps are bigger, so this is quiet overkill
    else:
        maximum = count * int(count)             # n*n
    ref = str(sorted(setup.rectangles))

    for i in range(maximum):
        main.step_button.invoke()
        if is_end(sort):        # very possible that this will finish sooner
            break
    res = str(setup.rectangles)
    assert ref == res
