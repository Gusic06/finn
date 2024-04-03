from .expr import PUSH, BINOP, COMP, CALL, VARIABLE, PRINT, OP, IF, THEN, ELSE, VARIABLE_DECL, PROC, NAME, BLOCK, INCLUDE, STRUCT, AND, OR, NOT, EXIT, MEMBER, ARGS, ARG, RETURN, OBJECT
from .tokentype import Token


class PrettyPrinter:

    def __init__(self) -> None:
        self.tree: str = ""
        self.indent: int = 0

    def construct_tree(self, expr) -> None:
        if isinstance(expr, PRINT):
            self.tree += f"{' ' * self.indent}PRINT(\n"
            self.indent += 2
            self.construct_tree(expr.visit())
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, OBJECT):
            self.tree += f"{' ' * self.indent}OBJECT(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, ARG):
            self.tree += f"{' ' * self.indent}ARG(\n"
            self.indent += 2
            self.construct_tree(expr.visit())
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, RETURN):
            self.tree += f"{' ' * self.indent}RETURN(\n"
            self.indent += 2
            self.construct_tree(expr.visit())
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, STRUCT):
            self.tree += f"{' ' * self.indent}STRUCT(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"       
            
        elif isinstance(expr, PROC):
            self.tree += f"{' ' * self.indent}PROC(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, CALL):
            self.tree += f"{' ' * self.indent}CALL(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"
    
        elif isinstance(expr, ARGS):
            self.tree += f"{' ' * self.indent}ARGS(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"
            
        elif isinstance(expr, MEMBER):
            self.tree += f"{' ' * self.indent}MEMBER(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"    

        elif isinstance(expr, NAME):
            self.tree += f"{' ' * self.indent}NAME(\n"
            self.indent += 2
            self.construct_tree(expr.visit())
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, INCLUDE):
            self.tree += f"{' ' * self.indent}INCLUDE(\n"
            self.indent += 2
            self.construct_tree(expr.visit())
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, BLOCK):
            self.tree += f"{' ' * self.indent}BLOCK(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"                        

        elif isinstance(expr, EXIT):
            self.tree += f"{' ' * self.indent}EXIT(\n"
            self.indent += 2
            self.construct_tree(expr.visit())
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, VARIABLE):
            self.tree += f"{' ' * self.indent}VARIABLE(\n"
            self.indent += 2
            self.construct_tree(expr.visit())
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, VARIABLE_DECL):
            self.tree += f"{' ' * self.indent}VARIABLE_DECL(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, COMP):
            self.tree += f"{' ' * self.indent}COMP(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, IF):
            self.tree += f"{' ' * self.indent}IF(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, THEN):
            self.tree += f"{' ' * self.indent}THEN(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, ELSE):
            self.tree += f"{' ' * self.indent}ELSE(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, OR):
            self.tree += f"{' ' * self.indent}OR(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"
        
        elif isinstance(expr, AND):
            self.tree += f"{' ' * self.indent}AND(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, BINOP):
            self.tree += f"{' ' * self.indent}BINOP(\n"
            self.indent += 2
            [self.construct_tree(expr) for expr in expr.visit()]
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, OP):
            self.tree += f"{' ' * self.indent}OP("
            self.construct_tree(expr.visit())
            self.tree += f")\n"

        

        elif isinstance(expr, PUSH):
            self.tree += f"{' ' * self.indent}PUSH("
            self.construct_tree(expr.visit())
            self.tree += f")\n"

        elif isinstance(expr, dict):
            self.tree += f"{' ' * self.indent}TABLE(\n"
            self.indent += 2
            for key in expr.keys():
                self.tree += f"{' '* self.indent}{key} : "
                self.construct_tree(expr[key])
                self.tree += "\n"
            self.indent -= 2
            self.tree += f"{' ' * self.indent})\n"

        elif isinstance(expr, Token):
            self.tree += f"{expr.value}"

    def pprint(self, expr) -> None:
        self.construct_tree(expr)
        print(self.tree)