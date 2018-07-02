import argparse
import selection_utils

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', nargs = '+', help = "The id of course, e.g., CSC240")
    parser.add_argument('-c', '--campus', required = True, help = "The campus you belong to")
    parser.add_argument('-t', '--term', required = True, help = "The term you want to schedule for")
    args = parser.parse_args()

    print(args.id, args.campus)


