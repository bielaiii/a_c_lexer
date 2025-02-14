from enum import Enum, auto
import re
from typing import Generator
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

    def is_build_in_type(self) -> bool:
        return True if self.value < 14 else False

    def is_complex_type(self) -> bool:
        return True if self.value >= 14 else False


class C_type:
    def __init__(self, type_: build_in_type, is_const_=False, is_volatile_=False):
        self.type = type_
        self.is_const = is_const_
        self.is_volatile = is_volatile_
        # self.subtype = None

    def __str__(self) -> str:
        quan_ = ""
        if self.is_const:
            quan_ += "const "

        if self.is_volatile:
            quan_ += "volatile "

        return f"{quan_}{self.type}"

    def GetMember() -> list[tuple[str, "C_type"]]:
        pass


class C_build_in_type(C_type):
    def __init__(self, argument_list: list[str]):
        # super().__init__()
        self.size = len(argument_list)
        self.element_type


class C_complex_type(C_type):
    def __init__(
        self,
        type__: build_in_type,
        subtype_ : build_in_type | C_type,
        is_const_: bool = False,
        is_volatile: bool = False,
    ):
        super().__init__(type__, is_const_, is_volatile)
        self.__minorType: C_type | C_complex_type = None
        self.subtype = subtype_

    def __setitem__(self, key: int, val: any):
        self.argument_dict[key] = val

    def __getitem__(self, key: int):
        return self.argument_dict[key]

    def MinorType(self) -> C_type:
        return self.__minorType

    def __str__(self) -> str:
        return f"{super().__str__()} of "


class C_build_in_pointer(C_complex_type):
    def __init__(self, subtype: C_type, is_const_=False, is_volatile_=False):
        super().__init__(build_in_type.BUILD_IN_POINTER, subtype, is_const_, is_volatile_)

    def __str__(self):
        return f"{super().__str__()}{self.subtype}"

class C_build_in_array(C_complex_type):

    def __init__(
        self,
        size_: int,
        element_type_: C_type,
        is_const: bool = False,
        is_volatile=False,
    ):
        super().__init__(build_in_type.BUILD_IN_ARRAY, element_type_, is_const, is_volatile)
        self.__size = size_
        #self.sub_type: C_type = element_type_

    def Size(self) -> int:
        return self.__size

    def __setitem__(self, key: int, val: any):
        assert isinstance(key, int)
        self.argument_dict[key] = val

    def __getitem__(self, key: int):
        assert isinstance(key, int)
        return self.argument_dict[key]

    def __str__(self):
        return f"{super().__str__()}{self.__size} of {self.subtype}"


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


def StringToEnum(type_str: str):
    match type_str:
        case "int":
            return build_in_type.INT
        case "unsigned int":
            return build_in_type.UNSIGNED_INT
        case "long long":
            return build_in_type.LONG_LONG
        case "unsigned long long":
            return build_in_type.UNSIGNED_LONG_LONG
        case "long":
            return build_in_type.LONG


def SrtToType(type_str: str) -> build_in_type:
    match type_str:
        case "int":
            return build_in_type.INT
        case "unsigned int":
            return build_in_type.UNSIGNED_INT
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
            raise AssertionError


# def Factory_C_Type(type_ : build_in_type, *args, **kwargs):
#    match type_:
#        case type_.is_build_in_type():
#            return C_type(*args, **kwargs)
#        case build_in_type.C_Struct():
#            return C_complex_type(*args, **kwargs)


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

    if identifier in all_defined_type:
        return True
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


def is_cv(codeGenerator: peekable):
    cv_list = ["const", "volatile"]
    return True if codeGenerator.peek() in cv_list else False


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


def GetSubtype(codeGenerator: peekable, token_list: list[str]) -> C_type:
    token = next(codeGenerator)
    type_ = None
    is_ptr = False
    # token_list = []
    id: identifier = None
    is_const_ = 0
    is_volatile_ = 0
    temp_: str = ""
    bracket_content = ""
    argument_dict = {}
    while token != ";":

        token_list.append(token)

        if token == "[":
            token = next(codeGenerator)
            while token != "]":
                bracket_content += token
                token = next(codeGenerator)

                token_list.append(token)

            array_size = bracket_content
            token_list.pop()
            while (temp_ := token_list.pop()) != "[":
                array_size += temp_
            # update_typed = id.type.UpdateSubtype()
            if codeGenerator.peek() == "=":
                pass
            else:
                element_type = GetSubtype(codeGenerator, token_list)
                # argument_dict = {x : identifier(element_type, x, None) for  x in range()}

            return C_build_in_array(array_size, element_type)
            # current_type.subtype = GetSubtype(codeGenerator, token_list)
            break
            # math_type = token_list.pop()
            # update_typed.subtype = UsingType(math_type, is_array_=1, array_size_=array_size)
            # SetArraySize(array_size)
        elif token == "(":
            while token != ")":
                token = next(codeGenerator)
                token_list.append(token)

            argument_list = ""
            while (temp_ := token_list.pop()) != "(":
                argument_list += temp_
            id.type.argument_list = argument_list
            break
        elif token == ")":
            in_parathesis = []
            token_list.pop()
            while token_list[-1] != "(":
                in_parathesis.append(token_list.pop())

            token_list.pop()
            while is_cv(codeGenerator):
                temp_ = next(codeGenerator)
                if temp_ == "const":
                    is_const_ = True

                if temp_ == "volatile":
                    is_volatile_ = True

            return C_build_in_pointer(
                GetSubtype(codeGenerator, token_list),
                is_const_=is_const_,
                is_volatile_=is_volatile_,
            )

            token_list.pop()
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
        elif token in known_types:
            return StringToEnum(token)

        token = next(codeGenerator)

    while len(token_list):
        temp_ = token_list.pop()
        if temp_ == "const":
            is_const_ = True
        if temp_ == "volatile":
            is_volatile_= True
    assert len(token_list) == 0, token_list
    return C_type(StringToEnum(temp_), is_const_, is_volatile_)


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
    type_ = None
    try:
        while token != ";":
            token_list.append(token)
            if IsIdentifier(token):
                identifier_name = token_list.pop()
                id = identifier(GetSubtype(codeGenerator, token_list), token)
                all_identifier[id.annotated_name] = id
                return id
            token = next(codeGenerator)
    except StopIteration:
        pass

    return id


sample_code = [
    "int const volatile (*a)[3];",
    "int const volatile *a[3];",
]
samefile_code = ["int (*a)[3];"]
C_init_list = "struct a {.a = 10, .b = 3.124};"

for s in sample_code:
    TokenGen(s)
    print(all_identifier["a"])




class Lexer:
    all_type: dict[str, UserDefineType] = {}
    all_identifier: dict[str, identifier] = {}

    def __init__(self):

        pass
