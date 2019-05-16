import sys

fname = "../data/test.txt"


def add(a, b):
    return a + b

with open(fname) as f:
    contents = f.readlines()
    print(contents)


def main():
    pass



if __name__=="__main__":
    main()
    sys.exit(0)
