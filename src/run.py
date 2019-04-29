import argparse
import sys
import traceback

import Base
import week1.Solution
import week11.Solution
import week2.Solution
import week3.Solution
import week4.Solution
import week5.Solution
import week6.Solution
import week7.Solution
import week8.Solution
import week9.Solution


def run_task(week, task, fnprovider):
    try:
        res = task.run(fnprovider('{}_{}_'.format(week, task.name)))
    except Exception as e:
        res = 'The task has raised a {} exception'.format(e)
        traceback.print_exc()
    print('\n{}\n\nWeek {} Part {}:\n{}'.format('#' * 80, week, task.name, res))


def run(args):
    solutions = {1: week1.Solution.SOLUTIONS, 2: week2.Solution.SOLUTIONS, 3: week3.Solution.SOLUTIONS,
                 4: week4.Solution.SOLUTIONS, 5: week5.Solution.SOLUTIONS, 6: week6.Solution.SOLUTIONS,
                 7: week7.Solution.SOLUTIONS, 8: week8.Solution.SOLUTIONS, 9: week9.Solution.SOLUTIONS,
                 11: week11.Solution.SOLUTIONS}
    for sols in solutions.values():
        for sol in sols:
            assert sol.name is not None
    tasks = []
    all_tasks = [i for i in args.tasks if i[0] == 'all']
    if all_tasks:
        for week in solutions:
            for task in solutions[week]:
                tasks.append((week, task))
    else:
        for wt in args.tasks:
            if wt[1] == '*':
                for task in solutions[wt[0]]:
                    tasks.append((wt[0], task))
            else:
                candidates = [i for i in solutions[wt[0]] if i.name == wt[1]]
                assert len(candidates) == 1
                tasks.append((wt[0], candidates[0]))
    fnprovider = Base.TmpFilenameProvider if args.folder is None else (
        lambda folder: (lambda meta: Base.RealFilenameProvider(folder, meta)))(args.folder)
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
    if s == 'all':
        return s,
    res = s.split('/', 1)
    res[0] = int(res[0])
    if len(res) == 1:
        res = res[0], '*'
    return res


def main(args):
    parser = argparse.ArgumentParser(description='Run the tasks for IV122.')
    # parser.add_argument('--weeks', dest='weeks', nargs='*', metavar='W', type=week_parse,
    #                     help='The weeks to evaluate or "all"', default=[])
    parser.add_argument('--tasks', dest='tasks', nargs='*', metavar='T', type=task_parse, help='The tasks to evaluate.',
                        default=[])
    parser.add_argument('--folder', dest='folder', metavar='folder',
                        help='The path to store the results to (default creates temp files)')
    args = parser.parse_args(args[1:])
    run(args)


if __name__ == '__main__':
    main(sys.argv)
