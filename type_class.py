from enum import Enum, auto
import uuid

from lexer import identifier
from base_type import *



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
        type_: C_type,
        name_: str,
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
        self.name = name_

    def __str__(self) -> str:
        str_type = str(self.type)
        str_type = str_type.replace("defined ", " ").replace("build in ", " ")
        fmtstr = f"{str_type}  {f"aka : {self.aka}" if self.aka == "" else ""}\nmember:{{\n{"\n".join([f"{k} : {v}" for k, v in self.argument_dict.items()])}\n}}"
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
        fmtstr = f"{self.name} {"" if len(self.typedef_name) == 0 else f"aka {self.typedef_name}" }\nmember:{{{"\n    ".join([f"{k} : {v}" for k, v in self.member.items()])}}}"
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