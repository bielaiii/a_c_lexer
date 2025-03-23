from operator import truediv
import random
import re
import string
import token
from tracemalloc import start
from typing import Generator
from webbrowser import get
import base_type
import reserved_word
from base_type import *
from type_class import *


class identifier:
    all_identifier: dict[str, "identifier"] = {}

    def __init__(self, typename: C_type, varname: str, val=None):
        self.type_: C_type = typename
        self.annotated_name = varname

        self.value: dict | int | str = val
        identifier.all_identifier[self.annotated_name] = self
        self.is_const = False
        self.is_volatile = False

        if self.type_.is_composite_type():
            self.value = self.type_.init_param_dict()
        elif self.type_.using_type == build_in_type.BUILD_IN_ARRAY:
            self.value = self.type_.init_param_dict()
        else:
            self.value = None

    def __str__(self) -> str:
        temp_str = ""
        if self.type_.is_composite_type():
            temp_str = f"name : {self.annotated_name}\ntype : {self.type_}\n"
        elif self.type_ == build_in_type.BUILD_IN_ARRAY:
            temp_str = f"name : {self.annotated_name}\ntype : {self.type_}\nval : "
            temp_str = f"{temp_str} {{{self.value.values()}}}"
            return temp_str
        else:
            temp_str = f"name : {self.annotated_name}\ntype : {self.type_}\nval : {self.value}\n"
        return temp_str

    def initialize_list(self, token_list: list[str], start_idx: int) -> int:
        if not isinstance(self.value, dict):
            self.value = token_list[start_idx]
            start_idx += 1
            return start_idx
        new_start = start_idx
        v_: C_type
        for k_, v_ in self.value.items():
            if isinstance(v_, dict):
                for kk_, vv_ in v_.items():
                    new_start = vv_.initialize_list(token_list, new_start)
            elif v_.type_.using_type == build_in_type.BUILD_IN_ARRAY:
                new_start = v_.initialize_list(token_list, new_start)
            else:

                v_.value = token_list[new_start]
                new_start += 1

        return new_start

    def print_value(self):
        if not isinstance(self.value, dict):
            return f"{self.annotated_name} = {self.value}"
        ret_str = []
        for k_, v_ in self.value.items():
            if isinstance(v_, dict):
                temp = []
                for kk_, vv_ in v_.items():
                    temp.append(f".{vv_.print_value()}")
                ret_str.append(f".{k_}={{{",".join(temp)}}}")
            else:
                ret_str.append(f".{v_.print_value()}")
        return f"{{{",".join(ret_str)}}}"

    def stringnify_value(self):
        if not self.type_.is_composite_type():
            return self.value
        elif self.type_ == build_in_type.BUILD_IN_POINTER:
            return f"nullptr"
        else:
            str_values = [x.stringnify_value for x in self.value.values()]
            return f"{{{",".join(str_values)} }}"

    def __setitem__(self, key: str, value):
        assert self.type_.is_composite_type()
        self.value[key] = value

    def __getitem__(self, key: str):
        assert self.type_.is_composite_type()
        return self.value[key]


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


init_list_type = list
key_dict_type = dict[str, any]


class Initialization:
    def __init__(self):
        pass

    def reader(
        self, token_list: list[str], start_idx: int
    ) -> tuple[init_list_type, key_dict_type]:
        len_ = len(token_list)
        val_list: list = []
        ket_dict: key_dict_type = {}
        while start_idx < len_:
            # if token_list[start_idx] == "{":
            # val_list.append
            if token_list[start_idx] == ".":
                start_idx += 1
                key = token_list[start_idx]
                start_idx += 1
                if token_list[start_idx] == "{":
                    ket_dict[key] = self.reader(token_list, start_idx)
                else:
                    ket_dict[key] = token_list[start_idx]
            else:
                if token_list[start_idx] == "{":
                    val_list.append(self.reader(token_list, start_idx))
                else:
                    val_list.append(token_list[start_idx])
                # val_list.append(token_list[start_idx])

            while start_idx < len_ and token_list[start_idx] != ",":
                start_idx += 1
            start_idx += 1

        return val_list, ket_dict


class FunctionBody:
    def __init__(self, name_ : str, return_type : C_type, argument_ : dict[str, identifier]):
        #pass
        self.body = []
        self.return_type : C_type = return_type
        self.argument_ = argument_
        self.name_ =    name_ 
    def __str__(self):
        return f"Function\n{self.return_type} {self.name_}({self.argument_})"


class Lexer:
    all_type: dict[str, C_type] = {}
    all_identifier: dict[str, identifier] = {}
    all_typedef: dict[str, C_type] = {}
    all_function : dict[str,FunctionBody ] = {}
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
        if code == "*":
            return True
        return False

    def cv_keyword(self, code: str) -> False:
        if code in ["const", "volatile"]:
            return True
        return False

    """ ignore preprocess """

    def StartDeleration(self, code: str) -> str:
        pass

    def is_identifier(self, code: str) -> False:
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

    def GenerateRandomName(self) -> str:
        random_name = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        while random_name in self.all_type.keys():
            random_name = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
            )
        return random_name

    def GetIdenfitiferIndex(self, token_list: list[str]):
        idx_ = 0
        len_ = len(token_list)
        while idx_ < len_:
            if (
                token_list[idx_] not in self.all_type.keys()
                and token_list[idx_] not in self.all_typedef.keys()
                and self.is_identifier(token_list[idx_])
            ):
                return idx_
            elif token_list[idx_ + 1] == "{" and token_list[idx_] in [
                "struct",
                "union",
                "enum",
            ]:
                return idx_
            idx_ += 1
    
    def is_fundamental_type(self, may_be_type : str)-> bool:
        return True if may_be_type in reserved_word.fundamental_type else False
        """         #may_be_type = token_list[i_]
        if may_be_type.startswith(("struct", "union", "enum", "unsigend", "long")):
            pass
        else:
            may_be_type = may_be_type.split(" ")[-1]
        if may_be_type in reserved_word.fundamental_type:
            return True
        elif CTypeFactory.part_of_name.append(may_be_type):
            assert may_be_type.startswith("struct", "union", "enum")
            return True
        return False """
        
        

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
                elif self.is_fundamental_type(" ".join(token_list[:left + 1])):
                    return C_type(token_list[left], "")
                elif self.all_typedef.keys():
                    return self.all_typedef[token_list[left]]
                elif left > 0 and f"{token_list[left - 1]} {token_list[left]}" in self.all_type.keys():
                    return self.all_type[f"{token_list[left - 1]} {token_list[left]}"]

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

                    # element_type =self.ReadRecleration2(token_list, left, right + 1)self.ReadRecleration2(token_list, left, right + 1)

                    return CTypeFactory.get_array(
                        self.ReadRecleration2(token_list, left, right + 1), array_size_
                    )

                elif token_list[right] == ")":
                    temp_type = self.ReadRecleration2(token_list, left, right)
                    pass
                elif token_list[right] == ";":
                    return self.ReadRecleration2(token_list, left, len_)

            if left >= 0:

                if token_list[left] == "*":
                    return CTypeFactory.get_pointer(
                        self.ReadRecleration2(token_list, left - 1, right)
                    )
                elif token_list[left] in reserved_word.frament_type_key:
                    if (
                        left - 1 >= 0
                        and token_list[left - 1] in reserved_word.frament_type_key
                    ):
                        return C_type(f"{token_list[left - 1]} {token_list[left]}")
                    return C_type(token_list[left])
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
            return member_field(token_lst[identifier_idx], temp_type)

    def read_another_typedef(self, i_: int, token_list: list[str], target_type: C_type):
        typedef_name = []
        i_ += 1
        len_ = len(token_list)
        while i_ < len_ and token_list[i_] != ";":
            if token_list[i_] == "*":
                i_ += 1
                self.all_typedef[token_list[i_]] = CTypeFactory.get_pointer(
                    CTypeFactory(target_type)
                )
            else:
                typedef_name.append(token_list[i_])
                self.all_typedef[token_list[i_]] = target_type
            i_ += 1

    def early_return(self, token_list: list[str]) -> bool:
        i_ = 0
        len_ = len(token_list)
        while i_ < len_ and token_list[i_] != "(":
            i_ += 1
        if i_ >= len_:
            return False
        i_ -= 1
        if not self.is_identifier(token_list[i_]):
            return False

        i_ -= 1

        if not (
            token_list[i_] in reserved_word.frament_type_key or token_list[i_] == "*"
        ):
            return False

        if (
            token_list[i_] == "*"
            and token_list[i_ - 1] in reserved_word.frament_type_key
        ):
            return True

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
                    i_ += 1
                    while i_ < len_ and codes[i_] != "\n":
                        i_ += 1
                    i_ += 1
                elif codes[i_ + 1] == "*":
                    i_ += 2
                    while i_ + 1 < len_ and codes[i_] != "*" and codes[i_ + 1] != "/":
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

            if i_ < len_ and codes[i_] == ";" and len(bracket_lst) == 0:
                yield ret_lst
                ret_lst = []
            
            # elif len(bracket_lst) == 0 and len(ret_lst):
            #    yield ret_lst
            #    ret_lst = []
            i_ += 1
        if len(ret_lst) != 0:
            yield ret_lst

    def ReadUserDefinedType(self, token_list: str):
        argument_dict: dict[str, identifier] = {}
        i_ = 0
        len_ = len(token_list)
        struct_name = ""
        user_define_ = ""
        while i_ < len_ and token_list[i_] != "{":
            if token_list[i_] == "struct" and token_list[i_ + 1] == "{":
                struct_name = self.GenerateRandomName()
            elif self.is_identifier(token_list[i_]) and token_list[i_ - 1] in [
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
            argument_dict[id_.name_] = id_
        assert user_define_ != "", "unknown type"

        ret_type = CTypeFactory.auto_call_method(
            user_define_, struct_name, argument_dict
        )
        self.read_another_typedef(i_, token_list, ret_type)
        # return ret_type

    def is_type_decleration(self, token_list: list[str]) -> bool:
        i_ = 0
        len_ = len(token_list)
        for i_ in range(len_):
            if token_list[i_] in ["union", "struct", "enum"]:
                i_ += 1
                if token_list[i_] == "{":
                    return True
                elif self.is_identifier(token_list[i_]):
                    if f"struct_{token_list[i_]}" not in self.all_type.keys():
                        return True
                return False
            if token_list[i_] in self.all_typedef.keys():
                return False
            if token_list[i_] == "typedef":
                return True
        return False
    
    def is_type(self, code : str):
        if code in reserved_word.frament_type_key:
            return True 
        if code in reserved_word.fundamental_type:
            return True
        
        if code in self.all_typedef.keys():
            return True
        
        user_define_ = ["struct", "enum", "union"]
        for u in user_define_:
            new_code = f"{u} {code}"
            if new_code in self.all_type.keys():
                return True
        return False
    
    def GetReturnType(self,token_list : list[str], idx : int ) -> C_type:
        #i_ = idx
        return_type = ""
        type_lst = token_list[:idx]
        #while idx > 0 and
        return_type = self.ReadRecleration2(type_lst, 0, 0)
        return return_type

    def ReadFunction(self, token_list : list[str], idx : int):
        i_ = idx
        len_ = len(token_list)
        while i_ < len_ and token_list[i_] != "(":
            i_ += 1
        #i_ -= 1
        i_ += 1
        argument_dict: dict[str, C_type] = {}
        while token_list[i_] != ")":
            temp_list = []
            while token_list[i_] not in [",", ")"]:
                temp_list.append(token_list[i_])
                i_ += 1
            if token_list[i_] != ")":
                i_ += 1
            identifier_idx = self.GetIdenfitiferIndex(temp_list)
            temp_type = self.ReadDeclerationList(temp_list, identifier_idx - 1, identifier_idx + 1)
            id_ = identifier(temp_type, temp_list[identifier_idx])
            argument_dict[id_.annotated_name] = id_
        return_type = self.GetReturnType(token_list, idx)
        i_ += 1

        bracket_lst = ["{"]
        i_ += 1
        codes_ = []
        while i_ < len_ and len(bracket_lst) != 0:
            if token_list[i_] in ( "{", "(", "["):
                bracket_lst.append(token_list[i_])
            elif token_list[i_] == "}" and bracket_lst[-1] == "{": 
                bracket_lst.pop()
            elif token_list[i_] == "]" and bracket_lst[-1] == "[": 
                bracket_lst.pop()
            elif token_list[i_] == "(" and bracket_lst[-1] == ")": 
                bracket_lst.pop()
            codes_.append(token_list[i_])
            i_ += 1
        i_ +=- 1 
        functor_ = FunctionBody(token_list[idx], return_type, argument_dict)
        self.all_function[functor_.name_] = functor_

        #self.all_function 
        return temp_type

    def is_function_decleration(self, token_list: list[str], identifier_idx : int):
        if token_list[identifier_idx + 1] == "(" and self.is_type(token_list[identifier_idx - 1]):
            return True
        return False
    def TokenDispatch(self, codes: str):

        sentence_gen = self.OmitToken(codes)
        for lst in sentence_gen:
            identifier_idx = self.GetIdenfitiferIndex(lst)
            print(lst)
            if self.is_type_decleration(lst):
                self.ReadUserDefinedType(lst)
                # self.all_type[temp_type.name] = temp_type

            elif self.is_function_decleration(lst, identifier_idx):
                self.ReadFunction(lst, identifier_idx)
                
                pass
            else:
                temp_type = self.ReadRecleration2(
                    lst, identifier_idx - 1, identifier_idx + 1
                )
                if lst[identifier_idx + 1] == "[":
                    #cur_identifier = self.all_identifier[lst[identifier_idx]]
                    #cur_identifier.type_ = temp_type
                    temp_size = 0
                    if lst[identifier_idx + 2] == "]":
                        temp_size = 10
                        
                    else:
                        temp_size = ""
                        identifier_idx += 2
                        while lst[identifier_idx] != "]":
                            #temp_size = temp_size * 10 + int(lst[identifier_idx + 2])
                            #identifier_idx += 1
                            temp_size+= lst[identifier_idx ]
                            identifier_idx += 1
                        identifier_idx += 1
                    
                    #temp_size = lst[identifier_idx + 1]
                    array_type = CTypeFactory.auto_call_method(build_in_type.BUILD_IN_ARRAY, temp_type, temp_size)

                    cur_identifier = identifier(array_type, lst[identifier_idx])
                else:
                    cur_identifier = identifier(temp_type, lst[identifier_idx])

                self.all_identifier[lst[identifier_idx]] = cur_identifier

        # val_list = [1, 2, 3, 4, 5, 6, 7, 8]
        # self.all_identifier["b"].initialize_list(val_list, 0)
        # print(self.all_identifier["b"].print_value())
        a = 1

    def ParseFile(self, filename: str):
        with open(filename, "r") as fp:
            codes = fp.read()
            self.TokenDispatch(codes)

        #for k, v in self.all_typedef.items():
        #    print(f"{k}, {v}")


if __name__ == "__main__":
    parser_ = Lexer()
    parser_.ParseFile("a.c")
