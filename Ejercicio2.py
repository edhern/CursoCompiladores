import os
import re

def tokenize_cpp_code(cpp_code):
    keywords = {"while", "if", "return", "cout", "cin"}  # Palabras clave
    special_symbols = {"(", ")", "[", "]", "{", "}"}  # Símbolos especiales
    operators = {"*", "+", "-", "/", "%"}  # Operadores
    logical_operators = {"&&", "||", ">", "<", "==", "!="}  # Operadores lógicos

    tokens = []
    lines = cpp_code.split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith("#include"):
            continue
        for word in re.findall(r'\w+|\S', line):
            if word in keywords:
                tokens.append(("palabras claves", word))
            elif word in special_symbols:
                tokens.append(("simbolos especiales", word))
            elif word in operators:
                tokens.append(("operadores", word))
            elif word in logical_operators:
                tokens.append(("operadores logicos", word))
            elif re.match(r'^[a-zA-Z_]\w*$', word):
                tokens.append(("identificadores", word))

    return tokens

nombre_archivo = "evaluadores.txt"
ruta_archivo =  "C:/Users/Wuux/Desktop/Compiladores"  # Coloca la ruta correcta aquí
ruta_completa = os.path.join(ruta_archivo, nombre_archivo)

if os.path.exists(ruta_completa):
    archivo = open(ruta_completa, "r", encoding="utf-8")
    cpp_code = archivo.read()
    archivo.close()

    tokens = tokenize_cpp_code(cpp_code)
    
    categories = {
        "palabras claves": set(),
        "identificadores": set(),
        "operadores": set(),
        "operadores logicos": set(),
        "simbolos especiales": set()
    }
    
    for token_type, token_value in tokens:
        if token_type in categories:
            categories[token_type].add(token_value)
    
    for category, values in categories.items():
        print(f"{category:20} {', '.join(values)}")

else:
    print("El archivo no existe.")
