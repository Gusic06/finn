from .tokentype import Token, TokenType

from random import choices

CHARACTERS: str = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

class Compiler:

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens

        self.index: int = 0
        self.stack: list[any] = []

        self.data: str = "section .data\n"
        self.main_block: str = "\nsection .text\nglobal _start\n_start:\n"

        self.procs: dict[str, str] = {}
        self.strings: dict[str, str] = {}

    def at_end(self) -> bool:
        return self.tokens[self.index] == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.index]
    
    def advance(self) -> Token:
        token: Token = self.tokens[self.index]
        self.index += 1
        return token

    def compile_token(self) -> None:
        token: Token = self.advance()

        match token._type:

            case TokenType.PUSH:
                if token.value_type == TokenType.STRING:
                    self.stack.append(token.value)
                    if not (token.value in self.strings.keys()):
                        self.strings[token.value] = "".join(choices(CHARACTERS, k=30))
                        self.data += f"  {self.strings[token.value]}: db \"{token.value}\", 10\n  {self.strings[token.value]}_len: equ $-{self.strings[token.value]}\n"
                else:
                    self.main_block += f"  push {token.value}\n"

            case TokenType.PRINT:
                string_id: str = self.strings[self.stack.pop()]
                self.main_block += f"  mov eax, 4\n  mov ebx, 1\n  mov ecx, {string_id}\n  mov edx, {string_id}_len\n  int 80h\n"


    def compile(self) -> None:
        while self.peek()._type != TokenType.EOF:
            self.compile_token()
        self.main_block += "  mov eax, 1\n  mov ebx, 0\n  int 80h"
        return self.data + self.main_block