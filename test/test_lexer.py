import unittest
from lexer import (
    build_in_type,
    SetType,
    C_type,
    C_build_in_pointer,
    C_build_in_array,
    CompositeType,
    C_struct,
    C_union,
    C_enum,
    CTypeFactory,
    identifier,
    Lexer,
)


""" class TestBuildInType(unittest.TestCase):
    def test_is_build_in_type(self):
        self.assertTrue(build_in_type.INT.is_build_in_type())
        self.assertFalse(build_in_type.DEFINED_STRUCT.is_build_in_type())

    def test_is_composite_type(self):
        self.assertFalse(build_in_type.INT.is_composite_type())
        self.assertTrue(build_in_type.DEFINED_STRUCT.is_composite_type())


class TestSetType(unittest.TestCase):
    def test_set_type(self):
        self.assertEqual(SetType("int"), build_in_type.INT)
        self.assertEqual(SetType("unsigned int"), build_in_type.UNSIGNED_INT)
        self.assertEqual(SetType("unknown_type"), "unknown_type")
 """

""" class TestCType(unittest.TestCase):
    def test_c_type_str(self):
        c_type = C_type("int")
        self.assertEqual(str(c_type), "int")

    def test_is_cv(self):
        c_type = C_type("int", is_const_=True, is_volatile_=True)
        self.assertTrue(c_type.is_cv())

    def test_is_user_defined(self):
        c_type = C_type(build_in_type.DEFINED_STRUCT)
        self.assertTrue(c_type.is_user_defined())

    def test_is_composite_type(self):
        c_type = C_type(build_in_type.DEFINED_STRUCT)
        self.assertTrue(c_type.is_composite_type()) """


""" class TestCBuildInPointer(unittest.TestCase):
    def test_c_build_in_pointer_str(self):
        base_type = C_type("int")
        pointer = C_build_in_pointer(base_type)
        self.assertEqual(str(pointer), f"build in pointer of {base_type}")


class TestCBuildInArray(unittest.TestCase):
    def test_c_build_in_array_str(self):
        element_type = C_type("int")
        array = C_build_in_array(element_type, 10)
        self.assertEqual(str(array), f"build in array of 10 of {element_type}")

    def test_size(self):
        element_type = C_type("int")
        array = C_build_in_array(element_type, 10)
        self.assertEqual(array.Size(), 10)
 """

""" class TestCompositeType(unittest.TestCase):
    def test_composite_type_str(self):
        fields = {"field1": C_type("int")}
        composite = CompositeType(build_in_type.DEFINED_STRUCT, "test_struct", fields)
        self.assertIn("test_struct", str(composite))

    def test_return_member_dict(self):
        fields = {"field1": C_type("int")}
        composite = CompositeType(build_in_type.DEFINED_STRUCT, "test_struct", fields)
        member_dict = composite.ReturnMemberDict()
        self.assertIn("field1", member_dict)

    def test_init_param_dict(self):
        fields = {"field1": C_type("int")}
        composite = CompositeType(build_in_type.DEFINED_STRUCT, "test_struct", fields)
        param_dict = composite.init_param_dict()
        self.assertIn("field1", param_dict)
 """

""" class TestCTypeFactory(unittest.TestCase):
    def test_get_struct(self):
        fields = {"field1": C_type("int")}
        struct = CTypeFactory.get_struct("test_struct", fields)
        self.assertEqual(str(struct), "struct test_struct")

    def test_get_union(self):
        fields = {"field1": C_type("int")}
        union = CTypeFactory.get_union("test_union", fields)
        self.assertEqual(str(union), "union test_union")

    def test_get_enum(self):
        values = {"value1": 1}
        enum = CTypeFactory.get_enum("test_enum", values)
        self.assertEqual(str(enum), "enum test_enum")

    def test_get_pointer(self):
        base_type = C_type("int")
        pointer = CTypeFactory.get_pointer(base_type)
        self.assertEqual(str(pointer), f"build in pointer of {base_type}")

    def test_get_array(self):
        base_type = C_type("int")
        array = CTypeFactory.get_array(base_type, 10)
        self.assertEqual(str(array), f"build in array of 10 of {base_type}")
 """

class TestIdentifier(unittest.TestCase):
    def test_identifier_str(self):
        id = identifier(C_type("int"), "test_id")
        self.assertEqual(str(id), "name : test_id\ntype : int\nval : None\n")

    def test_initialize_list(self):
        id = identifier(C_type("int"), "test_id")
        token_list = ["1"]
        new_idx = id.initialize_list(token_list, 0)
        self.assertEqual(id.value, "1")
        self.assertEqual(new_idx, 1)


class TestLexer(unittest.TestCase):
    def test_is_literal(self):
        lexer = Lexer()
        literal = lexer.is_literal("123")
        self.assertEqual(literal.value, 123)

    def test_split_token(self):
        lexer = Lexer()
        tokens = lexer.split_token("int a = 10;")
        self.assertEqual(tokens, ["int", "a", "=", "10", ";"])

    def test_parse_file(self):
        lexer = Lexer()
        lexer.ParseFile("a.c")
        self.assertIn("main", lexer.all_function)


if __name__ == "__main__":
    unittest.main()