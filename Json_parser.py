import os

def lexer(input_string):
    tokens = []
    i = 0
    while i < len(input_string):
        if input_string[i] == '{' or input_string[i] == '}' or input_string[i] == ':' or input_string[i] == ',':
            tokens.append(input_string[i])
            i += 1
        elif input_string[i] == '"':
            start_quote = i
            i += 1
            while i < len(input_string) and input_string[i] != '"':
                i += 1
            if i < len(input_string):
                tokens.append(input_string[start_quote:i+1])
            i += 1
        elif input_string[i].isdigit() or input_string[i] == '-':
            start_num = i
            i += 1
            while i < len(input_string) and (input_string[i].isdigit() or input_string[i] == '.'):
                i += 1
            tokens.append(input_string[start_num:i])
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

def parser(tokens):
    if tokens[0] != '{' or tokens[-1] != '}':
        return False

    i = 1
    expected_key = True
    while i < len(tokens) - 1:
        if expected_key:
            if not (tokens[i].startswith('"') and tokens[i].endswith('"')):
                return False
            expected_key = False
        else:
            if tokens[i] != ':':
                return False
            if i + 1 >= len(tokens):
                return False
            if not (tokens[i + 1].startswith('"') and tokens[i+1].endswith('"')) and tokens[i + 1] not in ['true', 'false', 'null'] and not tokens[i + 1].isdigit() and not (tokens[i + 1].startswith('-') and tokens[i + 1][1:].isdigit()):
                return False
            expected_key = True
            i += 2 # skip the value token
        i += 1 # move to the next token
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


    

        
