
def func1():
    print(f"Global Value: ${_rows}")


if __name__ == "__main__":
    global _rows

    _rows = 2
    func1()
