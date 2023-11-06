#! /bin/env python
from argparse import ArgumentParser

AQ_DICT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
        'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27,
        'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35,
}

def aq_lookup(char):
    return AQ_DICT[char] if char in AQ_DICT else 0

def cumulate(number):
    # print(' + '.join(list(str(number))))
    return sum(map(int, str(number)))

def plex(number):
    if number < 10:
        return number
    return plex(cumulate(number))
        # return plex(sum(map(int, str(number))))

def qabbalize(text):
    return sum(map(aq_lookup, text.upper()))

def main():
    parser = ArgumentParser("Calculate the AQ of some text")
    parser.add_argument('words', metavar='WORDS', type=str, nargs='+',
            help='the words to process')
    args = parser.parse_args()
    words = ' '.join(args.words)

    print(words.upper(), "=")
    print(qabbalize(words))

print(qabbalize("the sky and the cosmos are one"))

if __name__ == "__main__":
    main()
