from ast import literal_eval
import collections
from copy import deepcopy
from curses.ascii import isalpha
from dataclasses import field
from enum import Enum, auto
from logging import raiseExceptions
from math import nan
from operator import le, truediv
import queue
import random
import re
import stat
import string
from sys import exception
import token
from turtle import left
from typing import Deque, Generator, TypeAlias, final
import uuid
import a_c_lexer.reserved_word as reserved_word
from collections import deque
from a_c_lexer.base_type import C_type, build_in_type, UNKOWN_TYPE


class identifier:
    all_identifier: dict[str, "identifier"] = {}

    __slot__ = [
        "type_",
        "annotated_name",
        "value",
        "is_const",
        "is_volatile",
        "is_static",
    ]
    def __init__(self, typename: C_type, varname: str, val=None ,is_const = False, is_volatile = False, is_static = False):
        self.type_: C_type = typename
        self.annotated_name = varname

        self.value: dict | int | str = val
        identifier.all_identifier[self.annotated_name] = self
        self.is_const = is_const
        self.is_volatile = is_volatile
        self.is_static = is_static

        if self.type_.using_type == build_in_type.BUILD_IN_ARRAY:
            self.value = self.type_.init_param_dict()
        elif self.type_.using_type == build_in_type.BUILD_IN_POINTER: #and (self.type_.subtype.is_composite_type() or self.type_.subtype.using_type == build_in_type.BUILD_IN_ARRAY):
            self.value = None
        elif self.type_.is_composite_type():
            self.value = self.type_.init_param_dict()
        else:
            self.value = None

    def __format__(self, format_spec: str) -> str:
        if isinstance(self.value, dict):
            fmt_str = f"{{v:format_spec for v in self.value.values()}}"
            return fmt_str
        else:
            if format_spec == "" or format_spec == "s": 
                return f"{self.annotated_name} = {self.value}"
            else:
                return f"{self.annotated_name} : {self.type_} = {self.value}"

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

    def is_chain_chain_identifier(self, tokens : Deque):
        if self.type_.is_composite_type():
            if (len(tokens) == 1) and tokens[0] == self.annotated_name:
                return True
            else:
                self.is_chain_chain_identifier(tokens.popleft())
        else:
            return True

    def print_struct_in_json(self)->str:
        pass

    def __setitem__(self, key :tuple[str], val):

        if isinstance(key, str):
            assert isinstance(self.value, dict)
            self.value[key] = val

        elif len(key) == 1:
            key = key[0]
            if isinstance(self.value , dict):
                assert not self.value[key].type_.had_multiple_members()

                self.value[key].value = val
                
            else:
                self.value = val
        elif isinstance(self.value, dict):
            assert len(key) > 1
            key = list(key)
            k_ = key.pop()
            next_ = key.pop()
           
            self.value[k_][tuple(key)] = val

        else:
            assert not self.type_.had_multiple_members()
            self.value = val


    def __getitem__(self, key :list[str]):
       
        if len(key) == 1:
            if isinstance(self.value, dict):
                return self.value[key[0]].value
            else:
                raise AssertionError
        elif isinstance(self.value, dict):
            assert len(key) > 1
            k_ = key.pop()
            key.pop()
            return self.value[k_][key]
        else:
            assert not self.type_.had_multiple_members()
            return self

    def __format__(self, format_spec: str) -> str:
        final_str = ""
        fmt_ = re.split("|", format_spec)
        enable_label = "l" in fmt_
        enable_name = "n" in fmt_
        enable_type = "t" in fmt_
        enable_value = "v" in fmt_
        final_str += f"{'name : ' if enable_label else '':6}{self.annotated_name if enable_name else '':^10}"
        final_str += f"{'type : ' if enable_label else '': <10}{self.type_ if enable_type else '': >20}"
        final_str += f"{'val : ' if enable_label else ''}"
        if isinstance(self.value, dict):
            final_str = "\n{\n"
            for v__ in self.value.values():
                final_str += f"{format(v__, format_spec)}"
            final_str = "\n}\n"
        else:
            final_str += f"{self.value if enable_value else ""}"
        return final_str


class C_build_in_pointer(C_type):
    def __init__(
        self, point_to_: C_type = None, is_const_=False, is_volatile_=False, aka: str = ""
    ):
        super().__init__(
            build_in_type.BUILD_IN_POINTER, is_const_= is_const_, is_volatile_ =is_volatile_, subtype=point_to_
        )
        self.subtype = point_to_

    def __str__(self):
        sss = ""
        temp_type = self.subtype
        while temp_type is not None:
            sss += f"{temp_type}"
            temp_type = temp_type.subtype
        return f"{super().__str__()} of {sss}"
    
    def __format__(self, format_spec: str) -> str:
        """
        s : simple 
        v : verbose
        """
        if format_spec == "s" or format_spec == "":
            if isinstance(self.subtype, C_build_in_array):
                return f"{self.subtype.subtype} (*)[{self.subtype.size}]"
            elif self.subtype.using_type == build_in_type.CALL_FUNCTION:
                pass
            else:
                return f"{self.subtype} *"
        else:
            return f"is pointer of {self.subtype:v}"


class C_function_pointer(C_type):
    def __init__(
        self, subtype: C_type, is_const_=False, is_volatile_=False, aka: str = ""
    ):
        super().__init__(
            build_in_type.BUILD_IN_POINTER, subtype, is_const_, is_volatile_
        )
        self.subtype = subtype
        self.return_type: C_type = None
        self.argument_type: list[C_type] = None

    def __str__(self):
        sss = ""
        temp_type = self.subtype.using_type
        while temp_type is not None:
            sss += f"{temp_type} -> "
            temp_type = temp_type.using_type
        return f"{super().__str__()} of {sss}"


class member_field:
    def __init__(self, name_: str, type_: C_type):
        self.name_ = name_
        self.type_ = type_

    def __str__(self):
        fmtstr = f"{{{self.name_} : {self.type_}}}"
        return fmtstr


class CompositeType(C_type):
    def __init__(
        self,
        type_: C_type,
        name_: str,
        field_: dict[str, C_type],
        # typedef_name: str = "",
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
        subtype : C_type= None,
    ):
        assert type_ is not None
        super().__init__(type_, is_const_, is_volatile_, aka,subtype)
        self.field_: dict[str, C_type] = field_
        self.name = name_

    def __str__(self) -> str:
        str_type = str(self.using_type)
        str_type = str_type.replace("defined ", " ").replace("build in ", " ")
        fmtstr = f"{str_type}  {f"aka : {self.aka}" if self.aka == "" else ""}\nmember:{{\n{"\n".join([f"{k} : {str(v)}" for k, v in self.field_.items()])}\n}}"
        return fmtstr

    def ReturnMemberDict(self) -> dict[str, identifier]:
        ret_dict: dict[str, identifier] = {}
        for k, v in self.field_.items():
            if v.using_type.is_composite_type():
                ret_dict[k] = v.using_type.ReturnMemberDict()
            else:
                ret_dict[k] = identifier(v.using_type, k, nan)
        return ret_dict

    def init_param_dict(self) -> dict[str, identifier]:
        ret = {}
        for k_, v_ in self.field_.items():
            if v_.type_.is_composite_type():
                ret[k_] = v_.type_.init_param_dict()
            else:
                ret[k_] = identifier(v_.type_, k_)
        return ret

    def __setitem__(self, key: int, val: any):
        self.field_[key] = val

    def __getitem__(self, key: int):
        return self.field_[key]
    """
    n : stand for name
    t : stand for type
    v : stand for value
    l : stand for label e.g. type : ${type}
    """    
    def __format__(self, format_spec: str) -> str:

        if format_spec == "to":
            fmt_str = f"{self.name} = {{\n"
            for v_ in self.field_.values():
                fmt_str += f".{v_.annotated_name} : {v_.type_.using_type}\n"
            fmt_str += "}\n"
            return fmt_str
        elif format_spec == "t":
            return ""


class C_build_in_array(CompositeType):

    def __init__(
        self,
        element_type: C_type,
        size_in_code: str | int,
        is_const: bool = False,
        is_volatile=False,
        aka: str = "",
    ):
        if isinstance(size_in_code, int):
            self.size = size_in_code
        else:
            self.size = 10

        self.field_ = {x: member_field(x, element_type) for x in range(self.size)}
        self.subtype = element_type
        super().__init__(
            build_in_type.BUILD_IN_ARRAY, "", self.field_, is_const, is_volatile, aka, self.subtype
        )
        self.size_code = size_in_code

    def Size(self) -> int:
        return self.size

    def __setitem__(self, key: int, val: any):
        assert isinstance(key, int)
        self.value[key] = val

    def __getitem__(self, key: int):
        assert isinstance(key, int)
        return self.value[key]

    def __str__(self):
        return f"{super().__str__()} of {self.size_code} of {self.subtype}"

    def print_element(self):
        return f""

    def ReturnMemberDict(self):
        idx_key = [f"_{x}" for x in range(self.size)]
        ret_dict: dict[str, identifier] = {}
        for i in idx_key:
            ret_dict[i] = identifier(self.subtype, i, nan)
        return ret_dict


class C_struct(CompositeType):
    def __init__(
        self,
        name_: str,
        field_: dict[str, C_type],
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.DEFINED_STRUCT, name_, field_, is_const_, is_volatile_, aka
        )
    
    def __str__(self)->str:
        return f"struct {self.name}{self.aka if self.aka != "" else ""}"


class C_union(CompositeType):
    def __init__(
        self,
        name_: str,
        field_: dict[str, C_type],
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.DEFINED_UNION, name_, field_, is_const_, is_volatile_, aka
        )
    
    def __str__(self):
        return f"union {self.name}"


class C_enum(CompositeType):
    def __init__(
        self,
        name_: str,
        field_: dict[str, C_type],
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.DEFINED_UNION, name_, field_, is_const_, is_volatile_, aka
        )
    
    def __str__(self):
        return f"enum {self.name}"


class CTypeFactory:
    _cache = {}

    part_of_name: list[str] = []

    @staticmethod
    def get_struct(name: str, fields: dict[str, C_type] = None, aka : str = ""):
        key = f"struct {name}"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        CTypeFactory.part_of_name.append(name)
        struct_type = C_struct(name, fields or {}, aka = aka)
        CTypeFactory._cache[key] = struct_type
        return struct_type

    @staticmethod
    def get_union(name: str, fields: dict[str, C_type] = None):
        key = f"union {name}"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        CTypeFactory.part_of_name.append(name)
        union_type = C_union(name, fields or {})
        CTypeFactory._cache[key] = union_type
        return union_type

    @staticmethod
    def get_enum(name: str, values: dict[str, int] = None):
        key = f"enum {name}"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        CTypeFactory.part_of_name.append(name)
        enum_type = C_enum(name, values or {})
        CTypeFactory._cache[key] = enum_type
        return enum_type

    @staticmethod
    def get_pointer(base_type: C_type):
        key = f"ptr{base_type.using_type})"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        # CTypeFactory.part_of_name.append(name)
        ptr_type = C_build_in_pointer(base_type)
        CTypeFactory._cache[key] = ptr_type
        return ptr_type

    @staticmethod
    def get_array(base_type: C_type, size: int):
        key = f"array({str(base_type.using_type)}, {size})"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        try:
            size = int(size)
        except ValueError:
            size = 20
        array_type = C_build_in_array(base_type, size)
        CTypeFactory._cache[key] = array_type
        return array_type

    @staticmethod
    def auto_call_method(type_: C_type, *args, **kwargs):
        if type_ == build_in_type.DEFINED_STRUCT:
            return CTypeFactory.get_struct(*args, **kwargs)
        elif type_ == build_in_type.DEFINED_ENUM:
            return CTypeFactory.get_enum(*args, **kwargs)
        elif type_ == build_in_type.DEFINED_UNION:
            return CTypeFactory.get_union(*args, **kwargs)
        elif type_ == build_in_type.BUILD_IN_POINTER:
            return CTypeFactory.get_pointer(*args, **kwargs)
        elif type_ == build_in_type.BUILD_IN_ARRAY:
            return CTypeFactory.get_array(*args, **kwargs)
        elif type_ in reserved_word.fundamental_type or (isinstance(type_, build_in_type) and type_.is_build_in_type()):
            return C_type(type_, *args, **kwargs)
        else:
            return UNKOWN_TYPE(type_, *args, **kwargs)

    @staticmethod
    def is_part_of_type(code_: str) -> False:
        return True if code_ in CTypeFactory.part_of_name else False


C_AnyType: TypeAlias = (
    C_type
    | C_build_in_array
    | C_build_in_pointer
    | C_function_pointer
    | C_struct
    | C_union
    | C_enum
    | CompositeType
)

class TokenEmiter():
    def __init__(self, tokens : collections.deque):
        self.tokens = tokens
        self.i_ = 0
        self.len = len(tokens)
        self.token = None
        self.it_i = 0
    
    def __getitem__(self, key: int) -> str:
        return self.tokens[key]
    
    def __iter__(self):
        return self 

    def __next__(self):
        self.it_i += 1
        yield self.token[self.it_i]
    
    def move_seek(self, i_ : int):
        self.it_i += i_
        return self

    def peek(self, i_ : int = 1)-> str:
        try:
            return self.tokens[self.it_i + i_]
        except IndexError:
            return None
    
    def update(self, i_: int = 1):
        self.move_seek(i_)
        try:
            return self[self.it_i]
        except IndexError:
            return None

    def pass_white_space(self):
        while self.it_i < self.len:
            while self.it_i < self.len and self.tokens[self.it_i] in ["\t", "\n", " "]:
                self.it_i += 1
            val_ = self.tokens[self.it_i]
            yield val_
            self.it_i += 1
    
    def find_until(self, target):
        for token in self:
            if token in target:
                break
        return self[self.it_i]
    def find_until_not(self, target):
        for token in self:
            if token not in target:
                break
        return self[self.it_i]

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


def is_legal_identifier(code : str) -> bool:
    regex = r"(^[a-zA-Z\_]+[\w\_]*?$)"
    if (result_ := re.search(regex, code)) is not None:
        return True if result_.group(1) == code else False
    return False

class continuous_signing:
    __slot__ = ["get_item", "set_item"]
    def __init__(self): 
        self.set_item = None
        self.get_item = None

class Statement:
    def __init__(self, tokens : list[str]):
        pass
        
        self.tokens = tokens
        self.idx = 0
        self.if_statememt: dict[int, list[str]] = {}
        self.while_statememt: dict[int, list[str]] = {}
        self.for_statememt: dict[int, list[str]] = {}

        self.not_compound_statement : list[list[str]] = self.find_chaining_signment(tokens)

        #self.not_coumpound_stated = 
        self.find_chaining_signment(self.tokens)

        self.statement_: dict[str, dict[int, list[str]]] = {}
    
    @staticmethod
    def surround(TE: TokenEmiter):
        bracket_ = collections.deque()
        left_bracket = ["(", "[", "{"]
        right_bracket = [")", "]", "}"]
        all_bracket = ["(", ")", "[", "]", "{", "}"]
        
        assert TE.peek(0) in left_bracket, f"{TE.peek(0)} is not expected"
        bracket_.append(TE.peek(0))

        while len(bracket_):
            token_ = TE.find_until(all_bracket)
            if token_ in left_bracket:
                bracket_.append(token)
            elif token_ in right_bracket:
                if token_ == "]" and bracket_[-1] == "[":
                    bracket_.pop()
                if token_ == ")" and bracket_[-1] == "(":
                    bracket_.pop()
                if token_ == "}" and bracket_[-1] == "{":
                    bracket_.pop()
                else:
                    raise AssertionError

    @staticmethod
    def consume_complete_compound(TE : TokenEmiter):
        token = TE.peek(0)
        for token in TE:
            if token in ["if", "for", "while"]:
                TE.find_until("[{(")
                Statement.surround(TE)
                
                if TE.peek(1) == "{":
                    TE.update()
                    Statement.surround(TE)
                elif TE.peek(1) == "\n":
                    TE.update()
                    Statement.consume_complete_compound()
                else:
                    raise exception

    def consume_statement_impl(self, tokens: list[str], i_: int):
        temp_dict = {}
        if len(tokens) == 0:
            return
        if tokens[i_] == "if":
            temp_dict = self.if_statememt
        elif token[i_] == "for":
            temp_dict = self.for_statememt
        elif tokens[i_] == "while":
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
                    if tokens[i_] == "-" and tokens[i_ + 1] == ">": 
                        codes.append("->")
                        i_ += 1
                    else:
                        codes.append(tokens[i_])
                    i_ += 1
                ret.append(codes)
            i_ += 1
        self.not_compound_statement = ret
    
    def consume_compound(self, i_) -> int:
        if self.tokens[i_] in ["if", "while", "for"]:
            while self.tokens[i_] != ")":
                i_ += 1
            i_ += 1
            if self.tokens[i_] != "{":
                bracket_ = collections.deque("{")
                while len(bracket_):
                    i_ += 1
                    if self.tokens[i_] == "{":
                        bracket_.append("}")
                    elif self.tokens[i_] == "}":
                        bracket_.pop()
            else:
                i_ = self.consume_compound(i_)
        else:
            while self.tokens[i_] != ";":
                i_ += 1
        return i_ 

    def find_chaining_signment(self, TE: TokenEmiter):
        #i_ = 0
        tokens = self.tokens

        len_ = len(self.tokens)
        ret_ = collections.deque()
        dq_ = [] #collections.deque()
        save_ = collections.deque()
        cont_sign = continuous_signing()
        for token in TE:
            if token in ["if", "for", "while"]:
                self.surround(TE)
            else:
                no_chaining = False
                while token != ";":
                    if no_chaining:
                        TE.find_until("\n")
                        #i_ += 1
                        break
                    if is_legal_identifier(token):
                        dq_.append(token)
                    elif token == "-" and TE.peek(1) == ">":
                        dq_.append("->")
                        TE.move_seek(1)
                        #i_ += 1
                    elif token == ".":
                        dq_.append("->")
                    elif token == "[":
                        dq_.append(".")
                        #i_ += 1
                        while token != "]":
                            #assert token.isdigit()
                            dq_.append(token)
                            #i_ += 1
                            token = TE.update()
                        dq_.append(token)
                    elif token == "=":
                        #dq_.append("=")
                        if len(dq_):
                            #ret_.append(deepcopy(dq_))
                            cont_sign.set_item = deepcopy(dq_)
                            dq_.clear()

                    elif token in ["\n", "\t", " "]:
                        pass
                    else:
                        no_chaining = True
                        dq_.clear()
                    if token== ";":
                        break
                    i_ += 1
                if len(dq_):
                    #ret_[-1].append(deepcopy(dq_))
                    cont_sign.get_item = deepcopy(dq_)
                    cont_sign.set_item.reverse()
                    cont_sign.get_item.reverse()
                    cont_sign.set_item = cont_sign.set_item[:-2]
                    cont_sign.get_item = cont_sign.get_item[:-2]
                    
                    ret_.append(deepcopy(cont_sign))
                    dq_.clear()
                i_ += 1
                no_chaining = False
        self.ret = ret_        
        return self


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
        self.statement_: Statement = Statement(self.body)
        self.stated_id: dict[str, identifier] = {}
        self.statement_.consume_statement(self.body, 0)

        #print(self.statement_.ret)

        #test_code = ['b', '->', 'f_', '.', 'a', '=', ['a', '.', 'a']
        
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
    
    def is_literal(self, codes: str) -> identifier:
        if (temp := re.search(r"^(\d+[uU]?[lL]{0,2})$", codes)) is not None:
            if temp.group(1) == len(codes):
                name_ = temp.group(1)
                val_ = int(name_)
                return identifier(build_in_type.INT, name_, val_)
        elif (temp := re.search(r"^(0x[0-9abcedfABCEDF]+[uU]?[lL]{0,2})$", codes)) is not None:
            if temp.group(1) == len(codes):
                name_ = temp.group(1)
                val_ = int(name_, base=16)
                return identifier(build_in_type.INT, name_, val_)
        elif (temp := re.search(r"^(0[01234567]+[uU]?[lL]{0,2})$", codes)) is not None:
            if temp.group(1) == len(codes):
                name_ = temp.group(1)
                val_ = int(name_, base=8)
                return identifier(build_in_type.INT, name_, val_)
        elif (temp := re.search(r"^(0b[01]+[uU]?[lL]{0,2})$", codes)) is not None:
            if temp.group(1) == len(codes):
                name_ = temp.group(1)
                val_ = int(name_, base=2)
                return identifier(build_in_type.INT, name_, val_)
        elif (temp := re.search(r"^[\d+]+\.[\d+]+f?$", codes)) is not None:
            if temp.group(1) == len(codes):
                name_ = temp.group(1)
                type_ = build_in_type.DOUBLE
                val_ = 0
                if name_.endswith("f"):
                    type_ = build_in_type.FLOAT
                    val_ = float(name_[:-1])
                else:
                    val_ = float(val_)
                return identifier(type_, name_, val_)
        elif (temp := re.search(r"^(\".*?\"|\'.*?\')$", codes)) is not None:
            if temp.group(1) == len(codes):
                name_ = temp.group(1)
                return identifier(C_build_in_pointer(build_in_type.CHAR), name_, name_)
        return None


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
    
    def chaining_assignment(self):
        pass
        

    def read_simple_assignment(self, tokens: list[str], i_: int):
        len_ = len(tokens)

def pass_white_space(tokens: list[str], i_: int):
    len_ = len(tokens)
    while i_ < len_ and tokens[i_] in [" ", "\n", "\t"]:
        i_ += 1
    return i_





class Lexer:
    all_type: dict[str, C_type] = {}
    all_identifier: dict[str, identifier] = {}
    all_typedef: dict[str, C_type] = {}
    all_function: dict[str, FunctionBody] = {}
    #all_funct : dict[str,]

    def __init__(self):
        self.i_ = 0
        pass
    
    def is_literal(self, codes: str) -> identifier:
        if (temp := re.search(r"^\d+$", codes)) is not None:
            name_ = codes
            val_ = int(name_)
            return identifier(C_type(build_in_type.INT), name_, val_)
        elif (temp := re.search(r"^0x[0-9abcedfABCEDF]+$", codes)) is not None:
            name_ = codes
            val_ = int(name_, base=16)
            return identifier(C_type(build_in_type.INT), name_, val_)
        elif (temp := re.search(r"^0[01234567]+$", codes)) is not None:
            name_ = codes
            val_ = int(name_, base=8)
            return identifier(C_type(build_in_type.INT), name_, val_)
        elif (temp := re.search(r"^0b[01]+$", codes)) is not None:
            name_ = codes
            val_ = int(name_, base=2)
            return identifier(C_type(build_in_type.INT), name_, val_)
        elif (temp := re.search(r"^[\d+]+\.[\d+]+f?$", codes)) is not None:
            name_ = codes
            type_ = build_in_type.DOUBLE
            val_ = 0
            if name_.endswith("f"):
                type_ = build_in_type.FLOAT
                val_ = float(name_[:-1])
            else:
                val_ = float(val_)
            return identifier(type_, name_, val_)
        elif (temp := re.search(r"^(\".*?\"|\'.*?\')$", codes)) is not None:
            name_ = codes
            return identifier(C_build_in_pointer(C_type(build_in_type.CHAR)), name_, name_)
        return None

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

        if code in Lexer.all_identifier.keys():
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
        random_name = uuid.uuid4()
        while random_name in CTypeFactory._cache: 
            random_name = uuid.uuid4()
        return random_name

    def GetIdenfitiferIndex(self, tokens: list[str]):
        i_ = len(tokens) - 1
        if tokens[i_] == ")":
            bracket_ = [tokens[i_]]
            i_ -= 1
            while i_ > 0 and len(bracket_):
                if tokens[i_] == "(":
                    bracket_.pop()
                elif tokens[i_] == ")":
                    bracket_.append(tokens[i_])
                i_ -= 1
            
        
        while i_  >= 0:
            if tokens[i_] in reserved_word.frament_type_key:
                pass
            elif tokens[i_] in reserved_word.fundamental_type:
                pass
            elif tokens[i_] in Lexer.all_type.keys():
                pass
            elif tokens[i_] in Lexer.all_typedef.keys():
                pass
            elif self.is_new_identifier(tokens[i_]):
                # and not self.is_identifier(tokens[i_])
                return i_
            elif tokens[i_] == "{" and tokens[i_ + 1] in [
                "struct",
                "union",
                "enum",
            ]:
                return i_
            i_ -= 1
        return i_

    def is_fundamental_type(self, may_be_type: str) -> bool:
        return True if may_be_type in reserved_word.fundamental_type else False
        

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
                elif Lexer.all_typedef.keys():
                    return Lexer.all_typedef[tokens[left]]
                elif (
                    left > 0
                    and f"{tokens[left - 1]} {tokens[left]}" in self.all_type.keys()
                ):
                    return self.all_type[f"{tokens[left - 1]} {tokens[left]}"]

    
    def read_complicate_type(self, tokens: list[str], left: int, right: int):
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
                    assert 0, "function ptr is not supported yet"
                elif tokens[right] == "[":
                    array_size_ = ""
                    right += 1
                    while right < len_ and tokens[right] != "]":
                        array_size_ += tokens[right]
                        right += 1

                    return CTypeFactory.get_array(
                        self.read_complicate_type(tokens, left, right + 1), array_size_
                    )

                elif tokens[right] == ")":
                    temp_type = self.read_complicate_type(tokens, left, right)
                    pass
                elif tokens[right] == ";":
                    return self.read_complicate_type(tokens, left, len_)

            if left >= 0:

                if tokens[left] == "*":
                    return CTypeFactory.get_pointer(
                        self.read_complicate_type(tokens, left - 1, right)
                    )
                elif tokens[left] in reserved_word.frament_type_key:
                    base_type = ""
                    if tokens[left] in Lexer.all_type.keys():
                        if tokens[left] == "long":
                            base_type += "long"
                            if left > 0 and tokens[left - 1] == "long":
                                base_type += " long"
                                left-= 1
                    dq = collections.deque()
                    while left >= 0:
                        if tokens[left] in reserved_word.frament_type_key:
                            dq.appendleft(tokens[left])
                            base_type += f"{tokens[left]}"
                        left -= 1
                        """                         if tokens[left] == "unsigned":
                            base_type += f" {tokens[left]}" """
                    return C_type(" ".join(dq))
                elif (
                    tokens[left] in Lexer.all_type.keys()
                    or tokens[left] in Lexer.all_typedef.keys()
                ):
                    temp_type = None
                    if tokens[left] in Lexer.all_type.keys():
                        temp_type = Lexer.all_type[tokens[left]]
                    else:
                        temp_type = Lexer.all_typedef[tokens[left]]
                    return temp_type
                else:
                    return CTypeFactory.auto_call_method(tokens[left])
            
                    

    def ReadIdDecleration(self, tokens: list[str]):
        identifier_idx = self.GetIdenfitiferIndex(tokens)
        if tokens[identifier_idx] in ["union", "struct", "enum"]:
            self.ReadUserDefinedType(tokens)
        else:
            temp_type = self.read_complicate_type(
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
                Lexer.all_typedef[tokens[i_]] = CTypeFactory.get_pointer(
                    CTypeFactory(target_type)
                )
            else:
                typedef_name.append(tokens[i_])
                Lexer.all_typedef[tokens[i_]] = target_type
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
        i_ += 2
        while tokens[i_] != "\n":
            i_ += 1
            if tokens[i_] == "\\":
                i_ += 2
        return i_
    def consume_extern_C(self, tokens: list[str], i_ : int) -> int:
        len_ = len(tokens) - 1
        while tokens[i_] != "{":
            i_ += 1
        i_ += 1
        while tokens[len_] != "}":
            len_ -= 1
        tokens.pop(len_)
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
    
    def is_type_keyword(self, code : str) -> bool:
        if code in reserved_word.fundamental_type:
            return True
        elif code in Lexer.all_type.keys():
            return True
        elif code in Lexer.all_typedef.keys():
            return True
        elif code in Lexer.all_identifier.keys():
            return False
        return False
    
    def is_legal_identifier(self, code : str) -> bool:
        regex = r"^[a-zA-Z\_]+[\w\_]*?$"
        if (result_ := re.search(regex, code)) is not None:
            return True
        return False
    
    def is_reserved_word(self, code : str) -> bool:
        if code.startswith("__"): # for compiler extension
            return False
        if code in reserved_word.fundamental_type:
            return True
        if code in reserved_word.frament_type_key:
            return True
        return False
    
    def Const(self):
        const_attr = 0
        def inner():
            nonlocal const_attr 
            if const_attr == 0:
                const_attr = 1
            else:
                const_attr = 0
            temp_ = const_attr
            return temp_
        return inner()

    def Static(self):
        const_attr = 0
        def inner():
            nonlocal const_attr 
            if const_attr == 0:
                const_attr = 1
            else:
                const_attr = 0
            temp_ = const_attr
            return temp_
        return inner()

    def Volatile(self):
        volatile_attr = 0
        def inner():
            nonlocal volatile_attr 
            if volatile_attr == 0:
                volatile_attr = 1
            else:
                volatile_attr = 0
            temp_ = volatile_attr
            return temp_
        return inner()

    def consume_compound(self, tokens:list[str], i_ : int = 0):
        bracket = []
        len_ = len(tokens)
        #i_ = 0
        while i_ < tokens:
            
            #temp.append(tokens[i_])
            if tokens[i_] == "{":
                bracket.append("}")
            elif tokens[i_] == "(":
                bracket.append(")")
            elif tokens[i_] == "[":
                bracket.append("]")
            elif tokens[i_] in ["}", "]", ")"]:
                assert bracket[-1] == tokens[i_]
                bracket.pop()
        return i_


    def find_identifier_index(self, tokens: list[str]):
        pass

    def initialization_list1(self, tokens):
        pass

    def initialization_list_impl(self, TE : TokenEmiter):
        temp_ = []
        for token in TE.pass_white_space():
            if token == "}" or token == ",":
                break
            temp_.append(token)
        val_ = "".join(temp_)
        if self.is_literal(val_):
            return val_
        else:
            return val_
        


    def initialization_list(self, TE: TokenEmiter) -> tuple[list[str, int, dict[str, int]], int]:
        temp_ = collections.deque()
        lst_ = []
        TE.update()
        for token in TE.pass_white_space():
            if token == ".":
                k_ = TE.update()
                TE.update(2)
                temp_ = self.initialization_list_impl(TE)
                lst_.append({k_ : temp_})
                print(lst_)
            elif token == "{":
                temp_ = self.initialization_list(TE)
                lst_.append(temp_)
                print(lst_)
            elif token == "}":
                break
            else:
                temp_ = self.initialization_list_impl(TE)
                lst_.append(temp_)
                print(lst_)
            
            token = TE.peek(0)
            if token == ",":
                TE.update()
                continue
            if token == "}":
                
                break
            token = TE.update()
         
        return lst_

    def read_function_body(self, TE : TokenEmiter):
        token = next(TE)
        assert token == "{"
        bracket_ = ["{"]
        #body_ = []
        dq_ = collections.deque()
        while len(bracket_) != 0:
            i_ += 1
            dq_.append(token)
            if token == "{":
                bracket_.append(token)
            elif token == "}":
                bracket_.pop()
        while dq_[-1] != ";":
            dq_.pop()
        return dq_, i_

    def read_function(self, tokens:list[str], i_ : int, dq):

        
        pass
    

    def parse_enum(self, TE : TokenEmiter):
        i_ = 0
        auto_val = 0
        it_ = TE.pass_white_space()
        member_  : dict[str, identifier] = {}
        for token in TE.pass_white_space():# := next(it_)) != "}":
            if is_legal_identifier(token):
                name_ = token
            elif token == ",":
                member_[name_] = identifier(CTypeFactory.auto_call_method("int"), name_, auto_val)
            if TE.peek(1) == "=" and TE.peek(2).isalnum() :
                #next(it_)
                val_ = TE.peek(2)
                TE.update(2)
                assert val_.isdigit()
                auto_val = int(val_)
            else:
                auto_val += 1
            if token == "}":
                break

        return member_
    
    def parse_struct(self, TE: TokenEmiter):
        i_ = 0
        it_ = TE.pass_white_space()
        member_  : dict[str, identifier] = {}
        dq_ = collections.deque()
        token = TE.update()
        while token != "}":
            if is_legal_identifier(token):
                dq_.append(token)
            elif token == "[":
                dq_.append(token)
                while token != "]":
                    dq_.append(token)
                    token = TE.update(1)
                dq_.append(token)
            elif token == "*":
                dq_.append(token)
            elif token == "(" or token == ")":
                dq_.append(token)
            elif token == ";":
                name_i = self.GetIdenfitiferIndex(dq_)
                name_ = ""
                if name_i >= 0:
                    name_ = dq_[name_i]
                
                type_ = self.read_complicate_type(dq_, name_i - 1, name_i + 1)
                id_ = identifier(type_, name_, None)
                member_[name_] = id_
                
                dq_.clear()
            token = TE.update()
        TE.move_seek(1)
            
        return member_
    

    def LexerImpl(self, TE : TokenEmiter): 
        identifier_ =""
        type_ : C_type = None
        last_id_ = ""
        #name_ : str = ""
        id_ : identifier| C_type = None
        is_typing = False
        is_const = False
        is_false = False
        is_static = False
        val_ = None
        saves : list[str] = []
        dq : list[str] =[]
        endl_ = "{"
        
        for token in TE.pass_white_space():
            
            if token in ["\t", "\n", " "]:
                pass
            
            elif token == "typedef":
                is_typing = True
            elif token == "const":
                is_const =True
                saves.append(token)
                dq.append(token)
                self.Const()
            elif token == "volatile":
                saves.append(token)
                #is_volatile = True
                dq.append(token)
                self.Volatile()
            elif token == "static":
                saves.append(token)
                is_static = True
                dq.append(token)
                self.Static()
            elif token == "enum":
                dq.append(token)
                current_type_ = build_in_type.DEFINED_ENUM
                identifier_idx = self.GetIdenfitiferIndex(dq)
                name_ = ""
                if identifier_idx < 0:
                    name_ == f"anonymous {token}"
                else:
                    name_ = dq[identifier_idx]


                if self.is_legal_identifier(token) and self.is_legal_identifier(TE.peek(1)) and TE.peek(2) == ";": # enum A ; 
                    TE.update(2)
                elif self.is_legal_identifier(token) and self.is_legal_identifier(TE.peek(1)): # enum A a;
                    TE.update(1)
                assert (self.is_legal_identifier(token) and TE.peek(1) == "{") or token == "{"
                TE.update(2)
                member_ = self.parse_enum(TE)
                identifier_ = CTypeFactory.auto_call_method(current_type_, name_, member_)
                if name_ != "":
                    Lexer.all_typedef[identifier_.name_] = identifier_

                temp_name= "" 
                temp_type : C_type = None
                while token != ";":
                    if self.is_legal_identifier(token):
                        temp_name = token
                    elif token == "*":
                        temp_type = C_build_in_pointer(identifier_.using_type)
                    elif token == "[":
                        sz_ = ""
                        while token != "]":
                            sz_ += token
                        if temp_type is not None:
                            temp_type = CTypeFactory.get_array(temp_type, sz_)
                        else:
                            temp_type = CTypeFactory.get_array(identifier_, sz_)
                    token = TE.update(1)
                    if token in ["," ,";"]:
                        new_type = deepcopy(identifier_ if temp_type is None else identifier_.using_type)
                        new_type.name = temp_name
                        Lexer.all_typedef[temp_name] = new_type
                        temp_type = None
                        temp_name = ""
                while len(dq):
                    dq.pop()

            elif token in ["struct", "union"]:
                dq.append(token)
                current_type_ = build_in_type.DEFINED_STRUCT if token == "struct" else build_in_type.DEFINED_UNION
                identifier_idx = self.GetIdenfitiferIndex(dq)
                if identifier_idx < 0:
                    name_ = f"anonymous {self.GenerateRandomName()}"
                else:
                    name_ = dq[identifier_idx]
                
                if self.is_legal_identifier(token) and self.is_legal_identifier(TE.peek()) and TE.peek(2) == ";": # enum A ; 
                    TE.update(2)
                elif self.is_legal_identifier(token) and self.is_legal_identifier(TE.peek()): # enum A a;
                    TE.update(1)
                assert (self.is_legal_identifier(token) and TE.peek(1) == "{") or token == "{"

                TE.update(2)
                
                    
                member_ = self.parse_struct(TE) 
                identifier_: C_type = CTypeFactory.auto_call_method(current_type_, name_, member_)
                temp_name= ""
                token = TE.peek(0) 
                temp_type : C_type = None
                while token != ";":
                    if self.is_legal_identifier(token):
                        temp_name = token
                    elif token == "*":
                        temp_type = C_build_in_pointer(identifier_.using_type)
                    elif token == "[":
                        sz_ = ""
                        while token != "]":
                            sz_ += token
                        if temp_type is not None:
                            temp_type = CTypeFactory.get_array(temp_type, sz_)
                        else:
                            temp_type = CTypeFactory.get_array(identifier_, sz_)
                    
                    token = TE.update(1)
                    if token in ["," ,";"]:
                        new_type = deepcopy(identifier_ if temp_type is None else identifier_.using_type)
                        new_type.name = temp_name
                        Lexer.all_typedef[temp_name] = new_type
                        temp_type = None
                        temp_name = ""
                while len(dq):
                    dq.pop()
                a = 0
            elif token == ";":
                assert identifier_ is not None
                if isinstance(identifier_, identifier) and val_ is not None:
                    identifier_.value = val_
                if is_typing:
                    pass
                    return None
                else:
                    identifier_idx = self.GetIdenfitiferIndex(dq)
                    name_ = dq[identifier_idx]
                    complicate_type = self.read_complicate_type(dq, identifier_idx -1, identifier_idx + 1);
                    id_ =   identifier(complicate_type, name_, nan, self.Const(), self.Volatile(), self.Static())
                    #Lexer.all_typedef[id_.annotated_name] = id_
                    is_typing = False
                    name_ = ""
                    return id_
            elif token == "}":
                return None
            elif token == "(":
                dq.append(token)
                identifier_idx = self.GetIdenfitiferIndex(dq)
                if identifier_idx < 0:
                    pass
                elif dq[identifier_idx - 1] == "*":
                    pass
                elif name_ != "":
                    args = {}
                    while token != ")":
                        temp_ = []
                        while token != "," and token != ")":
                            temp_.append(token)
                        identifier_idx = self.GetIdenfitiferIndex(dq)
                        
                        id_ = self.read_complicate_type(temp_, identifier_idx - 1, identifier_idx + 1)
                        if token == ")":
                            break
                    #while
                    body_ = self.read_function_body(TE)
                    
                    fb = FunctionBody(name_, CTypeFactory.auto_call_method(dq[identifier_idx - 1]), args, body_)
                    Lexer.all_function[fb.name_] = fb
                
                pass
            elif token == ")":
                pass
                dq.append(token)
            elif token == "[":
                sz_ = ""
                while token != "]":
                    dq.append(token)
                    sz_ += token
                    token = TE.update()
                dq.append(token)

                assert type_ is not None
                type_ = CTypeFactory.get_array(type_, sz_)

            elif token == "*":
                dq.append(token)
                type_ = C_build_in_pointer(type_)
                pass
            elif self.is_type_keyword(token):
                dq.append(token)
                type_ = CTypeFactory.auto_call_method(token)
            elif self.is_legal_identifier(token):
                #assert type_ is not None
                dq.append(token)
            elif token == "=":
                
                identifier_idx = self.GetIdenfitiferIndex(dq)
                name_ = dq[identifier_idx]
                temp_type = self.read_complicate_type(dq, identifier_idx - 1, identifier_idx + 1)
                id_ = identifier(temp_type, name_, None, self.Const(), self.Volatile(), self.Static())
                assign_list  = self.initialization_list(TE)
                while len(dq):
                    dq.pop()
                val_ = self.is_literal(token)
            
        return


    def split_token(self, codes: str):
        tokens = re.split(r"(\W)", codes)
        tokens = [s for s in tokens if s != "" and s != " "]
        return tokens

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
            
            if self.is_legal_identifier(token):
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

    def is_type_decleration(self, token_list: list[str]) -> bool:
        i_ = 0
        len_ = len(token_list)
        for i_ in range(len_):
            if token_list[i_] in ["union", "struct", "enum"]:
                i_ += 1
                if token_list[i_] == "{":
                    return True
                elif self.is_new_identifier(token_list[i_]):
                    if f"struct_{token_list[i_]}" not in Lexer.all_type.keys():
                        return True
                return False
            if token_list[i_] in Lexer.all_typedef.keys():
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
        return_type = ""
        type_lst = tokens[:idx]
        return_type = self.read_complicate_type(type_lst, 0, 0)
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
            if self.is_type_decleration(lst):
                self.ReadUserDefinedType(lst)

            elif self.is_function_decleration(lst, identifier_idx):
                self.ReadFunction(lst, identifier_idx)

                pass
            else:
                temp_type = self.read_complicate_type(
                    lst, identifier_idx - 1, identifier_idx + 1
                )
                if lst[identifier_idx + 1] == "[":
                    temp_size = 0
                    if lst[identifier_idx + 2] == "]":
                        temp_size = 10

                    else:
                        temp_size = ""
                        identifier_idx += 2
                        while lst[identifier_idx] != "]":
                            temp_size += lst[identifier_idx]
                            identifier_idx += 1
                        identifier_idx += 1

                    array_type = CTypeFactory.auto_call_method(
                        build_in_type.BUILD_IN_ARRAY, temp_type, temp_size
                    )

                    cur_identifier = identifier(array_type, lst[identifier_idx])
                else:
                    cur_identifier = identifier(temp_type, lst[identifier_idx])

                Lexer.all_identifier[lst[identifier_idx]] = cur_identifier
      
        a = 1
    
    def remove_preprocess(self, tokens : list[str]) -> list[str]:
        tokens_ = []

        len_ = len(tokens)
        i_ = 0
        while i_ < len_:
            if tokens[i_] == " ":
                pass
            elif tokens[i_] == "#" and tokens[i_ + 1] in ["if", "endif", "ifdef", "ifndef", "define" ,"else", "include"]:
                i_ += 1
                while tokens[i_] != "\n":
                    i_ += 1
                    if  tokens[i_] == "\\":
                        i_ += 1
            else:
                tokens_.append(tokens[i_])
            i_ += 1
        return tokens_
    
    def regex_remove_comments(self, codes):
        # 去除所有多行注释
        code = re.sub(r'/\*.*?\*/', '', codes, flags=re.DOTALL)
        # 去除所有单行注释
        code = re.sub(r'//.*', '', code)
        return code
    def remove_comments_macros(self, code):
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'//.*', '', code)
        lines = code.splitlines()
        result = []

        keep_if_block = False

        for line in lines:
            stripped = line.strip()
            
            if re.match(r'#\s*(if|ifdef|ifndef|elif|else|endif)\b', stripped):
                continue
            elif re.match(r'#\s*(define|undef|include|pragma|error|line)\b', stripped):
                continue
            else:
                result.append(line)

        return '\n'.join(result)
    def ParseFile(self, filename: str):
        with open(filename, "r") as fp:
            codes = fp.read()
            TE = TokenEmiter(self.split_token(self.remove_comments_macros(codes)))
            
            self.LexerImpl(TE)
        
        cfg_ = identifier(self.all_typedef["foocfg"], "cfg")
        reg_ = identifier(self.all_typedef["fooreg"], "reg")
        cfg_[["a"]]= 1
        cfg_[["b"]]= 0
        cfg_[["c"]]= 3
        
        

if __name__ == "__main__":
    parser_ = Lexer()
    parser_.ParseFile("b.c")
