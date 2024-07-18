import sys
import os

def lexer(input_string):
    tokens = []
    i = 0
    while i < len(input_string):
        if input_string[i] == '{':
            tokens.append(input_string[i])
        elif input_string[i] == '}':
            tokens.append(input_string[i])
        elif input_string[i] == '"':
            start_quote = i
            i += 1 
            while i < len(input_string) and input_string[i] != '"':
                i += 1
            if i < len(input_string):
                tokens.append(input_string[start_quote:i+1])
        elif input_string[i] == ':' or input_string[i] == ',':
            tokens.append(input_string[i])
        elif not input_string[i].isspace():
            raise ValueError(f"unexpected character: {input_string[i]}")
        i += 1 
    return tokens

def parser(tokens):
    if len(tokens) < 3 or tokens[0] != '{' or tokens[-1] != '}' or len(tokens) % 4 != 1 :
        return False
    i = 1 
    while i < len(tokens):
        if not (tokens[i].startswith('"') and tokens[i].endswith('"')):
            return False
        if i+1 >= len(tokens) or tokens[i+1] != ':':
            return False
        if i+2 >= len(tokens) or not (tokens[i+2].startswith('"') and tokens[i+2].endswith('"')):
            return False
        i += 4 
    return True
    
def validate_json(input_string):
    try:
        tokens = lexer(input_string)
        if parser(tokens):
            return "Valid JSON"
        else:
            return "Invalid JSON"
            
    except ValueError as e:
        print(f"Invalid jason: {e}")
        return "Invalid JSON"


def  test_json_files():
    test_folder = 'test_json'
    for test_file in os.listdir(test_folder):
        file_path = os.path.join(test_folder, test_file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                json_content = file.read().strip()
                result = validate_json(json_content)
                print(f"Testing: {test_file} : {result}")
                

if __name__ == "__main__":
    test_json_files()
    

        
