# C Lexer and Parser

This project implements a lexer and parser for C languages. It includes functionality to tokenize, parse, and analyze C code, supporting various C constructs such as structs, unions, enums, arrays, and pointers.

## Project Structure

## Features

- **Lexer**: Tokenizes C code, ignoring comments and preprocessing directives.
- **Parser**: Parses C declarations, user-defined types, and function definitions.
- **Type System**: Supports built-in types, pointers, arrays, structs, unions, and enums.
- **Initialization**: Handles initialization of composite types.
- **Function Parsing**: Parses function signatures and bodies.

## Key Components

### Lexer

The lexer is implemented in [lexer.py](lexer.py)[lexer.py](lexer.py). It tokenizes the input C code and dispatches tokens for further processing.

### Type System

The type system is defined in [base_type.py](base_type.py)[base_type.py](base_type.py) and [type_class.py](type_class.py)[type_class.py](type_class.py). It includes:

- Built-in types (e.g., `int`, `float`, `char`)
- Composite types (e.g., `struct`, `union`, `enum`)
- Pointers and arrays

### Reserved Words

Reserved words and fundamental types are listed in [reserved_word.py](reserved_word.py)[reserved_word.py](reserved_word.py).

### Defeat

- not support compiler extension
- not support preprocessor(compiler frontend usually does not support either)

### Example C Code

The file [a.c](a.c)[a.c](a.c) contains sample C code for testing the lexer and parser.

### Test Cases

The file [test_case.h](test_case.h)[test_case.h](test_case.h) provides various C declarations for testing.

## Usage

1. **Run the Lexer**:  
   Use the `Lexer` class in [lexer.py](lexer.py)[lexer.py](lexer.py) to parse a C file:

   ```python
   from lexer import Lexer
   
   parser = Lexer()
   parser.ParseFile("a.c")
   ```
