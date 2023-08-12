import os
import re

def tokenize(input_str):
    tokens = []
    pattern = r"([0-9]+\.[0-9]+|[0-9]+|\+|\-|\*|\/|\(|\))"
    matches = re.finditer(pattern, input_str)

    for match in matches:
        token = match.group()
        if re.match(r"[0-9]+\.[0-9]+", token):
            tokens.append(("NUMERO_DECIMAL", token))
        elif re.match(r"[0-9]+", token):
            tokens.append(("NUMERO_ENTERO", token))
        elif token in "+-*/":
            tokens.append(("SIGNO_MAS" if token == "+" else "SIGO_MULTIPLICACION", token))
        elif token == "(":
            tokens.append(("PARENTESIS_IZQ", token))
        elif token == ")":
            tokens.append(("PARENTESIS_DER", token))
        else:
            tokens.append(("ERROR", token))
    
    return tokens

nombre_archivo = "numeros.txt"
ruta_archivo = "C:/Users/Wuux/Desktop/Compiladores"
ruta_completa = os.path.join(ruta_archivo, nombre_archivo)

if os.path.exists(ruta_completa):
    archivo = open(ruta_completa, "r", encoding="utf-8")
    contenido = archivo.read()
    archivo.close()

    tokens = tokenize(contenido)
    for token_type, token_value in tokens:
        print(f"{token_type:20} {token_value:10}")

else:
    archivo = open(ruta_completa, "w")
    archivo.write("Curso de compiladores.\n")
    archivo.close()
