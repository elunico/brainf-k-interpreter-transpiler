# brainf-k-interpreter-transpiler
An interpreter and C transpiler for brainf\*\*k written in python

[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) is an esoteric programming language and a popular one at that, despite its name. 
It is based around a data pointer, some number of bytes used as data, a program consisting of a sequence of any of 8 single character instructions.
brainf\*\*k programs can usually contain any other data as well but it is ignored by the interpreter (as is the case with this one). 
Any symbols that are not `< > + - , . [ ]` are simply discarded. 

This program (specifically `bfc.py`) is capable of taking a brainf\*\*k program as input (either from a file, an input prompt and stdin, or as a 
command line argument string) and interpreting it. It can also transpile the brainf\*\*k program into a very simple C program that can then 
be compiled and run using a C compiler. For information can be found using `python3 bfc.py -h` when executing the program. 

By default the program will, on start, produce no output and begin reading from stdin. 

By default the program allows access to 64 kibibytes (65536 bytes) of memory. brainf\*\*k specifies at least 30000 bytes be available to a program
but 64k was chosen as homage to the Commodore64. You can adjust this number using the `-m SIZE` flag. The program will "segfault" if you access memory out 
of bounds for either the instruction (return code 1) or data (return code 2) memory which are not the same. 

Note that C transpilation simply outputs corresponding C commands to stdout and therefore does not check memory bounds or indeed perform any checks
on the validity or syntactic correctness of the program. It will do its best to literally translate all of the brainf\*\*k it sees into C code 
regardless of whether it will function in brainf\*\*k or not.
