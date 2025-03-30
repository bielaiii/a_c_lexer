from operator import truediv
import queue
import random
import re
import stat
import string
import token
from typing import Deque, Generator
import base_type
import reserved_word
from base_type import *
from type_class import *
from collections import deque


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
        elif self.type_.using_type == build_in_type.BUILD_IN_POINTER and (self.type_.subtype.is_composite_type() or self.type_.subtype.using_type == build_in_type.BUILD_IN_ARRAY):
            self.value = self.type_.subtype.init_param_dict()
        else:
            self.value = None
        
        a = 1

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

    def __setitem__(self, key: str | int | Deque, value):
        if isinstance(key, Deque)and len(key) > 0: 
            v_ = key.popleft()#
            if len(key) == 1:
                self.value = value
            else:
                self.value[v_][key] = value
        else:
            assert not self.type_.is_composite_type()
            if isinstance(key, Deque):
                key = key.popleft()
            self.value[key] = value

    def __getitem__(self, key: str | int | Deque):
        if isinstance(key, Deque) : 
            if len(key) == 1:
                return self.value[key.popleft()]
            val_ = key.popleft()
            return self.value[val_][key]
        else:
            assert self.type_.is_composite_type()
            return self.value[key]
    
    def is_chain_chain_identifier(self, tokens : Deque):
        #if self.type_.
        if self.type_.is_composite_type():
            if (len(tokens) == 1) and tokens[0] == self.annotated_name:
                return True
            else:
                #return False
                self.is_chain_chain_identifier(tokens.popleft())
        else:
            return True
        #pass


class RedefineType:
    def __init__(self, name: str, type_: C_type):
        self.name = name
        self.type_ = type_


class Expression:
    expression_keyword = ["if", "while", "for", "do"]

    def __init__(self, mode_: str):
        pass

    def is_assignment(self, tokens: list[str]):

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
        self.idx = 0
        self.if_statememt: dict[int, list[str]] = {}
        self.while_statememt: dict[int, list[str]] = {}
        self.for_statememt: dict[int, list[str]] = {}

        self.not_compound_statement : list[list[str]] = []

        #self.not_coumpound_stated = 

        self.statement_: dict[str, dict[int, list[str]]] = {}

    # todo: no {}
    def consume_statement_impl(self, tokens: list[str], i_: int):
        temp_dict = {}
        if len(tokens) == 0:
            return
        if tokens[i_] == "if":
            # i_ += 2
            temp_dict = self.if_statememt
        elif token[i_] == "for":
            # i_ += 3
            temp_dict = self.for_statememt
        elif tokens[i_] == "while":
            # i_ += 5
            temp_dict = self.while_statememt
        else:
            return

        i_ += 1
        brackets = []
        brackets.append(")")
        i_ += 1
        save_ = ["("]
        while len(brackets) != 0:
            if tokens[i_] == "{":
                brackets.append("}")
            elif tokens[i_] == "[":
                brackets.append("]")
            elif tokens[i_] == "(":
                brackets.append(")")
            elif tokens[i_] in ["}", ")", "]"]:
                if brackets[-1] == tokens[i_]:
                    brackets.pop()
                else:
                    raise AssertionError(f"{tokens[i_]} is unexpected")

                if tokens[i_] == "{":
                    if tokens[i_] == "{":
                        brackets.append("}")
                    elif tokens[i_] == "[":
                        brackets.append("]")
                    elif tokens[i_] == "(":
                        brackets.append(")")
            save_.append(tokens[i_])
            i_ += 1
        temp_dict[self.idx] = save_
        return i_
    
    def consume_statement(self, tokens: list[str], i_: int):
        len_ = len(tokens)
        ret = []
        while i_ < len_:
            if tokens[i_] in ["if", "for", "while"]:
                i_ = self.consume_statement_impl(tokens, i_)
            else:
                codes = []
                while i_ < len_ and tokens[i_] != ";":
                    codes.append(tokens[i_])
                    i_ += 1
                ret.append(codes)
            i_ += 1
        self.not_compound_statement = ret
        #return ret


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
    def __init__(
        self,
        name_: str,
        return_type: C_type,
        argument_: dict[str, identifier],
        body: list[str],
    ):
        self.body = body
        self.return_type: C_type = return_type
        self.argument_ = argument_
        self.name_ = name_
        self.statement_: Statement = Statement()
        self.stated_id: dict[str, identifier] = {}
        self.statement_.consume_statement(self.body, 0)

        #test_code = ['b', '->', 'f_', '.', 'a', '=', ['a', '.', 'a']
        val1 = Deque(['a'])
        val2 = Deque(["0x123"])
        self.argument_["a"][val1] = 0x123
        val1 = Deque(['f_',  'a'])
        val2 = Deque(['a'])
        self.argument_["b"][val1] = self.argument_["a"][val2]
        for k_, v_ in self.argument_.items():
            self.stated_id[k_] = v_

    def __str__(self):
        return f"Function\n{self.return_type} {self.name_}({",".join(f"{v_.annotated_name}: {v_.type_}" for v_ in self.argument_.values())})"

    def retrieveing(self, que: Deque, id_: identifier):
        if len(que) == 1:
            return id_.value

        k_ = que.popleft()
        v_ = id_.value[k_]
        assert que.popleft() in ["->", "."]
        self.is_assignment(que, v_)
    
    def is_lieral(self, codes: str):
        if (temp := re.search("\d+", codes)) is not None:
            if temp.group(1) == len(codes):
                return True
        elif (temp := re.search("0x[0-9abcedfABCEDF]+", codes)) is not None:
            if temp.group(1) == len(codes):
                return True
        elif (temp := re.search("0[01234567]+", codes)) is not None:
            if temp.group(1) == len(codes):
                return True
        elif (temp := re.search("0b[01]+", codes)) is not None:
            if temp.group(1) == len(codes):
                return True
        elif (temp := re.search("[\d+]+\.[\d+]+f?", codes)) is not None:
            if temp.group(1) == len(codes):
                return True
        elif (temp := re.search("(\".*?\"|\'.*?\')", codes)) is not None:
            if temp.group(1) == len(codes):
                return True
        return False


    def signing(self, que: Deque, val: int | str, id_: identifier) -> None:
        if len(que) == 1:
            id_.value = val
            return
        k_ = que.popleft()
        v_ = id_.value[k_]
        assert que.popleft() in ["->", "."]
        self.is_assignment(que, v_)
    
    def is_assignment(self,tokens : list[str]):
        if "=" not in tokens:
            return False
    
    def reading_assignment(self):
        pass
        

    def read_simple_assignment(self, tokens: list[str], i_: int):
        len_ = len(tokens)


class Lexer:
    all_type: dict[str, C_type] = {}
    all_identifier: dict[str, identifier] = {}
    all_typedef: dict[str, C_type] = {}
    all_function: dict[str, FunctionBody] = {}

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

    def StartDeleration(self, code: str) -> str:
        pass

    def is_new_identifier(self, code: str) -> False:
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

    def GetIdenfitiferIndex(self, tokens: list[str]):
        i_ = 0
        len_ = len(tokens)
        while i_ < len_:
            if tokens[i_] in reserved_word.frament_type_key:
                pass
            elif tokens[i_] in reserved_word.fundamental_type:
                pass
            elif tokens[i_] in self.all_type.keys():
                pass
            elif tokens[i_] in self.all_typedef.keys():
                pass
            elif self.is_new_identifier(tokens[i_]):
                # and not self.is_identifier(tokens[i_])
                return i_
            elif tokens[i_] == "{" and tokens[i_ - 1] in [
                "struct",
                "union",
                "enum",
            ]:
                return i_
            i_ += 1
        return i_

    def is_fundamental_type(self, may_be_type: str) -> bool:
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

    def ReadDeclerationList(self, tokens: list[str], left: int, right: int):
        len_ = len(tokens)
        while right < len_ or left >= 0:
            while right < len_:
                if tokens[right] == "(":
                    assert (
                        tokens[left] in reserved_word
                        or tokens[left] in self.all_type.keys()
                        or tokens[left] == "*"
                    ), f"{tokens[left]} is unexpected"
                    if tokens[left] == "*":
                        # function pointer
                        pass
                    else:
                        pass
                elif tokens[right] == "[":
                    array_size_ = ""
                    while right < len_ and tokens[right] != "]":
                        array_size_ += tokens[right]
                        right += 1
                    return C_build_in_array(
                        array_size_, self.ReadDeclerationList(tokens, left, right)
                    )
                elif tokens[right] == ")":
                    temp_type = self.ReadDeclerationList(tokens, left, len_ + 1)

                    pass
                right += 1
            if left >= 0:

                if tokens[left] == "*":
                    return C_build_in_pointer(
                        self.ReadDeclerationList(tokens, left - 1, right)
                    )
                elif self.is_fundamental_type(" ".join(tokens[: left + 1])):
                    return C_type(tokens[left], "")
                elif self.all_typedef.keys():
                    return self.all_typedef[tokens[left]]
                elif (
                    left > 0
                    and f"{tokens[left - 1]} {tokens[left]}" in self.all_type.keys()
                ):
                    return self.all_type[f"{tokens[left - 1]} {tokens[left]}"]

    def ReadRecleration2(self, tokens: list[str], left: int, right: int):
        len_ = len(tokens)

        i_ = 0
        while right < len_ or left >= 0:
            if (
                right < len_
                and left >= 0
                and tokens[right] == ")"
                and tokens[left] == "("
            ):
                right += 1
                left -= 1
            if right < len_ and tokens[right] != ")":
                if tokens[right] == "(":
                    assert (
                        tokens[left] in reserved_word
                        or tokens[left] in self.all_type.keys()
                        or tokens[left] == "*"
                    ), f"{tokens[left]} is unexpected"
                    if tokens[left] == "*":
                        # function pointer
                        pass
                    else:
                        pass
                elif tokens[right] == "[":
                    array_size_ = ""
                    right += 1
                    while right < len_ and tokens[right] != "]":
                        array_size_ += tokens[right]
                        right += 1

                    # element_type =self.ReadRecleration2(token_list, left, right + 1)self.ReadRecleration2(token_list, left, right + 1)

                    return CTypeFactory.get_array(
                        self.ReadRecleration2(tokens, left, right + 1), array_size_
                    )

                elif tokens[right] == ")":
                    temp_type = self.ReadRecleration2(tokens, left, right)
                    pass
                elif tokens[right] == ";":
                    return self.ReadRecleration2(tokens, left, len_)

            if left >= 0:

                if tokens[left] == "*":
                    return CTypeFactory.get_pointer(
                        self.ReadRecleration2(tokens, left - 1, right)
                    )
                elif tokens[left] in reserved_word.frament_type_key:
                    if (
                        left - 1 >= 0
                        and tokens[left - 1] in reserved_word.frament_type_key
                    ):
                        return C_type(f"{tokens[left - 1]} {tokens[left]}")
                    return C_type(tokens[left])
                elif (
                    tokens[left] in self.all_type.keys()
                    or tokens[left] in self.all_typedef.keys()
                ):
                    a = 0
                    temp_type = None
                    if tokens[left] in self.all_type.keys():
                        temp_type = self.all_type[tokens[left]]
                    else:
                        temp_type = self.all_typedef[tokens[left]]
                    return temp_type

    def ReadIdDecleration(self, tokens: list[str]):
        identifier_idx = self.GetIdenfitiferIndex(tokens)
        if tokens[identifier_idx] in ["union", "struct", "enum"]:
            self.ReadUserDefinedType(tokens)
        else:
            temp_type = self.ReadRecleration2(
                tokens, identifier_idx - 1, identifier_idx + 1
            )
            return member_field(tokens[identifier_idx], temp_type)

    def read_another_typedef(self, i_: int, tokens: list[str], target_type: C_type):
        typedef_name = []
        i_ += 1
        len_ = len(tokens)
        while i_ < len_ and tokens[i_] != ";":
            if tokens[i_] == "*":
                i_ += 1
                self.all_typedef[tokens[i_]] = CTypeFactory.get_pointer(
                    CTypeFactory(target_type)
                )
            else:
                typedef_name.append(tokens[i_])
                self.all_typedef[tokens[i_]] = target_type
            i_ += 1

    def early_return(self, tokens: list[str]) -> bool:
        i_ = 0
        len_ = len(tokens)
        while i_ < len_ and tokens[i_] != "(":
            i_ += 1
        if i_ >= len_:
            return False
        i_ -= 1
        if not self.is_new_identifier(tokens[i_]):
            return False

        i_ -= 1

        if not (tokens[i_] in reserved_word.frament_type_key or tokens[i_] == "*"):
            return False

        if tokens[i_] == "*" and tokens[i_ - 1] in reserved_word.frament_type_key:
            return True

    def consume_preprocess(self, tokens: list[str], i_: int) -> list[str]:
        if (
            tokens[i_ : i_ + 3] == "#if"
            or tokens[i_ : i_ + 7] == "#define"
            or tokens[i_ : i_ + 6] == "#endif"
            or tokens[i_ : i_ + 8] == "#include"
            or tokens[i_ : i_ + 5] == "#else"
        ):
            while tokens[i_] != "\n":
                i_ += 1
                if tokens[i_] == "\\":
                    i_ += 2
        return i_

    def consume_comments(self, tokens: list[str], i_: int) -> int:
        len_ = len(tokens)
        if tokens[i_ + 1] == "/":
            i_ += 1
            while i_ < len_ and tokens[i_] != "\n":
                i_ += 1
            i_ += 1
        elif tokens[i_ + 1] == "*":
            i_ += 2
            while i_ + 1 < len_:
                i_ += 1
                if tokens[i_] == "*" and tokens[i_ + 1] == "/":
                    break
            i_ += 2
        return i_

    def OmitToken(self, codes: str) -> Generator[str, any, any]:
        token = ""
        len_ = len(codes)
        i_ = 0
        ret_lst: list[str] = []
        bracket_lst: list[str] = []
        while i_ < len_:
            while codes[i_] == "_" or codes[i_].isalnum():
                token += codes[i_]
                i_ += 1
            if token != "":
                ret_lst.append(token)
                token = ""
            if codes[i_] in ["\t", " ", "\b", "\n"]:
                pass
            elif codes[i_] == "#":
                i_ = self.consume_preprocess(codes, i_)
            elif codes[i_ : i_ + 2] in ["//", "/*"]:
                i_ = self.consume_comments(codes, i_)
                continue
            elif "{" == codes[i_]:
                bracket_lst.append("{")
                ret_lst.append(codes[i_])
            elif "}" == codes[i_]:
                if bracket_lst[-1] == "{":
                    bracket_lst.pop()
                ret_lst.append(codes[i_])
            elif ">" == codes[i_] and codes[i_ - 1] == "-":
                ret_lst.pop()
                ret_lst.append("->")
            elif (
                codes[i_]
                not in "0123456789_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            ):
                ret_lst.append(codes[i_])

            if i_ < len_ and codes[i_] == ";" and len(bracket_lst) == 0:
                yield ret_lst
                ret_lst = []

            i_ += 1
        if len(ret_lst) != 0:
            yield ret_lst

    def ReadUserDefinedType(self, tokens: str):
        argument_dict: dict[str, identifier] = {}
        i_ = 0
        len_ = len(tokens)
        struct_name = ""
        user_define_ = ""
        while i_ < len_ and tokens[i_] != "{":
            if tokens[i_] == "struct" and tokens[i_ + 1] == "{":
                struct_name = self.GenerateRandomName()
            elif self.is_new_identifier(tokens[i_]) and tokens[i_ - 1] in [
                "union",
                "enum",
                "struct",
            ]:
                struct_name = tokens[i_]

            if tokens[i_] == "struct":
                user_define_ = build_in_type.DEFINED_STRUCT
            elif tokens[i_] == "union":
                user_define_ = build_in_type.DEFINED_UNION
            elif tokens[i_] == "enum":
                user_define_ = build_in_type.DEFINED_ENUM
            i_ += 1
        i_ += 1
        while i_ < len_ and tokens[i_] != "}":
            r = i_
            while r < len_ and tokens[r] != ";":
                r += 1
            temp_list = tokens[i_ : r + 1]
            i_ = r + 1
            id_ = self.ReadIdDecleration(temp_list)
            argument_dict[id_.name_] = id_
        assert user_define_ != "", "unknown type"

        ret_type = CTypeFactory.auto_call_method(
            user_define_, struct_name, argument_dict
        )
        self.read_another_typedef(i_, tokens, ret_type)
        # return ret_type

    def is_type_decleration(self, token_list: list[str]) -> bool:
        i_ = 0
        len_ = len(token_list)
        for i_ in range(len_):
            if token_list[i_] in ["union", "struct", "enum"]:
                i_ += 1
                if token_list[i_] == "{":
                    return True
                elif self.is_new_identifier(token_list[i_]):
                    if f"struct_{token_list[i_]}" not in self.all_type.keys():
                        return True
                return False
            if token_list[i_] in self.all_typedef.keys():
                return False
            if token_list[i_] == "typedef":
                return True
        return False

    def is_type(self, code: str):
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

    def GetReturnType(self, tokens: list[str], idx: int) -> C_type:
        # i_ = idx
        return_type = ""
        type_lst = tokens[:idx]
        # while idx > 0 and
        return_type = self.ReadRecleration2(type_lst, 0, 0)
        return return_type

    def ReadFunction(self, tokens: list[str], idx: int):
        i_ = idx
        len_ = len(tokens)
        while i_ < len_ and tokens[i_] != "(":
            i_ += 1
        # i_ -= 1
        i_ += 1
        argument_dict: dict[str, C_type] = {}
        while tokens[i_] != ")":
            temp_list = []
            while tokens[i_] not in [",", ")"]:
                temp_list.append(tokens[i_])
                i_ += 1
            if tokens[i_] != ")":
                i_ += 1
            identifier_idx = self.GetIdenfitiferIndex(temp_list)
            temp_type = self.ReadDeclerationList(
                temp_list, identifier_idx - 1, identifier_idx + 1
            )
            id_ = identifier(temp_type, temp_list[identifier_idx])
            argument_dict[id_.annotated_name] = id_
        return_type = self.GetReturnType(tokens, idx)
        i_ += 1

        bracket_lst = ["{"]
        i_ += 1
        codes_ = []
        while i_ < len_ and len(bracket_lst) != 0:
            if tokens[i_] in ("{", "(", "["):
                bracket_lst.append(tokens[i_])
            elif tokens[i_] == "}" and bracket_lst[-1] == "{":
                bracket_lst.pop()
            elif tokens[i_] == "]" and bracket_lst[-1] == "[":
                bracket_lst.pop()
            elif tokens[i_] == "(" and bracket_lst[-1] == ")":
                bracket_lst.pop()
            codes_.append(tokens[i_])
            i_ += 1
        i_ += -1
        functor_ = FunctionBody(tokens[idx], return_type, argument_dict, codes_)
        self.all_function[functor_.name_] = functor_

        # self.all_function
        return temp_type

    def is_function_decleration(self, token_list: list[str], identifier_idx: int):
        if token_list[identifier_idx + 1] == "(" and self.is_type(
            token_list[identifier_idx - 1]
        ):
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
                    # cur_identifier = self.all_identifier[lst[identifier_idx]]
                    # cur_identifier.type_ = temp_type
                    temp_size = 0
                    if lst[identifier_idx + 2] == "]":
                        temp_size = 10

                    else:
                        temp_size = ""
                        identifier_idx += 2
                        while lst[identifier_idx] != "]":
                            # temp_size = temp_size * 10 + int(lst[identifier_idx + 2])
                            # identifier_idx += 1
                            temp_size += lst[identifier_idx]
                            identifier_idx += 1
                        identifier_idx += 1

                    # temp_size = lst[identifier_idx + 1]
                    array_type = CTypeFactory.auto_call_method(
                        build_in_type.BUILD_IN_ARRAY, temp_type, temp_size
                    )

                    cur_identifier = identifier(array_type, lst[identifier_idx])
                else:
                    cur_identifier = identifier(temp_type, lst[identifier_idx])

                Lexer.all_identifier[lst[identifier_idx]] = cur_identifier

        for k_, v_ in self.all_function.items():
            print(k_)
            print(str(v_))
        # val_list = [1, 2, 3, 4, 5, 6, 7, 8]
        # self.all_identifier["b"].initialize_list(val_list, 0)
        # print(self.all_identifier["b"].print_value())
        a = 1

    def ParseFile(self, filename: str):
        with open(filename, "r") as fp:
            codes = fp.read()
            self.TokenDispatch(codes)

        # for k, v in self.all_typedef.items():
        #    print(f"{k}, {v}")


if __name__ == "__main__":
    parser_ = Lexer()
    parser_.ParseFile("a.c")
