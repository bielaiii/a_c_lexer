from enum import Enum, auto
from math import nan
import uuid

from lexer import identifier
from base_type import *


class C_build_in_type(C_type):
    def __init__(self, argument_list: list[str]):
        pass
class C_build_in_array: pass
class C_build_in_pointer: pass
class C_function_pointer: pass
class C_struct: pass
class C_union: pass
class C_enum: pass
class CompositeType: pass

    

C_AnyType = (
    C_type
    | C_build_in_array
    | C_build_in_pointer
    | C_function_pointer
    | C_struct
    | C_union
    | C_enum
    | CompositeType
)

class C_build_in_pointer(C_type):
    def __init__(
        self, subtype: C_type, is_const_=False, is_volatile_=False, aka: str = ""
    ):
        super().__init__(
            build_in_type.BUILD_IN_POINTER, subtype, is_const_, is_volatile_
        )
        self.subtype = subtype

    def __str__(self):
        return f"{super().__str__()} of {self.subtype}"


class C_function_pointer(C_type):
    def __init__(
        self, subtype: C_type, is_const_=False, is_volatile_=False, aka: str = ""
    ):
        super().__init__(
            build_in_type.BUILD_IN_POINTER, subtype, is_const_, is_volatile_
        )
        self.subtype = subtype
        self.return_type: C_AnyType = None
        self.argument_type: list[C_AnyType] = None

    def __str__(self):
        return f"{super().__str__()} of {self.subtype}"


class C_build_in_array(C_type):

    def __init__(
        self,
        element_type_: C_type,
        size_: int,
        is_const: bool = False,
        is_volatile=False,
        aka: str = "",
    ):
        super().__init__(build_in_type.BUILD_IN_ARRAY, aka, is_const, is_volatile)
        self.__size = int(size_)
        self.__element_type = element_type_

        self.value: dict[int, identifier] = {x : None for x in range(self.__size)}

    def Size(self) -> int:
        return self.__size

    def __setitem__(self, key: int, val: any):
        assert isinstance(key, int)
        self.argument_dict[key] = val

    def __getitem__(self, key: int):
        assert isinstance(key, int)
        return self.argument_dict[key]

    def __str__(self):
        return f"{super().__str__()} of {self.__size} of {self.__element_type}"

    def __format__(self, format_spec):
        temp_str = f"{{{",".join([str(x) for x in self.value])}}}"
        return super().__format__(format_spec)

    def print_element(self):
        return f""

    def ReturnMemberDict(self):
        idx_key = [f"_{x}" for x in range(self.__size)]
        ret_dict: dict[str, identifier] = {}
        for i in idx_key:
            ret_dict[i] = identifier(self.__element_type, i, nan)
        return ret_dict


class member_field:
    def __init__(self,name_ : str, type_ : C_AnyType): 
        self.name_ = name_
        self.type_ = type_

class CompositeType(C_type):
    def __init__(
        self,
        type_: C_type,
        name_: str,
        field_: dict[str, C_AnyType],
        # typedef_name: str = "",
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        assert type_ is not None
        super().__init__(type_, is_const_, is_volatile_, aka)
        self.field_: dict[str, C_type] = field_
        self.name = name_

    def __str__(self) -> str:
        str_type = str(self.type_)
        str_type = str_type.replace("defined ", " ").replace("build in ", " ")
        fmtstr = f"{str_type}  {f"aka : {self.aka}" if self.aka == "" else ""}\nmember:{{\n{"\n".join([f"{k} : {v}" for k, v in self.field_.items()])}\n}}"
        return fmtstr

    def ReturnMemberDict(self) -> dict[str, identifier]:
        ret_dict: dict[str, identifier] = {}
        for k, v in self.field_.items():
            if v.type_.is_user_defined():
                ret_dict[k] = v.type_.ReturnMemberDict()
            else:
                ret_dict[k] = identifier(v.type_, k, nan)
        return ret_dict
    
    def init_param_dict(self) -> dict[str, identifier]:
        ret = {}
        for k_, v_ in self.field_.items(): 
            if v_.type_.is_user_defined():
                ret[k_] = v_.type_.init_param_dict()
            else:
                ret[k_] = identifier(v_.type_, k_)
        return ret


class C_struct(CompositeType):
    def __init__(
        self,
        field_: dict[str, C_type],
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.DEFINED_STRUCT, field_, is_const_, is_volatile_, aka
        )


class C_union(CompositeType):
    def __init__(
        self,
        field_: dict[str, C_type],
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.DEFINED_UNION, field_, is_const_, is_volatile_, aka
        )
        self.field_: dict[str, C_type] = field_


class C_enum(CompositeType):
    def __init__(
        self,
        field_: dict[str, C_type],
        is_const_=False,
        is_volatile_=False,
        aka: str = "",
    ):
        super().__init__(
            build_in_type.DEFINED_UNION, field_, is_const_, is_volatile_, aka
        )

class CTypeFactory:
    _cache = {}

    @staticmethod
    def get_struct(name: str, fields: dict[str, C_type] = None):
        key = f"struct {name}"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        struct_type = C_struct(name, fields or {})
        CTypeFactory._cache[key] = struct_type
        return struct_type

    @staticmethod
    def get_union(name: str, fields: dict[str, C_type] = None):
        key = f"union {name}"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        union_type = C_union(name, fields or {})
        CTypeFactory._cache[key] = union_type
        return union_type

    @staticmethod
    def get_enum(name: str, values: dict[str, int] = None):
        key = f"enum {name}"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        enum_type = C_enum(name, values or {})
        CTypeFactory._cache[key] = enum_type
        return enum_type

    @staticmethod
    def get_pointer(base_type: 'C_type'):
        key = f"ptr({base_type})"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        ptr_type = C_build_in_pointer(base_type)
        CTypeFactory._cache[key] = ptr_type
        return ptr_type

    @staticmethod
    def get_array(base_type: 'C_type', size: int):
        key = f"array({base_type}, {size})"
        if key in CTypeFactory._cache:
            return CTypeFactory._cache[key]
        array_type = C_build_in_array(base_type, size)
        CTypeFactory._cache[key] = array_type
        return array_type


    @staticmethod
    def auto_call_method(type_ : C_type, *args, **kwargs):
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
        else:
            return C_type(*args, **kwargs)
