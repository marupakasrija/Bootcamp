import argparse

def main():
    parser = argparse.ArgumentParser(description="A simple CLI tool from mypkg")
    parser.add_argument("name", help="The name to greet")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()