from enum import Enum, auto
import random
import re
import string
from typing import Generator
from more_itertools import peekable
import uuid
import more_itertools
from functools import partial


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
    DEFINED_ENUM = auto()
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
        self,
        type_: build_in_type,
        aka: list[str],
        is_const_=False,
        is_volatile_=False,
    ):
        self.type = type_
        self.is_const = is_const_
        self.is_volatile = is_volatile_
        self.aka = []
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

    def is_cv(self) -> bool:
        return self.is_const and self.is_volatile


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
        typedef_name: str = "",
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        assert type_ is not None
        super().__init__(type_, is_const_, is_volatile_, aka)
        self.argument_dict = argument_dict
        self.typedef_name = typedef_name

    def __str__(self) -> str:
        fmtstr = f"{self.type}  {f"aka : {self.aka}" if len(self.aka) != 0 else ""}\nmember:{{\n{"\n".join([f"{k} : {v}" for k, v in self.argument_dict.items()])}\n}}"
        return fmtstr


# class C_struct(C_USER_DEFINED_TYPE):
#    def __init__(
#        self,
#        argument_dict: dict[str, C_type],
#        is_const_=False,
#        is_volatile_=False,
#        aka: str = "",
#    ):
#        super().__init__(
#            build_in_type.DEFINED_STRUCT, argument_dict, is_const_, is_volatile_, aka
#        )
#        # self.type = build_in_type.DEFINED_STRUCT
#
#
# class C_union(C_USER_DEFINED_TYPE):
#    def __init__(
#        self,
#        argument_dict: dict[str, C_type],
#        is_const_=False,
#        is_volatile_=False,
#        aka: str = "",
#    ):
#        super().__init__(
#            build_in_type.DEFINED_UNION, argument_dict, is_const_, is_volatile_, aka
#        )
#        # self.type = build_in_type.DEFINED_UNION
#
# class C_enum(C_USER_DEFINED_TYPE):
#    def __init__(
#        self,
#        argument_dict: dict[str, C_type],
#        is_const_=False,
#        is_volatile_=False,
#        aka: str = "",
#    ):
#        super().__init__(
#            build_in_type.DEFINED_UNION, argument_dict, is_const_, is_volatile_, aka
#        )


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

class RedefineType:
    def __init__(self, name : str, type_ : C_type):
        self.name = name
        self.type_ = type_


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


class Expression:
    expression_keyword = ["if", "while", "for", "do"]

    def __init__(self, mode_: str):
        pass

class Scope:
    def __init__(self):
        pass


class Declaration():
    def __init__(self):
        pass


class Expression():
    def __init__(self):
        pass

class Statement():
    def __init__(self):
        pass

class FunctionBody():
    def __init__(self):
        pass
        self.body = []




class Lexer:
    all_type: dict[str, C_type] = {}
    all_identifier: dict[str, identifier] = {}
    all_typedef: dict[str, C_type] = {}

    def __init__(self):
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

    def StringToEnum(self, type_str: str) -> build_in_type:
        match type_str:
            case "int":
                return build_in_type.INT
            case w if w in ["unsigned int", "int unsigned"]:
                return build_in_type.UNSIGNED_INT
            case "char":
                return build_in_type.CHAR
            case w if w in ["unsigned char", "char unsigned"]:
                return build_in_type.UNSIGNED_CHAR
            case w if w in ["signed char", "char signed"]:
                return build_in_type.SIGNED_CHAR
            case "short":
                return build_in_type.SHORT
            case w if w in ["unsigned short", "short unsigned"]:
                return build_in_type.UNSIGNED_SHORT
            case "long long":
                return build_in_type.LONG_LONG
            case w if w in ["unsigned long long", "long long unsigned"]:
                return build_in_type.UNSIGNED_LONG_LONG
            case "long":
                return build_in_type.LONG
            case w if w in ["unsigned long", "long unsigned"]:
                return build_in_type.UNSIGNED_LONG
            case "struct":
                return build_in_type.DEFINED_STRUCT
            case "union":
                return build_in_type.DEFINED_UNION

    def SrtToType(self, type_str: str) -> build_in_type:
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

    def is_c_type(self, code: str) -> bool:
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

    def cv_keyword(self, code: str) -> False:
        if code in ["const", "volatile"]:
            return True
        return False

    def GetType(self, codeGenerator: peekable, token_list: list[str]) -> C_type:
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
        while token not in [";", ","]:

            if token not in ["{", "}"]:
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
                    element_type = self.GetType(codeGenerator, token_list)
                #assert len(token_list) == 0, f"{token_list}"
                return C_build_in_array(array_size, element_type)

            elif token == "(":
                pass
                # break
            elif token == ")":
                in_parathesis = []
                token_list.pop()
                while len(token_list) and token_list[-1] != "(":
                    in_parathesis.append(token_list.pop())

                token_list.pop()
                while self.cv_keyword(codeGenerator):
                    temp_ = next(codeGenerator)
                    if temp_ == "const":
                        is_const_ = True

                    if temp_ == "volatile":
                        is_volatile_ = True

                #assert len(token_list) == 0, f"{token_list}"
                return C_build_in_pointer(
                    self.GetType(codeGenerator, token_list),
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
                    id = self.ReadDeclaration(codeGenerator)
                    if id is None and codeGenerator.peek() == "}":
                        break
                    argument_dict[id.annotated_name] = id
                    #token = codeGenerator.peek()
                #assert len(token_list) == 0, f"{token_list}"
                using_type_ = None
                if token_list[-1] == "struct":
                    using_type_ = build_in_type.DEFINED_STRUCT
                    token_list.pop()
                elif token_list[-1] == "union":
                    using_type_ = build_in_type.DEFINED_UNION
                    token_list.pop()
                elif token_list[-1] == "enum":
                    using_type_ = build_in_type.DEFINED_ENUM
                    token_list.pop()
                return C_USER_DEFINED_TYPE(using_type_, argument_dict)
            elif token == "*":
                if codeGenerator.peek() == "(":
                    pass
                current_type = C_build_in_pointer(
                    self.GetType(codeGenerator, token_list)
                )
                #assert len(token_list) == 0, f"{token_list}"
                return current_type

            elif token in self.frament_type_key:
                long_token = token
                try:
                    while codeGenerator.peek() in self.frament_type_key:
                        long_token = f"{next(codeGenerator)} {long_token}"
                except StopIteration:
                    pass
                #print(long_token)
                #assert len(token_list) == 0, f"{token_list}"
                return self.StringToEnum(long_token)

            token = next(codeGenerator)

        if len(token_list):
            token_list.reverse()
            newcodeGenerator = peekable(iter(token_list))
            return self.GetType(newcodeGenerator, [])
        #assert len(token_list) == 0
        return None

    def ReadDeclaration(self, codeGenerator: peekable) -> identifier:
        token = next(codeGenerator)
        token_list = []
        id: identifier = None
        try:
            while token != ";":
                if token != "\n":
                    token_list.append(token)
                if self.IsIdentifier(token):
                    identifier_name = token_list.pop()
                    
                    id = identifier(
                        self.GetType(codeGenerator, token_list), identifier_name
                    )
                    return id
                token = next(codeGenerator)
        except StopIteration:
            pass

        return id

    def ReadTypedef(self, codeGenerator: peekable, token_list : list[str]) -> tuple[str, C_type]:
        token = next(codeGenerator)
        id: identifier = None
        try:
            while token != ";":
                token_list.append(token)
                if self.IsIdentifier(token):
                    identifier_name = token_list.pop()
                    # id = identifier(GetSubtype(codeGenerator, token_list), token)
                    # all_identifier[id.annotated_name] = id
                    return identifier_name, self.GetType(codeGenerator, token_list)
                token = next(codeGenerator)
        except StopIteration:
            pass

        return id

    """ ignore preprocess """

    def StartDeleration(self, code: str) -> str:
        pass

    def IsIdentifier(self, code: str) -> False:
        if code in reserved_word:
            return False

        if code in self.all_identifier.keys():
            return False
        
        if code in self.all_type.keys():
            return False
        if (temp := re.search(r"(^[a-zA-Z_][\w_]*?$)", code)) is not None:
            temp = temp.group(0)
            if temp == code:
                return True
            else:
                return False
        else:
            return False




    def OmitToken(self, codes: str) -> Generator[str, any, any]:
        token = ""
        len_ = len(codes)
        i_ = 0
        while i_ < len_:
            while (
                i_ < len_
                and codes[i_]
                in "0123456789_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            ):
                token += codes[i_]
                i_ += 1

            if token != "":
                yield token
                token = ""
            if codes[i_] in ["\t", " ", "\b", "\n"]:
                pass
            elif codes[i_] == "#":
                while i_ < len_ and codes[i_] != "\n":
                    if codes[i_] == "\\":
                        i_ += 1
                    i_ += 1
            elif (
                codes[i_]
                not in "0123456789_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            ):
                yield codes[i_]
            i_ += 1

    #typedef_dict: dict[str, C_type] = {}


    def GenerateRandomName(self) -> str: 
        random_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        while random_name in self.all_type.keys():
            random_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        return random_name 
    
    def PrintGenerator(self, gen : Generator):
        try:
            while True:
                print(next(gen))
        except StopIteration:
            pass

    def TokenGen(self, codes: str):
        tokengen = peekable(self.OmitToken(codes))

        peek_token = tokengen.peek()
        typedef_name = ""
        temp_type = None
        had_typedef = False
        id_ = None
        save_token = []
        name_ = ""
        bind_func = None
        used_type_ = None
        token = ""
        try:
            while True:
                if peek_token == "typedef":
                    had_typedef = True

                if peek_token == "struct":
                    used_type_ = build_in_type.DEFINED_STRUCT
                    id_ = self.ReadDeclaration(tokengen)
                    self.all_identifier[id_.annotated_name] = id_
                    if had_typedef:
                        while (peek_token := tokengen.peek()) != ";":
                            self.all_typedef[peek_token] = id_
                            next(tokengen)
                        assert save_token.pop() == "typedef"
                        had_typedef = False
                    
                elif token == "union":
                    used_type_ = build_in_type.DEFINED_UNION
                    id_  = self.ReadDeclaration(tokengen)
                    self.all_identifier[id_.annotated_name] = id_
                elif token == "enum":
                    used_type_ = build_in_type.DEFINED_ENUM
                    id_ = self.ReadDeclaration(tokengen)

                    self.all_identifier[id_.annotated_name] = id_
                
                elif had_typedef and self.IsIdentifier(token):
                    if token in self.all_identifier.keys():
                        # EXPRESSION
                        pass
                    else:
                        if had_typedef:
                            #temp_type = 
                            self.all_type[token] = RedefineType(token, self.GetType(tokengen, save_token))
                            peek_token = tokengen.peek()

                            while (peek_token := tokengen.peek()) != ";":
                                self.all_typedef[token] = temp_type
                                next(tokengen)
                            had_typedef = False
                        else:
                            pass
                elif token in reserved_word:
                    typedef_name, new_type_ = self.ReadTypedef(tokengen, save_token)
                    self.all_typedef[typedef_name] = new_type_
                    pass


                if (used_type_ is not None and peek_token == "{"):
                    save_token.append(self.GenerateRandomName())
                
                if token == ";":
                    assert len(save_token) == 1 and save_token.pop() == ";"

                token = next(tokengen)
                save_token.append(peek_token)
                peek_token = tokengen.peek()
        except StopIteration:
            pass

    def ParseFile(self, filename: str):
        with open(filename, "r") as fp:
            codes = fp.read()
            self.TokenGen(codes)

        for k ,v in self.all_type.items():
            print(f"{k}, {v}")

def Preprocessor(codeGenerator: peekable):
    temp = ""
    while codeGenerator.peek() != "#":
        temp = next(codeGenerator)
    pass


if __name__ == "__main__":
    parser_ = Lexer()
    # parser_.To
    parser_.ParseFile("b.h")
