import errno
import os
import random

_BASE_DIRECTORY = "files"


def _get_file_name(i_file):
    return os.path.join(_BASE_DIRECTORY, "%d" % i_file)


def mod7_file(i_file, open_fn=open):
    contents = []

    for i in range(1, i_file):
        with open_fn(_get_file_name(i), 'r') as f:
            contents.append(f.read())

    return "\n".join(contents)


def mod5_file(i_file):
    return "This is every 5th file!"


def random_file(i_file):
    n_characters = random.randint(1, 65)
    characters = [chr(random.randint(32, 127)) for i in range(n_characters)]

    line = "".join(characters)
    return line


def evaluate_rules(i_file):
    if i_file % 7 == 0:
        return mod7_file(i_file)
    elif i_file % 5 == 0:
        return mod5_file(i_file)
    else:
        return random_file(i_file)


if __name__ == "__main__":
    if not os.path.exists(_BASE_DIRECTORY):
        os.mkdir(_BASE_DIRECTORY)

    if not os.path.isdir(_BASE_DIRECTORY):
        raise OSError(errno.ENOTDIR, "Not a directory", _BASE_DIRECTORY)

    for i in range(1, 101):
        with open(_get_file_name(i), 'w') as f:
            contents = evaluate_rules(i)
            f.write(contents)
