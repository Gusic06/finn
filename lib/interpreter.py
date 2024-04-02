from typing import Any, Dict, List, Literal, Tuple, Type, Union

from .tokentype import Token, TokenType
from .vm import VM

class Interpreter:

    def __init__(self, tokens: List[Token]) -> None:
        self.vm: VM = VM()
        self.tokens: List[Token] = tokens
        self.stack: list = []
        self.call_stack: List[str] = []

        self.variables: Dict[str, Any] = {}

        self.index: int = 0
        self.end_tolerance: int = 0

        self.conditional: bool = False
        self.fall_through: bool = False

        self.found_if: bool = False

        self.in_proc: bool = False
        self.proc_name: str = ""
        self.proc_contents: List[Token] = []
        self.proc_buffer: List[List[Union[str,List[Token]]]] = []
        self.buffer_index: int = 0
        self.procs: Dict[str, List[Token]] = {}

        self.in_struct: bool = False
        self.struct_name: str = ""
        self.struct_contents: Dict[str, Tuple[Any,TokenType]] = {}
        self.structs: Dict[str, Dict[str, Tuple[Any, TokenType]]] = {}

        self.in_macro: bool = False
        self.macro_name: str = ""
        self.macro_contents: list[Token] = []
        self.macros: dict[str, list[Token]] = {}

        self.type_table: Dict[Type, TokenType] = {
            int  : TokenType.INT,
            str  : TokenType.STRING,
            bool : TokenType.BOOL
        }

    def print_error(self, error: str) -> None:
        print(error)
        self.tokens = [Token(TokenType.EOF, None, TokenType.OPERAND, (0, 0), "")]

    def at_end(self) -> bool:
        return self.index >= len(self.tokens)

    def advance(self) -> Token:
        self.token: Token = self.tokens[self.index]
        self.index += 1
        return self.token
    
    def peek(self) -> Token:
        return self.tokens[self.index]
    
    def interpret_object(self, obj: List[Token]) -> None:
        current_branch = self.tokens
        current_index = self.index
        self.tokens = obj
        self.index = 0
        for _ in obj:
            self.interpret_token()
        self.index = current_index
        self.tokens = current_branch

    def interpret_token(self) -> None:
        self.token: Token = self.advance()

        if self.fall_through:

            if self.in_macro:
                if self.token._type in [TokenType.PROC, TokenType.MACRO, TokenType.STRUCT]:
                    self.print_error(f"{self.token.filename}:{self.token.position[0]}:{self.token.position[1]}: Unable to have object definition inside macro\n\nIllegal Example:\n--------------------\n[macro_name] :: macro\n    [{self.token._type.name.lower()}_name] :: {self.token._type.name.lower()}\n        [{self.token._type.name.lower()}_contents]\n    end\n    [macro_contents]\nend\n--------------------\n\nLegal Example:\n--------------------\n[{self.token._type.name.lower()}_name] :: {self.token._type.name.lower()}\n    [{self.token._type.name.lower()}_contents]\nend\n\n[macro_name] :: macro\n    [macro_contents]\nend\n--------------------")

                if self.end_tolerance == 0 and self.token._type == TokenType.END:
                    self.fall_through = False
                    return
                
                if self.token._type != TokenType.END:
                    if self.token._type == TokenType.IF:
                        self.end_tolerance += 1
                else:
                    self.end_tolerance -= 1

                self.macro_contents.append(self.token)
                return
            if self.in_proc:

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

                self.proc_contents.append(self.token)
                return
            
            if self.in_struct:
                if self.token._type == TokenType.END:
                    self.fall_through = False
                    return
                if self.token._type != TokenType.END:
                    self.struct_contents[self.token.value] = (None, self.tokens[self.index]._type)
                    self.index =+ 1
                else:
                    self.fall_through = False
                return

            else:
                if self.token._type == TokenType.ELSE and self.end_tolerance == 0:
                    self.fall_through = False
                    return
                
                elif self.token._type != TokenType.END:
                    if self.token._type == TokenType.IF:
                        self.end_tolerance += 1
                    return
                
                if self.end_tolerance == 0:
                    self.fall_through = False
                    return
                else:
                    self.end_tolerance -= 1
                return
        
        if self.in_proc:
            if self.proc_name != "":
                self.procs[self.proc_name] = self.proc_contents
            else:
                self.stack.append(self.proc_contents)
                self.proc_contents = []
            self.in_proc = False
            self.proc_name = ""
            if len(self.proc_buffer) > 0:
                self.proc_name = self.proc_buffer[self.buffer_index - 1][0] # type: ignore
                self.proc_contents = self.proc_buffer[self.buffer_index - 1][1] # type: ignore
                self.proc_buffer.pop()
                self.buffer_index -= 1
                self.in_proc = True
            else:
                self.proc_contents = []

        if self.in_macro:
            self.macros[self.macro_name] = self.macro_contents
            self.macro_name = ""
            self.macro_contents = []
            self.in_macro = False

        if self.in_struct:
            try:
                del self.struct_contents[None] # type: ignore | stupid hack
            except KeyError:
                pass #fuck you
            self.structs[self.struct_name] = self.struct_contents
            self.in_struct = False
            self.struct_name = ""
            self.struct_contents = {}

        match self.token._type:

            case TokenType.MACRO:
                print(f"{self.token.filename}:{self.token.position[0]}:{self.token.position[1]}: Cannot declare a macro and leave it unwrapped.\n\nTry using:\n----------------------\n[macro-name] :: macro\n    [macro-contents]\nend\n----------------------")
                exit(1)

            case TokenType.EXIT:
                if len(self.stack) >= 1:
                    exit(self.stack.pop())
                else:
                    exit()

            case TokenType.PIPE:
                if self.tokens[self.index].value_type == TokenType.IDENTIFIER and self.tokens[self.index + 1]._type == TokenType.PIPE:
                    proc_name = self.tokens[self.index].value
                    self.stack.append(self.procs[proc_name])
                    self.index += 1
                else:
                    ...

            case TokenType.ARROW:
                struct: dict = self.stack.pop()
                param: str = self.tokens[self.index].value
                if self.tokens[self.index + 2]._type == TokenType.EQUAL:
                    content = self.tokens[self.index + 1].value
                    struct[param] = (content, struct[param][1])
                else:
                    self.stack.append(struct[param][0])

            case TokenType.CALL_STRUCT:
                self.stack.append(self.structs[self.stack.pop()])

            case TokenType.OBJECT_ASSIGN:
                match self.tokens[self.index]._type:

                    case TokenType.PROC:
                        self.proc_name = self.tokens[self.index - 2].value
                        self.index += 1
                        self.fall_through = True
                        self.in_proc = True

                    case TokenType.STRUCT:
                        self.struct_name = self.tokens[self.index - 2].value
                        self.index += 1
                        self.fall_through = True
                        self.in_struct = True

                    case TokenType.MACRO:
                        self.macro_name = self.tokens[self.index - 2].value
                        self.index += 1
                        self.fall_through = True
                        self.in_macro = True

                    case TokenType.LT:
                        name = self.tokens[self.index - 2].value
                        if self.tokens[self.index + 1].value_type == TokenType.IDENTIFIER and self.tokens[self.index + 2]._type == TokenType.GT:
                            struct_name = self.tokens[self.index + 1].value
                            self.variables[name] = self.structs[struct_name]
                            self.index += 3
                        else:
                            ...

                    case TokenType.GRAB_OBJECT:
                        name = self.tokens[self.index - 2].value
                        for item in self.stack:
                            if isinstance(item, list):
                                self.procs[name] = item
                                self.stack.remove(item)
                                break

                    case TokenType.PIPE:
                        name = self.tokens[self.index - 2].value
                        if self.tokens[self.index + 1].value_type == TokenType.IDENTIFIER and self.tokens[self.index + 2]._type == TokenType.PIPE:
                            proc_name = self.tokens[self.index + 1].value
                            self.procs[name] = self.procs[proc_name]
                            self.index += 3
                        else:
                            ...

                    case TokenType.PUSH:
                        name = self.stack.pop()
                        _object = self.stack.pop()
                        if isinstance(_object, list):
                            self.procs[name] = _object

            case TokenType.PROC:
                self.fall_through = True
                self.in_proc = True
                if self.tokens[self.index - 2]._type == TokenType.OBJECT_ASSIGN:
                    self.proc_name = self.tokens[self.index - 3].value

            case TokenType.CALL:
                proc_to_call = self.stack.pop()
                if isinstance(proc_to_call, list):
                    self.interpret_object(proc_to_call)
                else:
                    self.interpret_object(self.procs[proc_to_call])

            case TokenType.CALL_VAR:
                self.var_name: str = self.stack.pop()
                self.stack.append(self.variables[self.var_name])

            case TokenType.LT:
                item_1 = self.stack.pop()
                item_2 = self.stack.pop()
                self.stack.append(item_2 < item_1)

            case TokenType.EQUAL:
                #[print(f"{token._type} : ({token.position[0]}, {token.position[1]})") for token in self.tokens]
                self.contents = self.stack.pop()
                self.name = self.stack.pop()

                #if isinstance(self.name) or self.name_token.value_type == TokenType.NUMBER:
                #    self.print_error(f"{self.name_token.filename}:{self.name_token.position[0]}:{self.name_token.position[1]}: Expected variable name to be of type \"IDENTIFIER\" but got \"{self.name_token.value_type.name}\" instead.")
                #    return
                
                self.variables[self.name] = self.contents

            case TokenType.DUP:
                item = self.stack.pop()
                self.stack.append(item)
                self.stack.append(item)

            case TokenType.PUSH:
                if self.token.value in self.macros.keys():
                    self.interpret_object(self.macros[self.token.value])
                else:
                    self.stack.append(self.token.value)
                
            case TokenType.PLUS:
                num_1 = self.stack.pop()
                num_2 = self.stack.pop()

                self.stack.append(num_1 + num_2)

            case TokenType.PRINT:
                if len(self.stack) == 0:
                    self.print_error(f"{self.token.filename}:{self.token.position[0]}:{self.token.position[1]}: Attempting to print from an empty stack..")
                    return
                if self.token.value_type == TokenType.STRING:
                    print(self.stack.pop())
                else:
                    print(self.stack.pop())

            case TokenType.SWAP:
                item_1 = self.stack.pop()
                item_2 = self.stack.pop()
                self.stack.append(item_1)
                self.stack.append(item_2)

            case TokenType.DROP:
                name: str = self.stack.pop()
                if name in self.variables.keys():
                    del self.variables[name]

            case TokenType.IF:
                self.found_if = True
                self.conditional: bool = self.stack.pop()
                if not self.conditional:
                    self.fall_through = True
                    self.end_tolerance = 0

            case TokenType.ELSE:
                self.fall_through = True
                if not self.found_if:
                    token = self.tokens[self.index - 1]
                    self.print_error(f"{token.filename}:{token.position[0]}:{token.position[1]}: Found an \"else\" statement before an \"if\" statement")
                    return
                self.found_if = False

            case TokenType.END:
                self.fall_through = False

            case TokenType.EQUAL_EQUAL:
                self.item_1 = self.stack.pop()
                self.item_2 = self.stack.pop()
                self.stack.append(self.item_1 == self.item_2)

    def interpret(self, show_registers: bool, show_vars: bool, deconstruct: bool, proc_to_deconstruct: str) -> None:
        while not self.at_end():
            self.interpret_token()
        if show_vars:
            print(self.variables)
        if deconstruct:
            if proc_to_deconstruct in self.procs.keys():
                print(f"Result of \"{proc_to_deconstruct}\":")
                [print(f"    {token._type}") for token in self.procs[proc_to_deconstruct]]
