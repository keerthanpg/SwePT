import random


def main():
    a = random.randint(1, 12)
    b = random.randint(1, 12)
    for i in range(10):
        question = "What is " + str(a) + " x " + str(b) + "? "
        answer = input(question)
        if answer == str(a * b):
            print("Well done!")
        else:
            print("No.")


if __name__ == "__main__":
    main()
