def re(i, l=[]):
    l.append(i)
    if i == 3:
        return l
    return re(i - 1, l)


def main():
    print(re(11))


if __name__ == '__main__':
    main()

