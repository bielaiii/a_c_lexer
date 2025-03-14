from enum import Enum, auto
import random
import re
import string
from typing import Generator
from more_itertools import peekable
import uuid
import more_itertools
from functools import partial
import reserved_word
from base_type import *
from type_class import *


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
    
    def initialize_list(self, token_list[str]):
        lebn 
        for token_ in token_list:
            if token_ == ",":
                continue
            if token_ == "=":
                continue
            if token_ == ";":
                continue
            self.value.append(token_)

            
        


class RedefineType:
    def __init__(self, name: str, type_: C_type):
        self.name = name
        self.type_ = type_


class Expression:
    expression_keyword = ["if", "while", "for", "do"]

    def __init__(self, mode_: str):
        pass


class Scope:
    def __init__(self):
        pass


class Declaration:
    def __init__(self):
        pass

    def TypeDeclaration(self):

        pass


class Expression:
    def __init__(self):
        pass


class Statement:
    def __init__(self):
        pass


class FunctionBody:
    def __init__(self):
        pass
        self.body = []


class Lexer:
    all_type: dict[str, C_type] = {}
    all_identifier: dict[str, identifier] = {}
    all_typedef: dict[str, C_type] = {}

    def __init__(self):
        pass

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
        while codeGenerator.peek() not in [";", ","]:

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
                # assert len(token_list) == 0, f"{token_list}"
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

                # assert len(token_list) == 0, f"{token_list}"
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

                using_type_ = None
                if len(token_list):
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
                return current_type

            elif token in reserved_word.frament_type_key:
                long_token = token
                try:
                    while codeGenerator.peek() in reserved_word.frament_type_key:
                        long_token = f"{next(codeGenerator)} {long_token}"
                except StopIteration:
                    pass

                return self.StringToEnum(long_token)

            token = next(codeGenerator)

        if len(token_list):
            token_list.reverse()
            newcodeGenerator = peekable(iter(token_list))
            token_list = []
            return self.GetType(newcodeGenerator, [])

        return None

    def ReadDeclaration(self, codeGenerator: peekable) -> identifier:
        token = next(codeGenerator)
        token_list = []
        id: identifier = None
        while token != ";":
            if token != "\n":
                token_list.append(token)
            if self.IsIdentifier(token):
                identifier_name = token_list.pop()

                id = identifier(
                    self.GetType(codeGenerator, token_list), identifier_name
                )
                try:
                    token = next(codeGenerator)
                    while token != ";":
                        if token == "const":
                            id.is_const = True
                        elif token == "volatile":
                            id.is_volatile = True
                        else:
                            raise AssertionError("looks something is incorrect")
                    return id
                except StopIteration:
                    return id
            token = next(codeGenerator)

        return id

    def ReadTypedef(
        self, codeGenerator: peekable, token_list: list[str]
    ) -> tuple[str, C_type]:
        token = next(codeGenerator)
        id: identifier = None
        try:
            while token != ";":
                token_list.append(token)
                if self.IsIdentifier(token):
                    identifier_name = token_list.pop()

                    return identifier_name, self.GetType(codeGenerator, token_list)
                token = next(codeGenerator)
        except StopIteration:
            pass

        return id

    """ ignore preprocess """

    def StartDeleration(self, code: str) -> str:
        pass

    def IsIdentifier(self, code: str) -> False:
        if code in reserved_word.reserved_word:
            return False

        if code in self.all_identifier.keys():
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
        ret_lst: list[str] = []
        bracket_lst: list[str] = []
        while i_ < len_:
            while (
                i_ < len_
                and codes[i_]
                in "0123456789_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            ):
                token += codes[i_]
                i_ += 1

            if token != "":
                # yield token
                ret_lst.append(token)
                token = ""
            if codes[i_] in ["\t", " ", "\b", "\n"]:
                pass
            elif codes[i_] == "#":
                while i_ < len_ and codes[i_] != "\n":
                    if codes[i_] == "\\":
                        i_ += 1
                    i_ += 1
            elif codes[i_] == "/":
                if codes[i_ + 1] == "/":
                    while i_ < len_ and codes[i_] != "\n":
                        i_ += 1
                    i_ += 1
                elif codes[i_ + 1] == "*":
                    while i_ < len_ and codes[i_] != "*" and codes[i_ + 1] != "/":
                        i_ += 1
                    i_ += 2
                continue
            elif "{" == codes[i_]:
                bracket_lst.append("{")
                ret_lst.append(codes[i_])
            elif "}" == codes[i_]:
                bracket_lst.pop()
                ret_lst.append(codes[i_])
            elif (
                codes[i_]
                not in "0123456789_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            ):
                ret_lst.append(codes[i_])
                # yield codes[i_]

            if codes[i_] == ";" and len(bracket_lst) == 0:
                # yield codes[i_]
                a = 0
                yield ret_lst

                ret_lst = []
            i_ += 1

    def OmitSentence(self, codes: str) -> Generator[peekable, any, any]:
        token = peekable(self.OmitToken(codes))
        lst: list[str] = []
        record_scope: list[str] = ["("]
        try:
            while (peek_ := token.peek()) != "":
                while (
                    token.peek() != ";"
                    and (len(record_scope) != 0 and record_scope[-1] != "}")
                    # or (len(lst) != 0 and lst[-1] != ";")
                ):
                    if peek_ == "{":
                        record_scope.append("{")
                    elif peek_ == "}":
                        if record_scope[-1] == "{":
                            record_scope.pop()
                    lst.append(next(token))
                    # lst.append(next(token))

                yield peekable(lst)
                lst = []
        except StopIteration:
            pass

    def GenerateRandomName(self) -> str:
        random_name = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        while random_name in self.all_type.keys():
            random_name = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
            )
        return random_name

    def PrintGenerator(self, gen: Generator):
        token = next(gen)
        while token != "":
            print(token)
            token = next(gen)

    def ConcatTwo(self, lst: list, gen: peekable) -> Generator:
        new_gen = peekable(lst)
        for l in new_gen:

            yield l
        lst = []
        for l in gen:
            yield l

    def GeneratorToToken(self, tokengen: list[str]):
        typedef_name = ""
        temp_type = None
        id_ = None
        save_token = []
        name_ = ""
        bind_func = None
        used_type_ = None
        peek_token = tokengen.peek()
        token_list: list[str] = []
        is_typing = False
        name_ = ""
        define_type = False
        left = 0
        right = 0
        token = tokengen.peek()
        # try:
        while tokengen:
            if self.IsIdentifier(token):
                name_ = token
            elif token == "struct":
                next(tokengen)
                if (peek_ := tokengen.peek()) == "{" or (
                    self.IsIdentifier(peek_)
                    and (
                        peek_
                        not in reserved_word.fundamental_type.keys()
                        # or peek_ not in self.all_identifier.keys()
                    )
                ):
                    using_type = build_in_type.DEFINED_STRUCT
                    id_ = next(tokengen)
                    if id_ == "{":
                        id_ = self.GenerateRandomName()
                    argument_dict = {}
                    while token != "}":
                        id_ = self.ReadDeclaration(tokengen)
                        argument_dict[id_.annotated_name] = id_
                        token = next(tokengen)

                    self.all_type[id_] = C_USER_DEFINED_TYPE(
                        using_type, f"struct::{name_}", argument_dict
                    )

                    self.ReadDeclaration(tokengen)
            elif token == "union":
                using_type = build_in_type.DEFINED_UNION
            elif token == "enum":
                using_type = build_in_type.DEFINED_ENUM

            if define_type:
                new_type = self.ReadDeclaration()

            if self.IsIdentifier(token):
                if token in self.all_identifier.keys():
                    # no decleration
                    pass
                else:
                    self.ReadDeclaration(tokengen)

            # token = next(tokengen)
            token_list.append(peek_token)
            next(tokengen)
            token = tokengen.peek()
        # except StopIteration:
        #    raise AssertionError("what can be return")

    def PrintPeekable(self, pr_: peekable):
        try:
            while True:

                print(pr_.peek())
                next(pr_)
        except StopIteration:
            print("=================")

    def GetIdenfitiferIndex(self, token_list: list[str]):
        idx_ = 0
        len_ = len(token_list)
        while idx_ < len_:
            if (
                token_list[idx_] not in self.all_type.keys()
                and token_list[idx_] not in self.all_typedef.keys()
                and self.IsIdentifier(token_list[idx_])
            ):
                return idx_
            elif token_list[idx_ + 1] == "{" and token_list[idx_] in [
                "struct",
                "union",
                "enum",
            ]:
                return idx_
            idx_ += 1

    def ReadDeclerationList(self, token_list: list[str], left: int, right: int):
        len_ = len(token_list)
        while right < len_ or left >= 0:
            while right < len_:
                if token_list[right] == "(":
                    assert (
                        token_list[left] in reserved_word
                        or token_list[left] in self.all_type.keys()
                        or token_list[left] == "*"
                    ), f"{token_list[left]} is unexpected"
                    if token_list[left] == "*":
                        # function pointer
                        pass
                    else:
                        pass
                elif token_list[right] == "[":
                    array_size_ = ""
                    while right < len_ and token_list[right] != "]":
                        array_size_ += token_list[right]
                        right += 1
                    return C_build_in_array(
                        array_size_, self.ReadDeclerationList(token_list, left, right)
                    )
                elif token_list[right] == ")":
                    temp_type = self.ReadDeclerationList(token_list, left, len_ + 1)

                    pass
                right += 1
            if left >= 0:

                if token_list[left] == "*":
                    return C_build_in_pointer(
                        self.ReadDeclerationList(token_list, left - 1, right)
                    )
                elif token_list[left] in reserved_word:
                    return C_type(token_list[left], "")

    def ReadRecleration2(self, token_list: list[str], left: int, right: int):
        len_ = len(token_list)

        i_ = 0
        while right < len_ or left >= 0:
            if (
                right < len_
                and left >= 0
                and token_list[right] == ")"
                and token_list[left] == "("
            ):
                right += 1
                left -= 1
            if right < len_ and token_list[right] != ")":
                if token_list[right] == "(":
                    assert (
                        token_list[left] in reserved_word
                        or token_list[left] in self.all_type.keys()
                        or token_list[left] == "*"
                    ), f"{token_list[left]} is unexpected"
                    if token_list[left] == "*":
                        # function pointer
                        pass
                    else:
                        pass
                elif token_list[right] == "[":
                    array_size_ = ""
                    right += 1
                    while right < len_ and token_list[right] != "]":
                        array_size_ += token_list[right]
                        right += 1
                    return C_build_in_array(
                        array_size_, self.ReadRecleration2(token_list, left, right + 1)
                    )
                elif token_list[right] == ")":
                    temp_type = self.ReadRecleration2(token_list, left, right)
                    pass
                elif token_list[right] == ";":
                    return self.ReadRecleration2(token_list, left, len_)

            if left >= 0:

                if token_list[left] == "*":
                    return C_build_in_pointer(
                        self.ReadRecleration2(token_list, left - 1, right)
                    )
                elif token_list[left] in reserved_word.reserved_word:
                    return C_type(token_list[left], "")
                elif (
                    token_list[left] in self.all_type.keys()
                    or token_list[left] in self.all_typedef.keys()
                ):
                    a = 0
                    temp_type = None
                    if token_list[left] in self.all_type.keys():
                        temp_type = self.all_type[token_list[left]]
                    else:
                        temp_type = self.all_typedef[token_list[left]]
                    return temp_type

    def ReadIdDecleration(self, token_lst: list[str]):
        identifier_idx = self.GetIdenfitiferIndex(token_lst)
        if token_lst[identifier_idx] in ["union", "struct", "enum"]:
            self.ReadUserDefinedType(token_lst)
        else:
            temp_type = self.ReadRecleration2(
                token_lst, identifier_idx - 1, identifier_idx + 1
            )
            return identifier(temp_type, token_lst[identifier_idx])

    def ReadUserDefinedType(self, token_list: str):
        argument_dict: dict[str, identifier] = {}
        i_ = 0
        len_ = len(token_list)
        struct_name = ""
        user_define_ = ""
        while i_ < len_ and token_list[i_] != "{":
            if token_list[i_] == "struct" and token_list[i_ + 1] == "{":
                struct_name = self.GenerateRandomName()
            elif self.IsIdentifier(token_list[i_]) and token_list[i_ - 1] in [
                "union",
                "enum",
                "struct",
            ]:
                struct_name = token_list[i_]

            if token_list[i_] == "struct":
                user_define_ = build_in_type.DEFINED_STRUCT
            elif token_list[i_] == "union":
                user_define_ = build_in_type.DEFINED_UNION
            elif token_list[i_] == "enum":
                user_define_ = build_in_type.DEFINED_ENUM
            i_ += 1
        i_ += 1
        while i_ < len_ and token_list[i_] != "}":
            r = i_
            while r < len_ and token_list[r] != ";":
                r += 1
            temp_list = token_list[i_ : r + 1]
            i_ = r + 1
            id_ = self.ReadIdDecleration(temp_list)
            argument_dict[id_.annotated_name] = id_
        assert user_define_ != "", "unknown type"

        typedef_name = []
        i_ += 1
        while i_ < len_ and token_list[i_] != ";":
            if token_list[i_] == "*":
                i_ += 1
                typedef_name.append(f"ptr_of_{token_list[i_]}")
            else:
                typedef_name.append(token_list[i_])
            i_ += 1

        return C_USER_DEFINED_TYPE(
            user_define_, struct_name, argument_dict, typedef_name=typedef_name
        )

    def is_type_decleration(self, token_list: list[str]) -> bool:
        i_ = 0
        len_ = len(token_list)
        for i_ in range(len_):
            if token_list[i_] in ["union", "struct", "enum"]:
                i_ += 1
                if i_ == "{":
                    return True
                elif self.IsIdentifier(token_list[i_]):
                    if f"struct_{token_list[i_]}" not in self.all_type.keys():
                        return True
                return False
            if token_list[i_] in self.all_typedef.keys():
                return True
        return False

    def TokenDispatch(self, codes: str):

        sentence_gen = self.OmitToken(codes)
        for lst in sentence_gen:
            identifier_idx = self.GetIdenfitiferIndex(lst)
            if self.is_type_decleration(lst):
                temp_type = self.ReadUserDefinedType(lst)
                self.all_type[temp_type.name] = temp_type
                if len(temp_type.typedef_name):

                    for t_ in temp_type.typedef_name:
                        self.all_typedef[t_] = temp_type
                    temp_type.aka = ""
            else:
                temp_type = self.ReadRecleration2(
                    lst, identifier_idx - 1, identifier_idx + 1
                )
                self.all_identifier[lst[identifier_idx]] = identifier(
                    temp_type, lst[identifier_idx]
                )

        """ for k, v in self.all_identifier.items():
            print(v)
            print("=========================") """

        for k, v in self.all_type.items():
            print(v)
            print("=============================")

    def ParseFile(self, filename: str):
        with open(filename, "r") as fp:
            codes = fp.read()
            self.TokenDispatch(codes)

        for k, v in self.all_type.items():
            print(f"{k}, {v}")


def Preprocessor(codeGenerator: peekable):
    temp = ""
    while codeGenerator.peek() != "#":
        temp = next(codeGenerator)
    pass


if __name__ == "__main__":
    parser_ = Lexer()
    parser_.ParseFile("a.c")
