import os
import sys

RAW_DATA_DIR = '../raw-data'
sys.path.append(os.path.abspath('.'))


def get_lines_in_file():
    """ Print the number of lines in each file for import. """

    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i+1

    files = ('STOP.txt', 'PERSON.txt', 'SEARCH.txt',
             'CONTRABAND.txt', 'SEARCHBASIS.txt')
    for fn in files:
        print "{fn}: {lines} lines".format(fn=fn, lines=file_len(os.path.join(RAW_DATA_DIR, fn)))


def main():
    get_lines_in_file()


if __name__ == "__main__":
    main()


# STOP.txt:         16,822,954 lines
# PERSON.txt:       17,108,280 lines
# SEARCH.txt:       542,736 lines
# CONTRABAND.txt:   136,346 lines
# SEARCHBASIS.txt:  618,871 lines
