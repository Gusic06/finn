from enum import Enum
from typing import Any

class TokenType(Enum):

    PUSH = "PUSH"

    L_PAREN = "L_PAREN"
    R_PAREN = "R_PAREN"

    L_BRACE = "L_BRACE"
    R_BRACE = "R_BRACE"

    L_BIND = "L_BIND"
    R_BIND = "R_BIND"

    PLUS = "PLUS"
    PLUS_PLUS = "PLUS_PLUS"
    PLUS_EQUALS = "PLUS_EQUALS"

    MINUS = "MINUS"
    MINUS_MINUS = "MINUS_MINUS"
    MINUS_EQUALS = "MINUS_EQUALS"

    STAR = "STAR"
    STAR_STAR = "STAR_STAR"
    STAR_EQUALS = "STAR_EQUALS"

    SLASH = "SLASH"
    SLASH_EQUALS = "SLASH_EQUALS"

    GT = "GT"
    GT_EQUALS = "GT_EQUALS"

    LT = "LT"
    LT_EQUALS = "LT_EQUALS"

    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"

    BANG = "BANG"
    BANG_EQUALS = "BANG_EQUALS"

    OBJECT_ASSIGN = "OBJECT_ASSIGN"
    GRAB_OBJECT = "GRAB_OBJECT"

    TRUE = "TRUE"
    FALSE = "FALSE"

    PIPE = "PIPE"
    COMMA = "COMMA"
    DOT = "DOT"
    HASH = "HASH"
    ADDRESS = "ADDRESS"
    ARROW = "ARROW"

    MACRO = "MACRO"

    EXIT = "EXIT"
    IF = "IF"
    ELSE = "ELSE"
    END = "END"
    PASS = "PASS"
    INCLUDE = "INCLUDE"
    PROC = "PROC"
    IN = "IN"
    STRUCT = "STRUCT"
    CALL_STRUCT = "CALL_STRUCT"
    PRINT = "PRINT"
    DUP = "DUP"
    SYSCALL = "SYSCALL"
    CALL = "CALL"
    CALL_VAR = "CALL_VAR"
    CALL_LIKE = "CALL_LIKE"
    DEREF = "DEREF"
    CAST = "CAST"
    PTR = "PTR"
    CAST_PTR = "CAST_PTR"
    INT = "INT"
    BOOL = "BOOL"
    SIZEOF = "SIZEOF"
    DROP = "DROP"
    SWAP = "SWAP"
    REG = "REG"

    OPERAND = "OPERAND"
    INTRINSIC = "INTRINSIC"
    STRING = "STRING"
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    EOF = "EOF"

class Token:

    def __init__(self, _type: TokenType, value: Any, value_type: TokenType, position: tuple[int, int], filename: str) -> None:
        self._type = _type
        self.value = value
        self.value_type = value_type
        self.position = position
        self.filename = filename

    def pprint(self):
        padding_1 = 11 - len((str(self._type)))
        padding_2 = 3 - len(str(self._type))

        print(f"{' ' * padding_2}({self._type}) {self._type}{' ' * padding_1} │ Contents: {self.value}{' ' * (15 - len(str(self.value)))} │ Type: {self.value_type}")
