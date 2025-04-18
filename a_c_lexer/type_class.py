from ast import TypeAlias
from enum import Enum, auto
from math import nan
from sqlite3 import paramstyle
import uuid

from .import identifier
from .base_type import *


class C_build_in_pointer(C_type):
    def __init__(
        self, point_to_: C_type, is_const_=False, is_volatile_=False, aka: str = ""
    ):
        super().__init__(
            build_in_type.BUILD_IN_POINTER, point_to_, is_const_, is_volatile_
        )
        self.subtype = point_to_

    def __str__(self):
        sss = ""
        temp_type = self.subtype
        while temp_type is not None:
            sss += f"{temp_type}"
            temp_type = temp_type.subtype
        return f"{super().__str__()} of {sss}"
        # return f"{super().__str__()} of {self.point_to_}"


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
    ):
        assert type_ is not None
        super().__init__(type_, is_const_, is_volatile_, aka)
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
        # assert isinstance(key, int)
        self.field_[key] = val

    def __getitem__(self, key: int):
        # assert isinstance(key, int)
        return self.field_[key]


class C_build_in_array(CompositeType):

    def __init__(
        self,
        # field_: dict[str, member_field],
        element_type: C_type,
        size_in_code: str | int,
        # size_: int,
        is_const: bool = False,
        is_volatile=False,
        aka: str = "",
    ):
        if isinstance(size_in_code, int):
            self.size = size_in_code
        else:
            self.size = 10

        self.field_ = {x: member_field(x, element_type) for x in range(self.size)}
        # self.size = len(field_.keys())
        self.subtype = element_type
        super().__init__(
            build_in_type.BUILD_IN_ARRAY, "", self.field_, is_const, is_volatile, aka
        )
        # self.size = len(self.field_.keys())
        # self.size_code = self.
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
        return f"struct {self.name}{self.aka if self.aka is not "" else ""}"


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
        else:
            return C_type(*args, **kwargs)

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
