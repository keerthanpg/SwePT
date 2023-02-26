import random


def main():
    for i in range(10):
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        question = "What is " + str(a) + " x " + str(b) + "? "
        answer = int(input(question))
        if answer == a * b:
            print("Well done!")
        else:
            print("No.")


if __name__ == "__main__":
    main()
