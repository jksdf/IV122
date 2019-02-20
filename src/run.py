import sys

import src.Base
import src.week1.Solution


def main(args):
    solutions = {1: src.week1.Solution.SOLUTIONS}
    for week in solutions:
        for task in solutions[week]:
            try:
                res = task.run(src.Base.TmpFilenameProvider())
            except Exception as e:
                res = 'The task has raised a {} exception'.format(e)
            print('Week {} Part {}: {}'.format(week, task.name(), res))


if __name__ == '__main__':
    main(sys.argv)
