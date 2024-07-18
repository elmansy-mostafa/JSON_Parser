import sys
import os

def lexer(input_string):
    tokens = []
    i = 0
    while i < len(input_string):
        if input_string[i] in ["{", "}"]:
            tokens.append(input_string[i])
        elif input_string[i].isspace():        # ignore whitespace
            pass
        else:
            raise ValueError(f"unexpected character {input_string[i]}")
        i += 1 
    return tokens

def parser(tokens):
    if tokens == ["{", "}"]:
        return "Valid jason"
    else:
        return "Invalid jason"
    
def validate_json(input_string):
    try:
        tokens = lexer(input_string)
        result = parser(tokens)
        return result
    
    except ValueError as e:
        return f"Invalid jason: {e}"



    
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
    

        
