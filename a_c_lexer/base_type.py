from enum import Enum, auto


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
    UNKNOWN_TYPE = auto()

    def __str__(self):
        temp_str = self.name.lower().replace("_", " ").replace("build in ", "")
        return temp_str

    def is_build_in_type(self) -> bool:
        return True if self.value < 14 else False

    def __format__(self, format_spec: str) -> str:
        fmt_str = self.name.lower().replace("_", " ").replace("build in ", "")
        if format_spec == "":
            return fmt_str
        return f"{fmt_str:>20}"

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
            return build_in_type.UNKNOWN_TYPE


class C_type:
    def __init__(
        self,
        type_: str | build_in_type,
        aka: str = "",
        is_const_=False,
        is_volatile_=False,
        subtype : "C_type" = None,
    ):
        self.using_type = SetType(type_) if isinstance(type_, str) else type_
        self.is_const = is_const_
        self.is_volatile = is_volatile_
        self.aka = aka
        self.subtype = subtype
        # self.subtype = None

    def __str__(self) -> str:
        quan_ = ""
        if self.is_const:
            quan_ += "const "

        if self.is_volatile:
            quan_ += "volatile "

        return f"{quan_}{self.using_type}"
    
    def __format__(self, format_spec: str) -> str:
        """
        s : simple 
        v : verbose
        """
        if format_spec == "s" or format_spec == "":
            return f"{self.using_type:>10}"
        else:
            return f"{self.using_type:>10}"

    def GetMember() -> list[tuple[str, "C_type"]]:
        pass

    def is_cv(self) -> bool:
        return self.is_const and self.is_volatile

    def is_user_defined(self) -> bool:
        return (
            True
            if self.using_type
            in [
                build_in_type.DEFINED_ENUM,
                build_in_type.DEFINED_STRUCT,
                build_in_type.DEFINED_UNION,
            ]
            else False
        )
    
    def is_composite_type(self) -> bool:
        return (
            True
            if self.using_type
            in [
                build_in_type.DEFINED_ENUM,
                build_in_type.DEFINED_STRUCT,
                build_in_type.DEFINED_UNION,
                build_in_type.BUILD_IN_ARRAY
            ]
            else False
        )
    
    def had_multiple_members(self):
        return (
            True
            if self.using_type
            in [
                build_in_type.DEFINED_STRUCT,
                build_in_type.DEFINED_UNION,
                build_in_type.BUILD_IN_ARRAY
            ]
            else False
        )

    def single_value(self):
        pass

class UNKOWN_TYPE(C_type):
    def __init__(self, type_: str, aka: str = "", is_const_=False, is_volatile_=False, subtype: C_type = None):
        super().__init__(type_, type_, is_const_, is_volatile_, subtype)
    
    def __format__(self, format_spec: str) -> str:
        return f"{self.aka}(CURRENT_UNKNOWN)"
