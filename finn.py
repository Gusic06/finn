from lib.lexer import Lexer
from lib.interpreter import Interpreter
from lib.compiler import Compiler
from lib.parser import Parser
from lib.pretty_printer import PrettyPrinter

import sys
from time import time

def finn() -> None:
    filename: str = ""
    show_tokens: bool = False
    show_registers: bool = False
    show_variables: bool = False
    deconstruct: bool = False
    proc_to_deconstruct: str = ""
    time_it: bool = False
    repl: bool = False
    compile: bool = False
    interpret: bool = False
    for arg in sys.argv:

        if arg[:-4] == "-deconstruct:":
            arg = arg.split(":")
            deconstruct = True
            proc_to_deconstruct = arg[1]

        if arg == "-c":
            compile = True

        if arg == "-i":
            interpret = True

        if arg[-6:] == ".porth":
            filename = arg

        if arg == "-repl":
            repl = True

        if arg == "-reg":
            show_registers = True

        if arg == "-var":
            show_variables = True

        if arg == "-token":
            show_tokens = True

        if arg == "-time":
            time_it = True

    if repl:
        while True:
            user_input: str = input(" >> ")
            if user_input == ":q": exit(0)
            tokens, _ = Lexer(user_input, "finn-repl").scan_tokens()
            if show_tokens:
                [print(token) for token in tokens]
                continue
            Interpreter(tokens).interpret(show_registers, show_variables, deconstruct, proc_to_deconstruct)

    if filename == "":
        print("finn [filename] [mode], use \"-h\" for more information")
        exit(1)

    with open(filename, "r") as file:
        start: int = time()
        tokens, amount_lexed = Lexer(file.read(), sys.argv[1]).scan_tokens()
        print(Parser(tokens).parse())
        [PrettyPrinter().pprint(expr) for expr in Parser(tokens).parse()]
        if time_it:
            lexing_time = time() - start
        if show_tokens:
            [token.pprint() for token in tokens]
            exit(0)
    start = time()
    if interpret:
        Interpreter(tokens).interpret(show_registers, show_variables, deconstruct, proc_to_deconstruct)
    if compile:
        print(Compiler(tokens).compile())
    if time_it:
        print(f"Lexer completed lexing in {str(lexing_time)[:4]} seconds and lexed {amount_lexed - 1} tokens\nInterpreting took {str(time() - start)[:5]} seconds")

if __name__ == "__main__":
    finn()
