'''CMD tool that accept file path and iterate lines,
 each line split by space and build new lines with all words in all orders.'''
from itertools import permutations
import argparse
import sys
import toml


def get_version():
    '''Get version from pyproject toml file'''
    with open('./pyproject.toml', 'r') as file:
        poetry_toml = toml.load(file)
    return poetry_toml['tool']['poetry']['version']


def reader(file_path=None):
    '''Reader function generator thats open file and iterate each line split by space
    If file path is None than ask user to input sentence split by space each iteration'''
    if file_path is None:
        while True:
            line = input('Enter line: ')
            if line == '':
                break
            yield line
    else:
        with open(file_path, 'r') as file:
            for line in file:
                yield line


def processor(lines_iterator):
    '''Processor function thats accept iterator of lines
    split each line by space and build new lines with all combinations of words'''
    for line in lines_iterator:
        words = line.split()
        for word_permutation in permutations(words):
            yield ' '.join(word_permutation)


def writer(instance, lines):
    '''Writer accepts any instance that has write method and lines as iterator
    than write all lines to the instance'''
    for line in lines:
        instance.write(line)
        instance.write('\n')
    instance.close()


def main():
    ''' Main function use argparse to get file path for input and output file
    than call reader and processor functions and writer function
    if file path is None than ask user to input sentence
    if output file is None than print all lines
    if only version path as arg that print version
    '''
    parser = argparse.ArgumentParser(
        description='CMD tool that accept file path and iterate lines, each line split by space and build new lines with all words in all orders.')
    parser.add_argument('-v', '--version', action='version',
                        version=get_version())
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    args = parser.parse_args()
    if args.input is None:
        lines = processor(reader())
    else:
        lines = processor(reader(args.input))
    if args.output is None:
        writer(sys.stdout, lines)
    else:
        with open(args.output, 'w') as file:
            writer(file, lines)


if __name__ == "__main__":
    main()
