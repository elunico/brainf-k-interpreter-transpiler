import argparse
import sys
from typing import List

Pointer = int

# 64k
data: List[int] = [0] * (2 ** 16)

dptr: Pointer = 0


def err(msg):
    print('[D] ' + str(msg), file=sys.stderr)


def getch() -> int:
    return ord(sys.stdin.read(1))


def putch(n: int) -> None:
    sys.stdout.write(chr(n))
    sys.stdout.flush()


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--maxmem', type=int, default=(2 ** 16),
                    help="Maximum number of bytes to store (kept as ints)")
    ap.add_argument('-c', '--compile', action='store_true', help='Compile to C approximation')
    gp = ap.add_mutually_exclusive_group()
    gp.add_argument('-e', '--command', help='Execute the given string as a program')
    gp.add_argument('-p', '--prompt', help='Get keyboard input and execute the program')
    gp.add_argument('-f', '--file', help='Read program data from the file and execute it')
    return ap.parse_args()


def jump_to_close(ip: int, prog: List[str]) -> int:
    walker = ip + 1  # begin looking forward
    level = 0
    while walker < len(prog):
        c = prog[walker]
        if c == '[':
            level += 1
        elif c == ']' and level == 0:
            return walker  # iptr increments each time, jump to bracket
        elif c == ']' and level > 0:
            level -= 1
        walker += 1
    raise ValueError("Invalid program! Unbalanced opening bracket at {}".format(ip))


def jump_to_open(ip: int, prog: List[str]) -> int:
    walker = ip - 1  # begin looking backwards
    level = 0
    while walker >= 0:
        c = prog[walker]
        if c == ']':
            level += 1
        elif c == '[' and level == 0:
            return walker  # iptr increments each time, jump to bracket
        elif c == '[' and level > 0:
            level -= 1
        walker -= 1
    raise ValueError("Invalid program! Unbalanced close bracket at {}".format(ip))


def execute(program: str) -> int:
    global dptr
    global data
    program = [i for i in program]
    iptr = 0
    err('Brainf**k interpreter and C transpiler!')
    err('  Append " 2>/dev/null" to your command to discard debug output')
    err('Execution began: prog length = {}'.format(len(program)))
    while iptr < len(program):
        instruction = program[iptr]
        if instruction == '>':
            dptr += 1
        elif instruction == '<':
            dptr -= 1
        elif instruction == '+':
            data[dptr] += 1
        elif instruction == '-':
            data[dptr] -= 1
        elif instruction == '.':
            putch(data[dptr])
        elif instruction == ',':
            err("$ ")
            data[dptr] = getch()
        elif instruction == '[':
            if data[dptr] == 0:
                iptr = jump_to_close(iptr, program)
        elif instruction == ']':
            if data[dptr] != 0:
                iptr = jump_to_open(iptr, program)
        else:
            # ignore any characters not used for commands
            pass
        iptr += 1
    err('Program completed.')


def inprint(indent, msg):
    print(('  ' * indent) + msg)


def cpile(program):
    global dptr
    global data
    program = [i for i in program]
    iptr = 0
    err('Brainf**k interpreter and C transpiler!')
    err('  Append " 2>/dev/null" to your command to discard debug output')
    err('Compilation began: prog length = {}'.format(len(program)))
    indent = 0
    inprint(indent, '#include <stdlib.h>')
    inprint(indent, '#include <stdio.h>')
    inprint(indent, 'int main(int argc, char const *arv[]) {')
    indent += 1
    inprint(indent, 'char p[65536] = {0};')
    inprint(indent, 'char *ptr = (char*)p;')
    while iptr < len(program):
        instruction = program[iptr]
        if instruction == '>':
            inprint(indent, 'ptr++;')
        elif instruction == '<':
            inprint(indent, 'ptr--;')
        elif instruction == '+':
            inprint(indent, '++*ptr;')
        elif instruction == '-':
            inprint(indent, '--*ptr;')
        elif instruction == '.':
            inprint(indent, 'putchar(*ptr);')
        elif instruction == ',':
            inprint(indent, '*ptr = getchar();')
        elif instruction == '[':
            inprint(indent, 'while (*ptr) {')
            indent += 1
        elif instruction == ']':
            indent -= 1
            inprint(indent, '}')
        else:
            # ignore any characters not used for commands
            pass
        iptr += 1
    inprint(indent - 1, '}')
    err('Compilation complete.')


def main():
    global data
    args = parse_args()
    if args.maxmem:
        data = [0] * int(args.maxmem)
    if args.compile:
        if args.command:
            return cpile(args.command)
        elif args.prompt:
            program = input("%: ")
            return cpile(program)
        elif args.file:
            with open(args.file) as f:
                text = f.read()
            return cpile(text)
        else:
            return cpile(input())
    else:
        if args.command:
            return execute(args.command)
        elif args.prompt:
            program = input("%: ")
            return execute(program)
        elif args.file:
            with open(args.file) as f:
                text = f.read()
            return execute(text)
        else:
            return execute(input())


if __name__ == '__main__':
    exit(main())
