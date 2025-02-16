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
    def __init__(
        self, type_: build_in_type, is_const_=False, is_volatile_=False, aka: str = ""
    ):
        self.type = type_
        self.is_const = is_const_
        self.is_volatile = is_volatile_
        self.aka = aka
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
        subtype_: build_in_type | C_type,
        is_const_: bool = False,
        is_volatile: bool = False,
        aka: str = "",
    ):
        super().__init__(type__, is_const_, is_volatile, aka)
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
    def __init__(
        self, subtype: C_type, is_const_=False, is_volatile_=False, aka: str = ""
    ):
        super().__init__(
            build_in_type.BUILD_IN_POINTER, subtype, is_const_, is_volatile_
        )

    def __str__(self):
        return f"{super().__str__()}{self.subtype}"


class C_build_in_array(C_complex_type):

    def __init__(
        self,
        size_: int,
        element_type_: C_type,
        is_const: bool = False,
        is_volatile=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.BUILD_IN_ARRAY, element_type_, is_const, is_volatile, aka
        )
        self.__size = size_
        # self.sub_type: C_type = element_type_

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


class C_USER_DEFINED_TYPE(C_type):
    def __init__(
        self,
        type_,
        argument_dict: dict,
        typedef_name : str = "",
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(type_, is_const_, is_volatile_, aka)
        self.argument_dict = argument_dict
        self.typedef_name = typedef_name

    def __str__(self) -> str:
        fmtstr = f"{self.type} : aka {self.typedef_name}\nmember:{{\n{"\n".join([f"{k} : {v}" for k, v in self.argument_dict.items()])}\n}}"
        return fmtstr


class C_struct(C_USER_DEFINED_TYPE):
    def __init__(
        self,
        argument_dict: dict[str, C_type],
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.DEFINED_STRUCT, argument_dict, is_const_, is_volatile_, aka
        )
        # self.type = build_in_type.DEFINED_STRUCT


class C_union(C_USER_DEFINED_TYPE):
    def __init__(
        self,
        argument_dict: dict[str, C_type],
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.DEFINED_UNION, argument_dict, is_const_, is_volatile_, aka
        )
        # self.type = build_in_type.DEFINED_UNION


class C_function_ptr(C_USER_DEFINED_TYPE):
    def __init__(
        self,
        argument_dict: dict[str, C_type],
        is_const=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.CALL_FUNCTION, argument_dict, is_const, is_volatile_, aka
        )


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

    def __str__(self) -> str:
        fmtstr = f"{self.name} : aka {self.typedef_name}\nmember:{{{"\n    ".join([f"{k} : {v}" for k, v in self.member.items()])}}}"
        return fmtstr


class UserDefineStruct(UserDefineType):
    def __init__(self, name_: str):
        super().__init__(name_)

    def __setitem__(self, key: str, val: any):
        self.member[key].value = val

    def __setitem__(self, key: str, val: any):
        self.member[key].value = val

    def __str__(self) -> str:
        fmtstr = f"{self.name} : aka {self.typedef_name}\nmember:{{{"\n    ".join([f"{k} : {v}" for k, v in self.member.items()])}}}"
        return fmtstr


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
        self.is_const = False
        self.is_volatile = False

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
    "struct",
    "union",
    "unsigned",
]


frament_type_key = [
    "int",
    "unsigned",
    "char",
    "signed",
    "unsigned",
    "long",
    "double",
    "float",
    "struct",
    "union",
    "short",
]


def StringToEnum(type_str: str):
    match type_str:
        case "int":
            return build_in_type.INT
        case w if w in ["unsigned int" , "int unsigned"]:
            return build_in_type.UNSIGNED_INT
        case "char":
            return build_in_type.CHAR
        case w if w in ["unsigned char" , "char unsigned"]:
            return build_in_type.UNSIGNED_CHAR
        case w if w in ["signed char" , "char signed"]:
            return build_in_type.SIGNED_CHAR
        case "short":
            return build_in_type.SHORT
        case w if w in ["unsigned short" , "short unsigned"]:
            return build_in_type.UNSIGNED_SHORT
        case "long long":
            return build_in_type.LONG_LONG
        case w if w in ["unsigned long long" , "long long unsigned"]:
            return build_in_type.UNSIGNED_LONG_LONG
        case "long":
            return build_in_type.LONG
        case  w if w in ["unsigned long" , "long unsigned"]:
            return build_in_type.UNSIGNED_LONG
        case "struct":
            return build_in_type.DEFINED_STRUCT
        case "union":
            return build_in_type.DEFINED_UNION


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
            # if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789":
            #    token += c
            if c in ["\t", " ", "\b","\n"]:
                if token != "":
                    yield token
                    token = ""
                continue
            elif not IsIdentifier(c):
                if token != "":
                    yield token
                token = ""
                # token += c
                yield c
            elif token in known_types:
                yield token
                token = ""
            else:
                yield c
            # if not IsIdentifier(c) and IsIdentifier(token):
            #    yield token
            #    yield c


typedef_dict: dict[str, C_type] = {}


def TokenGen(codes: str):
    tokengen = peekable(OmitToken(codes))
    # print("hello,world")
    peek_ = tokengen.peek()
    typedef_name = ""
    temp_type = None
    try:
        while peek_ := tokengen.peek():
            if peek_ in known_types:
                ReadDeclaration(tokengen)
            elif peek_ == "#":
                # Preprocessor(tokengen)
                pass
            elif peek_ == "struct":
                next(tokengen)
                typedef_name, temp_type = ReadTypedef(tokengen)
                while peek_ != ";":
                    typedef_dict[peek_] = f"{typedef_name}"
                    peek_ = next(tokengen)
                # typed
                pass
            elif peek_ == "typedef":
                next(tokengen)
                if temp_type is not None:
                    peek_ = next(tokengen)
                    while peek_ != ";":
                        typedef_dict[peek_] = temp_type
                        peek_ = next(tokengen)
                    pass
            elif peek_ in expression_keyword:
                pass
            else:
                peek_ = next(tokengen)
    except StopIteration:
        pass


all_type: dict[str, UserDefineType] = {}
all_identifier: dict[str, identifier] = {}
sample_code = "int a[3];"


def IsIdentifier(identifier: str) -> False:
    if identifier in reserved_word:
        return False

    if identifier in all_defined_type:
        return True
    if (temp := re.search(r"(^[a-zA-Z_][\w_]*?$)", identifier)) is not None:
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
            if codeGenerator.peek() == "=":
                pass
            else:
                element_type = GetSubtype(codeGenerator, token_list)

            return C_build_in_array(array_size, element_type)

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
            while len(token_list) and token_list[-1] != "(":
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
                if codeGenerator.peek() == "\n":
                    token = next(codeGenerator)
                    continue
                elif codeGenerator.peek() == "}":
                    next(codeGenerator)
                    break
                id = ReadDeclaration(codeGenerator)
                if id is None and codeGenerator.peek() == "}":
                        break
                argument_dict[id.annotated_name] = id
                #token = next(codeGenerator)
            return C_USER_DEFINED_TYPE(build_in_type.DEFINED_STRUCT, argument_dict)
        elif token == "*":
            if codeGenerator.peek() == "(":
                pass
            current_type = C_build_in_pointer(GetSubtype(codeGenerator, token_list))
            return current_type

        elif token in frament_type_key:
            long_token = token
            try:
                while codeGenerator.peek() in frament_type_key:
                    long_token = f"{next(codeGenerator)} {long_token}"
            except StopIteration:
                pass
            print(long_token)
            return StringToEnum(long_token)

        token = next(codeGenerator)

    if len(token_list):
        token_list.reverse()
        newcodeGenerator = peekable(iter(token_list))
        return GetSubtype(newcodeGenerator, [])
    assert len(token_list) == 0
    return None


# token_count
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
            if token != "\n":
                token_list.append(token)
            if IsIdentifier(token):
                identifier_name = token_list.pop()
                id = identifier(GetSubtype(codeGenerator, token_list), identifier_name)
                all_identifier[id.annotated_name] = id
                return id
            token = next(codeGenerator)
    except StopIteration:
        pass

    return id


def ReadTypedef(codeGenerator: peekable) -> tuple[str, C_type]:
    token = next(codeGenerator)
    token_list = []
    id: identifier = None
    try:
        while token != ";":
            token_list.append(token)
            if IsIdentifier(token):
                identifier_name = token_list.pop()
                # id = identifier(GetSubtype(codeGenerator, token_list), token)
                # all_identifier[id.annotated_name] = id
                return identifier_name, GetSubtype(codeGenerator, token_list)
            token = next(codeGenerator)
    except StopIteration:
        pass

    return id


def Preprocessor(codeGenerator: peekable):
    temp = ""
    while codeGenerator.peek() != "#":
        temp = next(codeGenerator)

    pass


codes = ""
with open("b.h", "r") as fp:
    codes = fp.read()

    TokenGen(codes)
    # print(all_identifier)
    # print(all_identifier["a"])
# print(all)
for k, v in all_identifier.items():
    print(v)

print("typedef=============")
for k, v in typedef_dict.items():
    print(k, v)


class Lexer:
    all_type: dict[str, UserDefineType] = {}
    all_identifier: dict[str, identifier] = {}

    def __init__(self):

        pass
