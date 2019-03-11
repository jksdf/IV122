import argparse
import sys
import traceback

import src.Base
import src.week1.Solution
import src.week2.Solution
import src.week3.Solution
import src.week4.Solution


def run_task(week, task, fnprovider):
    try:
        res = task.run(fnprovider('{}_{}_'.format(week, task.name)))
    except Exception as e:
        res = 'The task has raised a {} exception'.format(e)
        traceback.print_exc()
    print('\n{}\n\nWeek {} Part {}:\n{}'.format('#' * 80, week, task.name, res))


def run(args):
    solutions = {1: src.week1.Solution.SOLUTIONS, 2: src.week2.Solution.SOLUTIONS, 3: src.week3.Solution.SOLUTIONS, 4: src.week4.Solution.SOLUTIONS}
    tasks = []
    for week in (solutions if 'all' in args.weeks else args.weeks):
        for task in solutions[week]:
            tasks.append((week, task))
    for week, task in args.tasks:
        found = False
        for otask in solutions[week]:
            if otask.name == task:
                tasks.append((week, otask))
                found = True
                break
        assert found
    fnprovider = src.Base.TmpFilenameProvider if args.folder is None else (
        lambda folder: (lambda meta: src.Base.RealFilenameProvider(folder, meta)))(args.folder)
    for week, task in tasks:
        run_task(week, task, fnprovider)


def week_parse(s):
    try:
        return int(s)
    except ValueError:
        if s == 'all':
            return s
        raise ValueError


def task_parse(s):
    if '/' not in s:
        raise ValueError
    w, t = s.split('/', 1)
    w = int(w)
    return w, t


def main(args):
    parser = argparse.ArgumentParser(description='Run the tasks for IV122.')
    parser.add_argument('--weeks', dest='weeks', nargs='*', metavar='W', type=week_parse,
                        help='The weeks to evaluate or "all"', default=[])
    parser.add_argument('--tasks', dest='tasks', nargs='*', metavar='T', type=task_parse, help='The tasks to evaluate.',
                        default=[])
    parser.add_argument('--folder', dest='folder', metavar='folder',
                        help='The path to store the results to (default creates temp files)')
    args = parser.parse_args(args[1:])
    run(args)


if __name__ == '__main__':
    main(sys.argv)
