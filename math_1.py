def add(a,b):
    return a + b

def subtract(a,b):
    return a - b

def multiply(a,b):
    return a * b

def divide(a,b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a/b

def main():
    a=4
    b = 5
    print("Addition:", add( b, a))
    print("Subtraction:", subtract(a,b))
    print("Multiplication:", multiply(a,b))
    print("Division:", divide(a,b))

if __name__ == "__main__":
    main()
