from .tokentype import Token, TokenType

class Lexer:

    def __init__(self, source: str, filename: str) -> None:

        self.path = __file__.split("lexer.py")
        self.source = source
        self.filename = filename

        self.line = 1
        self.line_index = 0
        self.start = 0
        self.current_index = 0

        self.tokens_created: int = 0

        self.output = []


    def at_end(self) -> bool:
        return self.current_index >= len(self.source)
      
    def advance(self) -> str:
        self.return_value = self.source[self.current_index]
        self.current_index += 1
        return self.return_value

    def create_token(self, _type: TokenType, value: any, value_type: TokenType) -> None:
        self.tokens_created += 1
        self.output.append(Token(_type, value, value_type, (self.line, self.line_index), self.filename))

    def error(self, message: str, fatal: bool = False) -> None:
        print(f"{self.filename}:{self.line}:{self.line_index}: {message}")
        if fatal:
            exit(1)
    
    def scan_token(self) -> None:
        self.character = self.advance()
        self.line_index += 1
        match self.character:

            case "[" | "]":
                ...

            case "(":
                self.create_token(TokenType.L_PAREN, None, TokenType.OPERAND)

            case ")":
                self.create_token(TokenType.R_PAREN, None, TokenType.OPERAND)

            case "{":
                self.create_token(TokenType.L_BRACE, None, TokenType.OPERAND)
            
            case "}":
                self.create_token(TokenType.R_BRACE, None, TokenType.OPERAND)

            case ",":
                self.create_token(TokenType.COMMA, None, TokenType.OPERAND)

            case ".":
                if self.match("."):
                    if self.match("."):
                        self.create_token(TokenType.GRAB_OBJECT, None, TokenType.OPERAND)
                    else:
                        ...
                else:
                    self.create_token(TokenType.DOT, None, TokenType.OPERAND)

            case ":":
                if self.match(":"):
                    self.create_token(TokenType.OBJECT_ASSIGN, None, TokenType.OPERAND)
                else:
                    self.create_token(TokenType.COLON, ":", TokenType.OPERAND)

            case "#":
                self.create_token(TokenType.HASH, None, TokenType.OPERAND)

            case "|":
                if self.match(">"):
                    self.create_token(TokenType.R_BIND, None, TokenType.OPERAND)
                else:
                    self.create_token(TokenType.PIPE, None, TokenType.OPERAND)

            case "-":
                if self.is_digit(self.peek()):
                    self.number(negative=True)
                elif self.match("="):
                    self.create_token(TokenType.MINUS_EQUALS, None, TokenType.OPERAND)
                elif self.match("-"):
                    self.create_token(TokenType.MINUS_MINUS, None, TokenType.OPERAND)
                elif self.match(">"):
                    self.create_token(TokenType.ARROW, None, TokenType.OPERAND)
                else:
                    self.create_token(TokenType.MINUS, "-", TokenType.OPERAND)

            case "+":
                if self.match("="):
                    self.create_token(TokenType.PLUS_EQUALS, None, TokenType.OPERAND)
                elif self.match("+"):
                    self.create_token(TokenType.PLUS_PLUS, None, TokenType.OPERAND)
                else:
                    self.create_token(TokenType.PLUS, "+", TokenType.OPERAND)

            case "*":
                if self.match("="):
                    self.create_token(TokenType.STAR_EQUALS, None, TokenType.OPERAND)
                elif self.match("*"):
                    self.create_token(TokenType.STAR_STAR, None, TokenType.OPERAND)
                else:
                    self.create_token(TokenType.STAR, "*", TokenType.OPERAND)
            
            case "!":
                if self.match("=") is True:
                    self.create_token(TokenType.BANG_EQUALS, None, TokenType.OPERAND)
                else:
                    self.create_token(TokenType.CALL_VAR, None, TokenType.OPERAND)

            case "=":
                if self.match("=") is True:
                    self.create_token(TokenType.EQUAL_EQUAL, "==", TokenType.OPERAND)
                else:
                    self.create_token(TokenType.EQUAL, "=", TokenType.OPERAND)

            case "<":
                if self.match("=") is True:
                    self.create_token(TokenType.LT_EQUALS, "<=", TokenType.OPERAND)
                elif self.match("|"):
                    self.create_token(TokenType.L_BIND, None, TokenType.OPERAND)
                else:
                    self.create_token(TokenType.LT, "<", TokenType.OPERAND)

            case ">":
                if self.match("=") is True:
                    self.create_token(TokenType.GT_EQUALS, ">=", TokenType.OPERAND)
                else:
                    self.create_token(TokenType.GT, ">", TokenType.OPERAND)

            case "/":
                if self.match("="):
                    self.create_token(TokenType.SLASH_EQUALS, "/=", TokenType.OPERAND)
                elif self.match("/"):
                    while (self.peek() != "\n" and not self.at_end()):
                        self.advance()
                else:
                    self.create_token(TokenType.SLASH, "/", TokenType.OPERAND)

            case "&":
                self.create_token(TokenType.ADDRESS, None, TokenType.OPERAND)

            case '"':
                self.string()

            case " ":
                pass

            case "\r":
                pass

            case "\t":
                pass

            case "\n":
                self.line += 1
                self.line_index = 0
                self.create_token(TokenType.NEWLINE, "", TokenType.OPERAND)

            case _:
                if self.is_digit(self.character):
                    self.number()
                if self.is_alpha(self.character):
                    self.identifier()
                if not self.is_alpha(self.character) and not self.is_digit(self.character):
                    self.error(f"Unexpected character \"{self.character}\"")

        
    def number(self, negative: bool = False) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        is_float: bool = False

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()
            
            is_float = True

        if is_float:
            number = float(self.source[self.start:self.current_index])
        else:
            number = int(self.source[self.start:self.current_index])
        
        if negative:
            self.create_token(TokenType.PUSH, -abs(number), TokenType.NUMBER)
        else:
            self.create_token(TokenType.PUSH, number, TokenType.NUMBER)


    def identifier(self) -> None:
        while self.is_alphanumeric(self.peek()):
            self.advance()
        self.text = self.source[self.start:self.current_index]
        match self.text:

            case "return":
                self.create_token(TokenType.RETURN, self.text, TokenType.INTRINSIC)

            case "and":
                self.create_token(TokenType.AND, self.text, TokenType.INTRINSIC)

            case "or":
                self.create_token(TokenType.OR, self.text, TokenType.INTRINSIC)

            case "not":
                self.create_token(TokenType.NOT, self.text, TokenType.INTRINSIC)

            case "str":
                self.create_token(TokenType.STRING, self.text, TokenType.INTRINSIC)

            case "exit":
                self.create_token(TokenType.EXIT, self.text, TokenType.INTRINSIC)

            case "include":
                self.create_token(TokenType.INCLUDE, self.text, TokenType.INTRINSIC)

            case "if":
                self.create_token(TokenType.IF, self.text, TokenType.INTRINSIC)
            
            case "else":
                self.create_token(TokenType.ELSE, self.text, TokenType.INTRINSIC)

            case "end":
                self.create_token(TokenType.END, self.text, TokenType.INTRINSIC)

            case "impl":
                self.create_token(TokenType.IMPL, self.text, TokenType.INTRINSIC)

            case "proc":
                self.create_token(TokenType.PROC, self.text, TokenType.INTRINSIC)

            case "struct":
                self.create_token(TokenType.STRUCT, self.text, TokenType.INTRINSIC)

            case "macro":
                self.create_token(TokenType.MACRO, self.text, TokenType.INTRINSIC)

            case "enum":
                self.create_token(TokenType.ENUM, self.text, TokenType.INTRINSIC)

            case "print":
                self.create_token(TokenType.PRINT, self.text, TokenType.INTRINSIC)

            case "dup":
                self.create_token(TokenType.DUP, self.text, TokenType.INTRINSIC)

            case "sizeof":
                self.create_token(TokenType.SIZEOF, self.text, TokenType.INTRINSIC)

            case "int":
                self.create_token(TokenType.INT, self.text, TokenType.INTRINSIC)

            case "call":
                self.create_token(TokenType.CALL, self.text, TokenType.INTRINSIC)

            case "call-like":
                self.create_token(TokenType.CALL_LIKE, self.text, TokenType.INTRINSIC)

            case "syscall":
                self.create_token(TokenType.SYSCALL, self.text, TokenType.INTRINSIC)

            case "drop":
                self.create_token(TokenType.DROP, self.text, TokenType.INTRINSIC)

            case "swap":
                self.create_token(TokenType.SWAP, self.text, TokenType.INTRINSIC)

            case "true":
                self.create_token(TokenType.TRUE, None, TokenType.BOOL)
            
            case "false":
                self.create_token(TokenType.FALSE, None, TokenType.BOOL)

            case _:
                self.create_token(TokenType.PUSH, self.text, TokenType.IDENTIFIER)

    def is_alphanumeric(self, character: str) -> bool:
        return self.is_alpha(character) or self.is_digit(character)

    def is_alpha(self, character: str) -> bool:
        return (character >= "a" and character <= "z") or (character >= "A" and character <= "Z") or character == "_"

    def is_digit(self, character: str) -> bool:
        try:
            character = int(character)
            return True
        except Exception:
            return False

    def string(self) -> None:
        while self.peek() != '"' and not self.at_end():
            if self.peek() == "\n":
                self.line += 1
                self.line_index = 0
            self.advance()
        
        if self.at_end():
            self.error("Unterminated string", fatal=True)
        
        self.advance()

        text: str = self.source[self.start + 1 : self.current_index - 1]
        if "\\n" in text:
            print("guh")
        text.replace("\\n", "\n")
        text.replace("\\0", "\0")
        self.line_index += 1 # accounting for ending quotation
        self.create_token(TokenType.PUSH, text, TokenType.STRING)
            
    def peek_next(self) -> str:
        if self.current_index >= len(self.source):
            return "\0"
        else:
            return self.source[self.current_index + 1]

    def peek(self) -> str:
        if self.at_end():
            return "\0"
        else:
            return self.source[self.current_index]

    def match(self, expected: str) -> bool:
        if self.at_end() or self.source[self.current_index] != expected:
            return False
        else:
            self.current_index += 1
            return True

    def scan_tokens(self) -> None:
        while not self.at_end():
            self.start = self.current_index
            self.scan_token()
        self.create_token(TokenType.EOF, None, TokenType.OPERAND)
        return self.output, self.tokens_created
