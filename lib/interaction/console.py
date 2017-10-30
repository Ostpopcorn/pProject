
def single_train_interaction(train):
    commands = {"book":book}

    target = input("select: ")

    if target in commands:
        commands[target](train)


def book(train):
    print("in booking")