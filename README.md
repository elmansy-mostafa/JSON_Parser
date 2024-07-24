# JSON_Parser (2024)
## Overview

This code is a custom JSON validator. It consists of functions that lex (tokenize) and parse JSON strings to ensure they adhere to the JSON format. The main components are:

1. Lexer (lexer function): Converts a JSON string into a list of tokens.
2. Parser (parser, parser_object, parser_array, parser_value functions): Analyzes the tokens to validate the structure and content of the JSON.
3. Validation Function (validate_json): Combines lexing and parsing to validate a JSON string.
4. Test Function (test_json_files): Reads JSON files from a directory and validates them using the validate_json function.

## Features

1. Tokenization:
   - Handles JSON syntax characters ({, }, [, ], :, ,).
   - Processes string literals, including escape sequences (e.g., \", \\, \/, \b, \f, \n, \r, \t, \u followed by four hexadecimal digits).
   - Recognizes numeric values, boolean values (true, false), and null.
   - Skips whitespace.

2. Parsing:
   - Validates JSON objects (key-value pairs) and arrays (ordered values).
   - Ensures proper structure and nesting.
   - Checks for valid number formats and leading zeros.
   - Prevents trailing commas in objects and arrays.

3. Error Handling:
   - Detects and reports invalid characters in strings and escape sequences.
   - Ensures strings are properly terminated.
   - Validates the completeness and correctness of JSON structure.

4. Testing:
   - Automatically validates multiple JSON files from a specified directory.
   - Outputs validation results for each file.

## Detailed Functions

- lexer(input_string): Converts a JSON string into tokens, handling escape sequences and special characters.
- parser_value(tokens, index): Parses individual JSON values (objects, arrays, strings, numbers, booleans, null).
- parser_object(tokens, index): Validates JSON objects, ensuring keys are strings and values are valid.
- parser_array(tokens, index): Validates JSON arrays, ensuring elements are valid.
- parser(tokens): Determines whether the tokenized JSON is a valid array or object.
- validate_json(input_string): Integrates the lexer and parser to validate a JSON string and returns the result.
- test_json_files(): Reads and validates JSON files in the test_json directory, printing the results.

This code ensures that JSON data is correctly formatted, preventing common errors such as incorrect escape sequences, invalid characters, and improper structure.
