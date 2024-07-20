import os

def lexer(input_string):
    tokens = []
    i = 0
    while i < len(input_string):
        if input_string[i] in ['{', '}', ':', ',', '[', ']']:
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

def parser_value(tokens, index):
    if tokens[index] == '{':
        return parser_object(tokens, index)
    elif tokens[index] == '[':
        return parser_array(tokens, index)
    elif tokens[index].startswith('"') and tokens[index].endswith('"'):
        return index + 1 # string value
    elif tokens[index] in ['true', 'false', 'null']:
        return index + 1 # boolean and null value
    elif tokens[index].isdigit() or (tokens[index].startswith('-') and tokens[index][1:].isdigit()):
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
            if not (tokens[index].startswith('"') and tokens[index].endswith('"')):
                return -1
            index += 1
            if tokens[index] != ':':
                return -1
            index += 1
            index = parser_value(tokens, index)
            if index == -1:
                return -1
            expected_key = False
        else:
            if tokens[index] == ',':
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
    while index < len(tokens) and tokens[index] != ']':
        index = parser_value(tokens, index)
        if index == -1:
            return -1
        if tokens[index] == ',':
            index += 1
    if tokens[index] != ']':
        return -1
    return index + 1

def parser(tokens):
    if tokens[0] != '{' or tokens[-1] != '}':
        return False
    return parser_object(tokens, 0) == len(tokens)
            

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


    

        
