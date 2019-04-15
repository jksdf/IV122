from Base import Base, AbstractFilenameProvider


class PartB(Base):
    name = 'A'
    import sys
    from collections import Counter
    from pprint import pprint

    def main(args):
        x = open(args[2])
        print(args[2])
        vals = tuple(map(int, filter(None, x.read().split())))
        c = Counter()
        ln = int(args[1])
        for idx in range(len(vals) - ln):
            c[vals[idx:idx + ln]] += 1
        pprint(c)

    if __name__ == '__main__':
        main(sys.argv)

    def run(self, fnprovider: AbstractFilenameProvider):
        pass
