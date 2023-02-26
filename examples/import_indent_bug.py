import random


def main():
    a = random.randint(1, 12)
    b = random.randint(1, 12)
    for i in range(10):
        question = "What is " + str(a) + " x " + str(b) + "? "
        answer = input(question)
        if int(answer) == a * b:
            print("Well done!")
        else:
            print("No.")


main()
