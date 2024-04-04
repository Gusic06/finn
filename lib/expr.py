from .tokentype import Token, TokenType

class Expr:...

class MEMBER(Expr):

    def __init__(self, root: Expr, member: Token) -> None:
        self.root: Expr = root
        self.member: Token = member

    def visit(self) -> Token:
        return self.root, self.member
    
class RETURN(Expr):

    def __init__(self, expr: Expr) -> None:
        self.expr: Expr = expr

    def visit(self) -> Expr:
        return self.expr
    
class IMPL(Expr):

    def __init__(self, name: Expr, *procs: list[Expr]) -> None:
        self.name: Expr = name
        self.procs: list[Expr] = procs

    def visit(self) -> any:
        return self.name, *self.procs

class ARGS(Expr):

    def __init__(self, args: list) -> None:
        self.args = args

    def visit(self) -> None:
        return self.args
    
class ARG(Expr):

    def __init__(self, arg: Expr) -> None:
        self.arg = arg

    def visit(self) -> None:
        return self.arg
    


class OBJECT(Expr):

    def __init__(self, name: Token, object_name: Token) -> None:
        self.name: Token = name
        self.object_name: Token = object_name

    def visit(self) -> Token:
        return self.name, self.object_name

class AND(Expr):

    def __init__(self, expr_1, expr_2) -> None:
        self.expr_1 = expr_1
        self.expr_2 = expr_2

    def visit(self) -> None:
        return self.expr_1, self.expr_2
    
class OR(Expr):

    def __init__(self, expr_1, expr_2) -> None:
        self.expr_1 = expr_1
        self.expr_2 = expr_2

    def visit(self) -> None:
        return self.expr_1, self.expr_2

class NOT(Expr):

    def __init__(self, expr) -> None:
        self.expr = expr

    def visit(self) -> None:
        return self.expr

class INCLUDE(Expr):

    def __init__(self, name) -> None:
        self.name = name

    def accept(self, visitor) -> None:
        return visitor.visit_include_expr(self)

    def visit(self) -> None:
        return self.name

class ENUM(Expr):

    def __init__(self, name, body) -> None:
        self.name = name
        self.body = body

    def accept(self, visitor) -> None:
        return visitor.visit_enum_expr(self)

class STRUCT(Expr):

    def __init__(self, name, body) -> None:
        self.name = name
        self.body = body

    def accept(self, visitor) -> None:
        return visitor.visit_struct_expr(self)
    
    def visit(self) -> None:
        return self.name, self.body

class PUSH(Expr):

    def __init__(self, value: Token) -> None:
        self.value: Token = value

    def accept(self, visitor) -> None:
        return visitor.visit_push_expr(self)

    def visit(self) -> Token:
        return self.value

class NAME(Expr):

    def __init__(self, name: Token) -> None:
        self.name: Token = name

    def accept(self, visitor) -> None:
        return visitor.visit_name_expr(self)

    def visit(self) -> Token:
        return self.name
    
class PROC(Expr):

    def __init__(self, name: NAME|None, contents) -> None:
        self.name: NAME|None = name
        self.contents = contents

    def accept(self, visitor) -> None:
        return visitor.visit_proc_expr(self)

    def visit(self) -> None:
        return self.name, self.contents
    
class BLOCK(Expr):

    def __init__(self, body) -> None:
        self.body = body

    def accept(self, visitor) -> None:
        return visitor.visit_block_expr(self)

    def visit(self) -> None:
        return self.body
    
class THEN(Expr):

    def __init__(self, body: list) -> None:
        self.body: list = body

    def visit(self) -> list:
        return self.body

class ELSE(Expr):

    def __init__(self, body: list) -> None:
        self.body: list = body

    def visit(self) -> list:
        return self.body
    
class IF(Expr):

    def __init__(self, conditional, then_branch, else_branch) -> None:
        self.conditional = conditional
        self.then_branch = then_branch
        self.else_branch = else_branch

    def visit(self) -> any: # who fucking knows
        return self.conditional, self.then_branch, self.else_branch
    
class OP(Expr):

    def __init__(self, operand: Token) -> None:
        self.operand: Token = operand

    def visit(self) -> Token:
        return self.operand
    
class COMP(Expr):

    def __init__(self, expr_1, expr_2, operand: Token) -> None:
        self.expr_1 = expr_1
        self.expr_2 = expr_2
        self.operand: Token = operand

    def visit(self) -> None:
        return self.expr_1, self.expr_2, self.operand

class BINOP(Expr):

    def __init__(self, expr_1, expr_2, operand: str) -> None:
        self.expr_1: PUSH|BINOP = expr_1
        self.expr_2: PUSH|BINOP = expr_2
        self.operand: str = operand

    def __repr__(self) -> str:
        return f"{self.expr_1} {self.operand} {self.expr_2}"

    def visit(self) -> list[PUSH]:
        return self.expr_1, self.expr_2, self.operand

class CALL(Expr):

    def __init__(self, proc: list[Token], args: list[any]) -> None:
        self.proc: list[Token] = proc
        self.args: list[any] = args

    def visit(self) -> None:
        return self.proc, self.args

class PRINT(Expr):

    def __init__(self, expr: any) -> None:
        self.expr: any = expr

    def visit(self) -> any:
        return self.expr
    
class VARIABLE_DECL(Expr):

    def __init__(self, name: Token, value: Token) -> None:
        self.name: Token = name
        self.value: Token = value

    def visit(self) -> None:
        return self.name, self.value

class VARIABLE(Expr):

    def __init__(self, name: str) -> None:
        self.name: str = name

    def visit(self) -> str:
        return self.name
    
class EXIT(Expr):

    def __init__(self, exit_code: Expr = PUSH(Token(TokenType.PUSH, 0, TokenType.INT, (-1, -1), ""))) -> None:
        self.exit_code: Expr = exit_code

    def visit(self) -> Expr:
        return self.exit_code
