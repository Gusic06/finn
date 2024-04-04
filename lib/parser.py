from .tokentype import Token, TokenType
from .expr import (
    PUSH, CALL, PRINT, BINOP, COMP, 
    OP, IF, THEN, ELSE, VARIABLE, 
    VARIABLE_DECL, PROC, ARGS, ARG, 
    NAME, BLOCK, INCLUDE, STRUCT, ENUM, 
    MEMBER, AND, OR, NOT, EXIT, IMPL,
    OBJECT, RETURN, Expr
)

class Parser:

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens

        self.index: int = 0
        self.stack: list[any] = []

        self.statements: list[list[Token]] = []
    
    def advance(self) -> Token:
        token: Token = self.tokens[self.index]
        self.index += 1
        return token
    
    def report_error(self, message: str) -> None:
        print(f"{self.peek().filename}:{self.peek().position[0]}:{self.peek().position[1]}: {message}")
        exit(1)
    
    def peek(self) -> Token:
        return self.tokens[self.index]
    
    def previous(self) -> Token:
        return self.tokens[self.index - 1]
    
    def at_end(self) -> bool:
        return self.tokens[self.index]._type == TokenType.EOF
    
    def parse_identifier(self) -> Expr:
        fall_through: bool = True
        statements = []
        self.index -= 1 # stupid hack

        while fall_through and not self.at_end():
            token: Token = self.advance()

            match token._type:

                case TokenType.PUSH:
                    statements.append(PUSH(token))

                case TokenType.DOT:
                    if len(statements) == 0:
                        self.report_error("todo")
    
                    root = statements.pop()
                    member = self.advance()

                    statements.append(MEMBER(root, PUSH(member)))

                case TokenType.L_PAREN:
                    function_name = statements.pop()
                    args = self.capture_args()
                    statements.append(CALL(function_name, ARGS(args)))

                case _:
                    fall_through = False
        
        return statements.pop()

    def capture_args(self) -> None:
        args = []
        while self.peek()._type != TokenType.R_PAREN and not self.at_end():
            token: Token = self.advance()

            match token._type:

                case TokenType.L_PAREN:
                    proc = args.pop()
                    args.append(CALL(proc, ARGS(self.capture_args())))

                case TokenType.PUSH:
                    args.append(PUSH(token))

                case TokenType.PLUS | TokenType.MINUS | TokenType.STAR | TokenType.SLASH:
                    expr_1 = args.pop()
                    expr_2 = args.pop()

                    args.append(BINOP(expr_2, expr_1, OP(token)))

                case TokenType.EQUAL_EQUAL | TokenType.BANG_EQUALS | TokenType.GT | TokenType.GT_EQUALS | TokenType.LT | TokenType.LT_EQUALS:
                    expr_1 = args.pop()
                    expr_2 = args.pop()

                    args.append(COMP(expr_2, expr_1, OP(token)))

        return args

    def construct_if_block(self) -> None:
        conditional = self.statements.pop()
        fall_through: bool = True
        branch_table: dict[str, list] = {"then" : [], "else" : []}
        current_branch = "then"

        while fall_through and not self.at_end():
            
            branch_table[current_branch] = self.parse_token(branch_table[current_branch])

            match self.previous()._type:
                    
                case TokenType.ELSE:
                    current_branch = "else"
                
                case TokenType.END:
                    fall_through = False

        return IF(conditional, THEN(branch_table["then"]), ELSE(branch_table["else"]))

    def construct_proc(self) -> None:
        contents = []
        fall_through: bool = True

        while fall_through and not self.at_end():
            contents = self.parse_token(contents)

            match self.peek()._type:

                case TokenType.HASH:
                    arg_num = contents.pop()
                    contents.append(ARG(arg_num))

                case TokenType.RETURN:
                    contents.append(RETURN(contents.pop()))

                case TokenType.END:
                    fall_through = False
        
        return contents

    def construct_enum(self) -> None:
        ...

    def construct_struct(self) -> None:
        type_table = {}
        fall_through: bool = True

        while fall_through and not self.at_end():
            token: Token = self.advance()

            match token._type:

                case TokenType.COLON:
                    data_type = self.tokens[self.index]
                    name = self.tokens[self.index - 2]

                    match data_type._type:

                        case TokenType.PROC:
                            data_type = PROC(self.tokens[self.index - 2], self.construct_proc())

                        case TokenType.STRUCT:
                            data_type = STRUCT(self.tokens[self.index - 2], self.construct_struct())

                    type_table[name.value] = data_type
                
                case TokenType.NEWLINE:
                    pass

                case TokenType.END:
                    fall_through = False

                case _:
                    if token._type not in [TokenType.PUSH, TokenType.COLON, TokenType.INT, TokenType.STRING, TokenType.BOOL, TokenType.PROC, TokenType.STRUCT, TokenType.NEWLINE]:
                        print(f"{token.filename}:{token.position[0]}:{token.position[1]}: Invalid struct syntax, found \"{token._type}\" inside struct definition")
                        exit(1)

        return type_table

    def construct_impl(self) -> IMPL:
        procs: list[PROC] = []
        stack: list[Expr] = []
        fall_through: bool = True
        name: PUSH = self.statements.pop()
        while fall_through and not self.at_end():
            token: Token = self.advance()

            match token._type:

                case TokenType.PUSH:
                    stack.append(PUSH(token))
                
                case TokenType.END:
                    fall_through = False

                case TokenType.OBJECT_ASSIGN:
                    if self.advance()._type == TokenType.PROC:
                        procs.append(PROC(NAME(stack.pop()), BLOCK(self.construct_proc())))
                        self.advance()
                    else:
                        self.report_error("Cannot have anything but a proc definition inside of an impl block")
        
        return IMPL(NAME(name), *procs)

    def construct_object(self) -> Expr:
        name: PUSH = self.statements.pop()
        token: Token = self.advance()

        match token._type:

            case TokenType.PROC:
                return PROC(NAME(name), BLOCK(self.construct_proc()))

            case TokenType.STRUCT:
                return STRUCT(NAME(name), self.construct_struct())
            
            case TokenType.ENUM:
                return ENUM(NAME(name), self.construct_enum())

            case TokenType.IMPL:
                self.statements.append(name)
                return self.construct_impl()
            
            case TokenType.PUSH:
                if token.value_type == TokenType.IDENTIFIER:
                    return OBJECT(NAME(name), NAME(self.parse_identifier()))

    def parse_token(self, statements) -> None:
        token: Token = self.advance()
        match token._type:

            case TokenType.EXIT:
                if len(statements) >= 1:
                    exit_code = statements.pop()
                    statements.append(EXIT(exit_code))
                else:
                    statements.append(EXIT())

            case TokenType.INCLUDE:
                name: Token = self.advance()
                statements.append(INCLUDE(PUSH(name)))

            case TokenType.L_PAREN:
                function: Token = statements.pop()
                args = self.capture_args()
                statements.append(CALL(function, ARGS(args)))
                
            case TokenType.OR:
                expr_1 = statements.pop()
                expr_2 = statements.pop()
                statements.append(OR(expr_2, expr_1))

            case TokenType.AND:
                expr_1 = statements.pop()
                expr_2 = statements.pop()
                statements.append(AND(expr_2, expr_1))

            case TokenType.GRAB_OBJECT:
                ...

            case TokenType.DOT:
                if len(statements) == 0:
                    self.report_error("todo")

                root = statements.pop()
                member = self.advance()

                statements.append(MEMBER(root, PUSH(member)))

            case TokenType.OBJECT_ASSIGN:
                self.statements.append(statements.pop())
                statements.append(self.construct_object())

            case TokenType.PROC:
                body = self.construct_proc()
                statements.append(PROC(None, BLOCK(body)))

            case TokenType.DUP:
                expr = statements.pop()
                statements.append(expr)
                statements.append(expr)

            case TokenType.IF:
                self.statements.append(statements.pop())
                statements.append(self.construct_if_block())

            case TokenType.PUSH:
                statements.append(PUSH(token))

            case TokenType.EQUAL:
                contents: Token = statements.pop()
                name: Token = statements.pop()
                statements.append(VARIABLE_DECL(name, contents))

            case TokenType.PLUS | TokenType.MINUS | TokenType.STAR | TokenType.SLASH:
                expr_1 = statements.pop()
                expr_2 = statements.pop()
                statements.append(BINOP(expr_2, expr_1, OP(token)))

            case TokenType.EQUAL_EQUAL | TokenType.BANG_EQUALS | TokenType.GT | TokenType.GT_EQUALS | TokenType.LT | TokenType.LT_EQUALS:
                expr_1 = statements.pop()
                expr_2 = statements.pop()
                statements.append(COMP(expr_2, expr_1, OP(token)))

            case TokenType.PRINT:
                expr = statements.pop()
                statements.append(PRINT(expr))

            case TokenType.CALL_VAR:
                expr = statements.pop()
                statements.append(VARIABLE(expr))
        
        return statements

    def parse(self) -> None:
        while not self.at_end():
            self.statements = self.parse_token(self.statements)
        self.statements.append(EXIT())
        return self.statements
