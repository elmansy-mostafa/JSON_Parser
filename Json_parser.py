import os
import re

def lexer(input_string):
    tokens = []
    i = 0
    while i < len(input_string):
        if input_string[i] in ['{', '}', ':', ',', '[', ']']:
            tokens.append(input_string[i])
            i += 1
        elif input_string[i] == '"':   # start of string literal
            start_quote = i
            i += 1
            while i < len(input_string):
                if input_string[i] == '\\':
                    if i + 1 < len(input_string):
                        escape_char = input_string[i + 1]
                        if escape_char in ['"', '\\', '/', 'b', 'f', 'n', 'r', 't']:    # \" (for a quote)  - \\ (for a backslash)  - \/ (for a slash) - \b (for backspace)  - \f (for form feed)  - \n (for newline)-  \r (for carriage return) - \t (for tab)
                            i += 2
                        elif escape_char == 'u':
                            if i + 5 < len(input_string) and all(c in '0123456789abcdefABCDEF' for c in input_string[i+2:i+6]):
                                i += 6
                            else: 
                                raise ValueError(f"Invalid unicode escape sequence : {input_string[i:i+6]}")
                        else: 
                            raise ValueError(f"Invalid escape sequence: {input_string[i:i+2]}")
                    else: 
                        raise ValueError(f"Invalid escape sequence: {input_string[i:i+2]}")
                
                elif input_string[i] == '"':   # end of string literal
                    tokens.append(input_string[start_quote:i+1])
                    i += 1 
                    break
                elif input_string[i] in '\t\n\r':  # add space to a list of invalid character
                    raise ValueError(f"Invalid character in a string : {input_string[i]}")
                else:
                    i += 1
            if i >= len(input_string) or input_string[i - 1] != '"':
                raise ValueError("Unterminated string literal")

        elif re.match(r'-?\d+(\.\d+)?([eE][+-]?\d+)?', input_string[i:]):
            match = re.match(r'-?\d+(\.\d+)?([eE][+-]?\d+)?', input_string[i:])
            tokens.append(match.group(0))
            i += len(match.group(0))
        elif input_string[i:i+4] == 'true' or input_string[i:i+5] == 'false' or input_string[i:i+4] == 'null':
            if input_string[i:i+4] == 'true' or input_string[i:i+4] == 'null':
                tokens.append(input_string[i:i+4])
                i += 4
            else:
                tokens.append(input_string[i:i+5])
                i += 5
        elif input_string[i].isspace():
            i += 1
        else:
            raise ValueError(f"Unexpected character: {input_string[i]}")
    return tokens

def parser_value(tokens, index):
    if index >= len(tokens):
        return -1
    if tokens[index] == '{':
        return parser_object(tokens, index)
    elif tokens[index] == '[':
        return parser_array(tokens, index)
    elif tokens[index].startswith('"') and tokens[index].endswith('"'):
        return index + 1 # string value
    elif tokens[index] in ['true', 'false', 'null']:
        return index + 1 # boolean and null value
    elif tokens[index][0] in '-0123456789':
        num = tokens[index]
        # check for leading zero .... 
        if num[0] == '0' and len(num) > 1 and num[1].isdigit():
            return -1
        if num.startswith('-') and len(num) > 2 and num[1] == '0' and num[2].isdigit():
            return -1     
        return index + 1 # numeric value
    return -1


def parser_object(tokens, index):
    if tokens[index] != "{":
        return -1
    index += 1
    expected_key = True
    while index < len(tokens):
        if tokens[index] == "}":
            return index + 1 
        if expected_key:
            if index >= len(tokens) or not (tokens[index].startswith('"') and tokens[index].endswith('"')):
                return -1
            index += 1
            if index >= len(tokens) or tokens[index] != ':':
                return -1
            index += 1
            index = parser_value(tokens, index)
            if index == -1:
                return -1
            expected_key = False
        else:
            if tokens[index] == ',':
                # check for trailing comma ... 
                if index + 1 >= len(tokens) or tokens[index + 1 ] == '}':
                    return -1
                index += 1
                expected_key = True
            elif tokens[index] == "}":
                return index + 1 
            else:
                return -1
    return -1 
        

def parser_array(tokens, index):
    if tokens[index] != "[":
        return -1
    index += 1 
    expected_value = True
    while index < len(tokens):
        if tokens[index] == ']':
            return index + 1
        if expected_value:
            index = parser_value(tokens, index)
            if index == -1:
                return -1
            expected_value = False
        else:
            if tokens[index] == ',':
                # check for trailing comma ...
                if index + 1 >= len(tokens) or tokens[index + 1 ] == ']':
                    return -1
                index += 1
                expected_value = True
            elif tokens[index] == ']':
                return index + 1
            else:
                return -1
    return -1

def parser(tokens):
    if tokens[0] == '[':
        return parser_array(tokens, 0) == len(tokens)
    elif tokens[0] == '{':
        return parser_object(tokens, 0) == len(tokens)
    return False
    
            

def validate_json(input_string):
    try:
        tokens = lexer(input_string)
        if parser(tokens):
            return "Valid JSON", 0
        else:
            return "Invalid JSON", 1
            
    except ValueError as e:
        return f"Invalid jason: {e}", 1




def  test_json_files():
    test_folder = 'test_json'
    for test_file in os.listdir(test_folder):
        file_path = os.path.join(test_folder, test_file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                json_content = file.read().strip()
                result, exit_code = validate_json(json_content)
                print(f"Testing: {test_file} : {result}")
                if exit_code != 0:
                    print(f"Exit code: {exit_code}")
                
if __name__ == "__main__":
    test_json_files()


    

        
