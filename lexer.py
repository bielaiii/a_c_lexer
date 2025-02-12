# from ast import Str, literal_eval
# from curses.ascii import isdigit
from enum import Enum, IntEnum, auto
from genericpath import samefile
from math import fabs
from mmap import MADV_AUTOSYNC
from os import name
import re
from tokenize import Token
from typing import Generator

# from xml.dom.minidom import Entity
from more_itertools import peekable
import uuid

import more_itertools





class build_in_type(Enum):
    INT = auto()
    UNSIGNED_INT = auto()
    SHORT = auto()
    UNSIGNED_SHORT = auto()
    LONG_LONG = auto()
    UNSIGNED_LONG_LONG = auto()
    LONG = auto()
    UNSIGNED_LONG = auto()
    DOUBLE = auto()
    FLOAT = auto()
    CHAR = auto()
    SIGNED_CHAR = auto()
    UNSIGNED_CHAR = auto()
    BUILD_IN_POINTER = auto()
    BUILD_IN_ARRAY = auto()
    DEFINED_STRUCT = auto()
    DEFINED_UNION = auto()
    CALL_FUNCTION = auto()

    def __str__(self):
        temp_str = self.name.lower().replace("_", " ")

        return temp_str

class C_type:
    def __init__(self, type_ : build_in_type, is_const_ = False, is_volatile_ = False):
        self.type = type_
        self.is_const = is_const_
        self.is_volatile = is_volatile_
        #self.subtype
        pass
    def __str__(self)->str:
        quan_ = ""
        if self.is_const:
            quan_ += "const "
        
        if self.is_volatile:
            quan_ += "volatile "
        
        return f"{quan_}{self.type}"
    
    def GetMember() -> list[tuple[str, "C_type"]]:
        pass

class C_build_in_type(C_type):
    def __init__(self, argument_list : list[str]):
        #super().__init__()
        self.size = len(argument_list)
        self.element_type 



class C_complex_type(C_type):
    def __init__(self, argument_dict:dict):
        self.argument_dict = argument_dict

    def __setitem__(self, key : int ,val : any):
        self.argument_dict[key] = val

    def __getitem__(self, key : int):
        return self.argument_dict[key]

class C_build_in_pointer(C_type):
    def __init__(self, type_, is_const_=False, is_volatile_=False):
        super().__init__(type_, is_const_, is_volatile_)
        self.type = build_in_type.BUILD_IN_POINTER
    pass
class C_build_in_array(C_complex_type):

    def __init__(self, argument_dict : dict):
        super().__init__(argument_dict)
        self.__size = len(argument_dict)
        self.type = build_in_type.BUILD_IN_ARRAY
    
    def Size(self) ->int:
        return self.__size

    def __setitem__(self, key : int ,val : any):
        assert isinstance(key, int)
        self.argument_dict[key] = val

    def __getitem__(self, key : int):
        assert isinstance(key, int)
        return self.argument_dict[key]

class C_struct(C_complex_type):
    def __init__(self):
        super().__init__()
        self.type = build_in_type.DEFINED_STRUCT

    
class C_union(C_complex_type):
    def __init__(self):
        super().__init__()
        self.type = build_in_type.DEFINED_UNION

class C_function_ptr(C_build_in_pointer):
    def __init__(self):
        super().__init__()
        self.type = build_in_type.CALL_FUNCTION




def SetType(type_: str) -> build_in_type | str:
    match (type_):
        case "unsigned int":
            return build_in_type.UNSIGNED_INT
        case "int":
            return build_in_type.INT
        case "short":
            return build_in_type.SHORT
        case "unsigned short":
            return build_in_type.UNSIGNED_SHORT
        case "long":
            return build_in_type.LONG
        case "long long":
            return build_in_type.LONG_LONG
        case "unsigned long long":
            return build_in_type.UNSIGNED_LONG_LONG
        case "char":
            return build_in_type.CHAR
        case "signed char":
            return build_in_type.SIGNED_CHAR
        case "unsigned char":
            return build_in_type.UNSIGNED_CHAR
        case "double":
            return build_in_type.DOUBLE
        case "float":
            return build_in_type.FLOAT
        case _:
            return type_


#class UsingType:
#    def __init__(
#        self,
#        typename_: str,
#        is_const_: bool = False,
#        is_volatile_: bool = False,
#        is_array_: bool = False,
#        array_size_: int = -1,
#        #########is_ptr: bool = False,
#    ):
#        self.typename: UsingType | str = SetType(typename_)
#        self.subtype: UsingType = None
#        self.is_const = is_const_
#        self.is_volatile = is_volatile_
#        self.is_array = is_array_
#        self.__array_size = array_size_
#        self.argument_list: list = None
#        self.typedef_name = ""
#        self.member_list = None
#        # self.is_ptr = is_ptr
#
#    # todo: future fix: location of const and volatile, which quantify which
#    def __str__(self):
#        quan_ = ""
#
#        if self.is_const:
#            quan_ += "const"
#        if self.is_volatile:
#            quan_ += "volatile"
#
#        if quan_ != "":
#            quan_ += " of"
#        # todo: support typedef
#
#        if self.typename == build_in_type.BUILD_IN_POINTER:
#            return f"is ptr to {self.subtype}"
#
#        if self.is_array:
#            assert self.__array_size != -1
#            return f"{quan_} array {self.__array_size} of {self.typename}"
#        else:
#            return f"{quan_} {self.typename}"
#
#    def is_buildin_type_combination(self) -> bool:
#        if isinstance(self.typename, build_in_type):
#            return True
#        return False
#
#    def SetArraySize(self, sz: int):
#        self.is_array = 1
#        self.__array_size = sz
#
#    def GetArraySize(self):
#        if not self.is_array:
#            print("current type is not array")
#        return self.__array_size
#
#    def UpdateSubtype(self) -> "UsingType":
#        type_: UsingType = None
#        if self.subtype is None:
#            return self
#        parent_type = self.typename
#        while (type_ := parent_type.subtype) is None:
#            parent_type = parent_type.subtype
#        return type_


all_defined_type: dict[str, "UserDefineType"] = {}


class UserDefineType:
    def __init__(self, name_: str, typedef_name_: str):
        if name_ == "":
            self.name = uuid.uuid4()

        self.member: dict[str, identifier] = {}
        if typedef_name_ == "":
            typedef_name_ = None
        self.typedef_name: str = typedef_name_

    def AddMember(self, name_: str, type_: str):
        self.member[name_] = identifier(type_, name_)


class UserDefineStruct(UserDefineType):
    def __init__(self, name_: str):
        super().__init__(name_)

    def __setitem__(self, key: str, val: any):
        self.member[key].value = val

    def __setitem__(self, key: str, val: any):
        self.member[key].value = val


class UserDefineEnum(UserDefineType):
    def __init__(self, name_: str):
        super().__init__(name_)


class UserDefineUnion(UserDefineType):
    def __init__(self, name_: str):
        super().__init__(name_)

    def __setitem__(self, key: str, val: any):
        self.member[key].value = val

    def __setitem__(self, key: str, val: any):
        self.member[key].value = val


class identifier:
    all_identifier: dict[str, "identifier"] = {}

    def __init__(self, typename: str | C_type, varname: str, val: int | str = None):
        self.type: C_type
        self.annotated_name = varname
        if isinstance(typename, str):
            self.type: C_type = C_type(typename)
        else:
            self.type: C_type = typename
        self.value: any = val
        identifier.all_identifier[self.annotated_name] = self

    def __str__(self) -> str:
        temp_str = (
            f"name : {self.annotated_name}\ntype : {self.type}\nval : {self.value}\n"
        )
        return temp_str


# much more reserved word
reserved_word = [
    "alignas",
    "alignof",
    "auto",
    "bool",
    "break",
    "case",
    "char",
    "const",
    "constexpr",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "false",
    "float",
    "for",
    "goto",
    "if",
    "inline",
    "int",
    "long",
    "nullptr",
    "register",
    "restrict",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "static_assert",
    "struct",
    "switch",
    "thread_local",
    "true",
    "typedef",
    "typeof",
    "typeof_unqual",
    "union",
    "unsigned",
    "void",
    "volatile",
    "while",
    "_Alignas",
    "_Alignof",
    "_Atomic",
    "_BitInt",
    "_Bool",
    "_Complex",
    "_Decimal128",
    "_Decimal32",
    "_Decimal64",
    "_Generic",
    "_Imaginary",
    "_Noreturn",
    "_Static_assert",
    "_Thread_local",
]


class UserDefineStruct:
    def __init__(self):
        pass


expression_keyword = ["if", "while", "for", "do"]


class Expression:
    def __init__(self, mode_: str):
        pass


known_types = [
    "int",
    "unsigned int",
    "char",
    "signed char",
    "unsigned char",
    "long",
    "unsigned long",
    "long long",
    "unsigned long long",
    "double",
    "float",
]


def OmitToken(codes: str) -> Generator:
    token = ""
    bracket_stack = []
    for c in codes:
        if c in "0123456789_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
            token += c
        else:
            if token != "" and token not in reserved_word:
                yield token
                yield c
                token = ""
            elif token != "" and token in reserved_word:
                yield token
                token = ""
                """ if token == "if":
                    pass
                elif token == "for":
                    pass
                elif token == "while" or token == "do":
                    pass """
            elif token in known_types:
                yield token
                token = ""
            elif c in ["\n", "\t", " ", "\b"]:
                # bracket_stack.append(c)
                continue
            else:
                yield c


def TokenGen(codes: str):
    tokengen = peekable(OmitToken(codes))
    # print("hello,world")

    peek_ = tokengen.peek()
    if peek_ in known_types:
        ReadDeclaration(tokengen)


all_type: dict[str, UserDefineType] = {}
all_identifier: dict[str, identifier] = {}
sample_code = "int a[3];"


def IsIdentifier(identifier: str) -> False:
    if identifier in reserved_word:
        return False
    if (temp := re.search(r"([\w_]+)", identifier)) is not None:
        temp = temp.group(1)
        if temp == identifier:
            return True
        else:
            return False
    else:
        return False


def SolveToken():
    more_itertools.peekable(OmitToken(sample_code))
    token = next(more_itertools)
    token_list = []
    try:
        while True:
            token_list.append(token)
            token = next(more_itertools)
            if IsIdentifier(token_list[-1]):
                name_ = token_list.pop()
                type_ = token_list.pop()
                # all_identifier[]

    except StopIteration:
        pass


class Lexer:
    all_type: dict[str, UserDefineType] = {}
    all_identifier: dict[str, identifier] = {}

    def __init__(self):

        pass

    pass


def funcname(self, parameter_list):
    """
    docstring
    """
    pass


def is_c_type(code: str):
    build_in_reserved_word = [
        "unsigned",
        "long",
        "char",
        "double",
        "float",
        "char",
        "int",
    ]
    if code in build_in_reserved_word:
        return True
    if code in all_defined_type:
        return True
    if code == "*":
        return True
    return False


def GetSubtype(codeGenerator : peekable, token_list : list[str]) -> C_type:
    token = next(codeGenerator)
    type_ = None
    is_ptr = False
    #token_list = []
    id: identifier = None
    is_const_ = 0
    is_volatile_ = 0
    temp_: str = ""
    bracket_content = ""
    while token != ";":

        token_list.append(token)

        if token == "[":
            while token != "]":
                token = next(codeGenerator)
                bracket_content += token
                
                token_list.append(token)

            array_size = ""
            token_list.pop()
            while (temp_ := token_list.pop()) != "[":
                array_size += temp_
            #update_typed = id.type.UpdateSubtype()
            current_type = C_build_in_array(build_in_type.BUILD_IN_ARRAY, array_size = bracket_content)
            current_type.subtype = GetSubtype(codeGenerator, token_list)
            break
            #math_type = token_list.pop()
            #update_typed.subtype = UsingType(math_type, is_array_=1, array_size_=array_size)
            #SetArraySize(array_size)
        elif token == "(":
            while token != ")":
                token = next(codeGenerator)
                token_list.append(token)

            argument_list = ""
            while (temp_ := token_list.pop()) != "(":
                argument_list += temp_
            id.type.argument_list = argument_list
            break
        # todo: support init list
        elif token == "{":  # init list
            while token != "}":
                token = next(codeGenerator)
            pass
            # continue
        elif token == "*":
            current_type = C_function_ptr()
            current_type.subtype = GetSubtype(codeGenerator, token_list)
            return current_type

        token = next(codeGenerator)
    #if len(token_list):
    #    math_type = token_list.pop()
    #    update_typed.subtype = UsingType(math_type)
    #    return update_typed
    return None


def ReadDeclaration(codeGenerator: peekable) -> identifier:
    token = next(codeGenerator)
    literal_: str = ""
    type_ = None
    is_ptr = False
    count_l_char = 0
    is_unsigned = 0
    token_list = []
    id: identifier = None
    is_const_ = 0
    is_volatile_ = 0
    temp_: str = ""
    try:
        while token != ";":

            token_list.append(token)

            if IsIdentifier(token):
                identifier_name = token_list.pop()
                while not is_c_type(type_ := token_list.pop()):
                    if type_ == "const":
                        is_const_ = 1
                    elif type_ == "volatile":
                        is_volatile_ = 1
                identifier_type = type_
                if identifier_type == "*":
                    if not codeGenerator.peek() == "[":
                        identifier_type = build_in_type.BUILD_IN_POINTER
                    else:
                        identifier_type = build_in_type.BUILD_IN_ARRAY
                
                if codeGenerator.peek() == ")":
                    _ = next(codeGenerator)

                #if id is None:
                id  = C_type(
                    UsingType(identifier_type, is_const_, is_volatile_), identifier_name
                )
                id.subtype = GetSubtype(codeGenerator, token_list)
                all_identifier[id.annotated_name] = id
                break
                #else:
                #    last_sub_type = id.type.UpdateSubtype()
                #    last_sub_type.subtype = UsingType(type_, is_const_, is_volatile_)
                #all_identifier[id.annotated_name] = id
                #all
            token = next(codeGenerator)
    except StopIteration:
        pass
        #elif id is None:
        #    token_list.append(token)
        """ elif id is not None:
            if token == "[":
                while token != "]":
                    token = next(codeGenerator)
                    token_list.append(token)

                array_size = ""
                token_list.pop()
                while (temp_ := token_list.pop()) != "[":
                    array_size += temp_
                update_typed = id.type.UpdateSubtype()
                math_type = token_list.pop()
                update_typed.subtype = UsingType(math_type, is_array_=1, array_size_=array_size)
                #SetArraySize(array_size)
            elif token == "(":
                while token != ")":
                    token = next(codeGenerator)
                    token_list.append(token)

                argument_list = ""
                while (temp_ := token_list.pop()) != "(":
                    argument_list += temp_
                id.type.argument_list = argument_list
            # todo: support init list
            elif token == "{":  # init list
                while token != "}":
                    token = next(codeGenerator)
                pass
                # continue """

    #    token = next(codeGenerator)
    #if len(token_list):
    #    math_type = token_list.pop()
    #    update_typed.subtype = UsingType(math_type)

    return id
    # return identifier(UsingType(type_), token, token)


sample_code = ["int const volatile (*a)[3];", "int const volatile *a[3];", ]
samefile_code = ["int (*a)[3];"]
C_init_list = "struct a {.a = 10, .b = 3.124};"

for s in samefile_code:
    TokenGen(s)
    print(all_identifier["a"])

# a = ReadDeclaration(cg)
# print(a)


class Lexer:
    all_type: dict[str, UserDefineType] = {}
    all_identifier: dict[str, identifier] = {}

    def __init__(self):

        pass
