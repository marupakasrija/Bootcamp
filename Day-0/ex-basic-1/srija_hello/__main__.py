import sys
from srija_hello import say_hello

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "world"
    print(say_hello(name))

if __name__ == "__main__":
    main()
