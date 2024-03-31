from .tokentype import Token, TokenType
from .expr import Expr

class Parser:

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens

        self.index: int = 0
        self.stack: list[any] = []

        self.output: list[list[Token]] = []

        self.end_tolerance: int = 0
    
    def advance(self) -> Token:
        token: Token = self.tokens[self.index]
        self.index += 1
        return token
    
    def at_end(self) -> bool:
        return self.tokens[self.index]._type == TokenType.EOF

    def parse(self) -> None:
        tokens: list[Token] = []

        procs: dict[str, list[Token]] = {}
        structs: dict[str, list[Token]] = {}
        enums: dict[str, list[Token]] = {}
        macros: dict[str, list[Token]] = {}

        while not self.at_end():
            token: Token = self.advance()

            match token._type:

                case TokenType.PROC:
                    self.construct_proc()

    def construct_proc(self) -> None:
        proc_name: str = ""
        if self.tokens[self.index - 2]._type == TokenType.OBJECT_ASSIGN:
            proc_name = self.tokens[self.index - 3].value
        proc_contents: list[Token] = []
        while True:
            self.token: Token = self.advance()
            if self.token._type == TokenType.PROC:
                self.proc_buffer.append([self.proc_name, self.proc_contents])
                self.proc_contents = []
                self.proc_name = ""
                self.buffer_index += 1
                return

            if self.end_tolerance == 0 and self.token._type == TokenType.END:
                self.fall_through = False
                return

            if self.token._type != TokenType.END:
                if self.token._type == TokenType.IF:
                    self.end_tolerance += 1
            else:
                self.end_tolerance -= 1

            proc_contents.append(self.token)
            return