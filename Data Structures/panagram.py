import string


def is_panagram(s):
    alphabet = set(string.ascii_lowercase)
    if set(s.lower()) >= alphabet:
        return 1
    else:
        return 0

is_panagram("Thequickbrownfoxjumpsoverthelazydog")