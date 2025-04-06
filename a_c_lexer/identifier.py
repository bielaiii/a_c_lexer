from typing import Deque
from .base_type import C_type, build_in_type
#from collections import Deque
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
        if self.type_.is_complex_type():
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