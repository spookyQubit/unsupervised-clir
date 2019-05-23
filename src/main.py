import sys

fname = "../Data/wikiclir2018/README.txt"


def add(a, b):
    return a + b

with open(fname) as f:
    contents = f.readlines()
    print(contents)


def main():
    with open(fname) as f:
        contents = f.readlines()
        print(contents)



if __name__=="__main__":
    main()
    sys.exit(0)
