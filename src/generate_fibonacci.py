def generate_fibonacci(length=0):
    f_list = []
    if length is not None:
        f_1 = 0
        f_2 = 1
        for x in range(length):
            f_list.append(f_2)
            f = f_1 + f_2
            f_1 = f_2
            f_2 = f
    return f_list


def print_fibonacci(length=10):
    print(generate_fibonacci(length))


if __name__ == '__main__':
    print_fibonacci(10)
